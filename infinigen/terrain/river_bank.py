import numpy as np
import heapq
from scipy.ndimage import gaussian_filter
from infinigen.terrain.utils import Mesh
from infinigen.assets.material.ice_final import shader_ice_final as mat_ice
from infinigen.assets.material.snow_terrain import shader_snow_terrain as mat_snow
from infinigen.core import surface
from infinigen.core.util.math import FixedSeed


def gen_river_and_hightmap(
    H,
    W,
    SInit,
    SMin,
    SMax,
    SDeltaSigma,
    HDeltaArctanK,
    HDeltaArctanB,
    HDeltaRange,
    BSplineres,
    GaussianFilterSigma,
    CurveNoise,
    CurveFreq,
    YMin,
    YMax,
    SinXDivXBeg,
    SinXDivXGap,
    ):
    print('---------------------------')
    print(SInit,
        SinXDivXBeg,
        SinXDivXGap)
    print('---------------------------')
    Ps = []
    min_y, max_y = None, None
    last_noise = 0.
    for i in range(CurveFreq * 2):
        x = SinXDivXBeg + i * SinXDivXGap
        cur_noise = last_noise + np.random.uniform(-CurveNoise, CurveNoise)
        y = np.sin(x) / x + cur_noise
        last_noise = cur_noise
        Ps.append((-0.5 + i / CurveFreq, y))
        if i == 0:
            min_y = y
            max_y = y
        else:
            min_y = min(y, min_y)
            max_y = max(y, max_y)
    for i in range(len(Ps)):
        Ps[i] = (Ps[i][0], (Ps[i][1] - min_y) / (max_y - min_y) * (YMax - YMin) + YMin)
    print(Ps)
    BSplineN = 4
    BSplineMat = [
        [-1 / 6, 3 / 6, -3 / 6, 1 / 6],
        [3 / 6, -6 / 6, 3 / 6, 0],
        [-3 / 6, 0, 3 / 6, 0],
        [1 / 6, 4 / 6, 1 / 6, 0]
    ]
    river_mask = np.zeros((H, W))
    S = SInit
    for n in range(len(Ps) - BSplineN + 1):
        V = [
            np.array(Ps[n]) * np.array([H, W]),
            np.array(Ps[n + 1]) * np.array([H, W]),
            np.array(Ps[n + 2]) * np.array([H, W]),
            np.array(Ps[n + 3]) * np.array([H, W]),
        ]
        for t in range(BSplineres + 1):
            u = t / BSplineres
            U = [u ** 3, u * u, u, 1]
            Q = np.zeros_like(V[0])
            for i in range(BSplineN):
                for j in range(BSplineN):
                    Q += U[i] * BSplineMat[i][j] * V[j]
            x = int(round(float(Q[0])))
            y = int(round(float(Q[1])))
            if max(x, 0) < int(min(x + S, H)) and max(y, 0) < int(min(y + S, W)):
                river_mask[max(x, 0):int(min(x + S, H)), max(y, 0):int(min(y + S, W))] = 1
            S += np.random.normal(0, SDeltaSigma)
            S = min(max(S, SMin), SMax)

    dx = [-1, -1, -1, 0, 0, 1, 1, 1]
    dy = [-1, 0, 1, -1, 1, -1, 0, 1]
    hmap = -np.ones_like(river_mask)
    heap = []
    for x in range(H):
        for y in range(W):
            if river_mask[x][y] > 0:
                heapq.heappush(heap, (0, x, y))
                hmap[x][y] = 0
    while len(heap) > 0:
        top = heapq.heappop(heap)
        x, y = top[1], top[2]
        for k in range(len(dx)):
            nx, ny = x + dx[k], y + dy[k]
            if 0 <= nx < H and 0 <= ny < W:
                if hmap[nx][ny] < 0:
                    tmp = hmap[x][y]
                    HDeltaMin = np.pi / 2 - np.arctan(HDeltaArctanK * tmp + HDeltaArctanB)
                    hmap[nx][ny] = tmp + np.random.uniform(HDeltaMin, HDeltaMin + HDeltaRange)
                    heapq.heappush(heap, (hmap[nx][ny], nx, ny))
    hmap = gaussian_filter(hmap, GaussianFilterSigma)
    hmap[river_mask > 0] = 0
    return river_mask, hmap



class RiverBank:
    def __init__(
        self,
        seed=0,
        H=2048,W=2048,YMin=-0.,YMax=1.,SMin=32,SMax=64,SDeltaSigma=0.2,HDeltaArctanK=0.1,HDeltaArctanB=5,HDeltaRange=0.5,BSplineres=4096,GaussianFilterSigma=32,CurveNoise=0.01,CurveFreq=32,
        SInit=96,
        SinXDivXBeg=0.1,
        SinXDivXGap=0.3,
        ice_param=0.,
        ice_param_scale= 12.0,
        ice_param_position = 0.0,
        MAX_HEIGHT = 10,  # max height
    ):
        print('---------------------------')
        print(SInit,
            SinXDivXBeg,
            SinXDivXGap)
        print('---------------------------')
        self._river, self._hmap = gen_river_and_hightmap(
    H,
    W,
    SInit,
    SMin,
    SMax,
    SDeltaSigma,
    HDeltaArctanK,
    HDeltaArctanB,
    HDeltaRange,
    BSplineres,
    GaussianFilterSigma,
    CurveNoise,
    CurveFreq,
    YMin,
    YMax,
    SinXDivXBeg,
    SinXDivXGap)
        self._max_height = MAX_HEIGHT
        self._hmap = self._hmap / self._hmap.max() * self._max_height
        with FixedSeed(seed):
            self._ice_params = {
                'ice_param': ice_param,
                'scale': ice_param_scale,
                'position': ice_param_position
            }
    
    def create_asset(self, name='RiverBank', scale=100):
        mesh = Mesh(heightmap=self._hmap, L=scale)
        
        mesh.vertex_attributes["river"] = self._river.reshape(-1).astype(np.float32)
        mesh.vertex_attributes["bank"] = 1 - self._river.reshape(-1).astype(np.float32)

        obj = mesh.export_blender(name)
        
        surface.add_material(obj, mat_ice, selection="river", input_kwargs={'params': self._ice_params})
        surface.add_material(obj, mat_snow, selection="bank", input_kwargs={'params': self._ice_params})
        return obj

    def h_map(self):
        return self._hmap.copy()

    def river_mask(self):
        return self._river > 0
    
    def h_map_normal(self):
        dh_dx = np.zeros_like(self._hmap)
        dh_dx[:-1, :] = self._hmap[1:, :] - self._hmap[:-1, :]
        x_dir = np.stack([np.ones_like(dh_dx), np.zeros_like(dh_dx), dh_dx], axis=-1)

        dh_dy = np.zeros_like(self._hmap)
        dh_dy[:, :-1] = self._hmap[:, 1:] - self._hmap[:, :-1]
        y_dir = np.stack([np.zeros_like(dh_dy), np.ones_like(dh_dy), dh_dy], axis=-1)

        n_dir = np.cross(x_dir, y_dir)
        return n_dir
