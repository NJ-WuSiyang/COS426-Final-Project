import bpy
import os
import numpy as np
from infinigen.assets.snowman import Snowman
from infinigen.assets.snowfall import Snowfall
from infinigen.terrain.river_bank import RiverBank
from infinigen.core.placement.camera import spawn_camera, set_active_camera

from infinigen.assets.lighting import sky_lighting

river_bank_geom_params = [
    dict(
        H=2048,W=2048,YMin=-0.,YMax=1.,SMin=32,SMax=64,SDeltaSigma=0.2,HDeltaArctanK=0.1,HDeltaArctanB=5,HDeltaRange=0.5,BSplineres=4096,GaussianFilterSigma=32,CurveNoise=0.01,CurveFreq=32,
        SInit=96,
        SinXDivXBeg=0.1,
        SinXDivXGap=0.3,
    ),
    dict(
        H=2048,W=2048,YMin=-0.,YMax=1.,SMin=32,SMax=64,SDeltaSigma=0.2,HDeltaArctanK=0.1,HDeltaArctanB=5,HDeltaRange=0.5,BSplineres=4096,GaussianFilterSigma=32,CurveNoise=0.01,CurveFreq=32,
        SInit=96,
        SinXDivXBeg=2.5,
        SinXDivXGap=0.3,
    ),
    dict(
        H=2048,W=2048,YMin=-0.,YMax=1.,SMin=32,SMax=64,SDeltaSigma=0.2,HDeltaArctanK=0.1,HDeltaArctanB=5,HDeltaRange=0.5,BSplineres=4096,GaussianFilterSigma=32,CurveNoise=0.01,CurveFreq=32,
        SInit=96,
        SinXDivXBeg=4.9,
        SinXDivXGap=0.3,
    ),
    dict(
        H=2048,W=2048,YMin=-0.,YMax=1.,SMin=32,SMax=64,SDeltaSigma=0.2,HDeltaArctanK=0.1,HDeltaArctanB=5,HDeltaRange=0.5,BSplineres=4096,GaussianFilterSigma=32,CurveNoise=0.01,CurveFreq=32,
        SInit=96,
        SinXDivXBeg=2.5,
        SinXDivXGap=0.1,
    ),
    dict(
        H=2048,W=2048,YMin=-0.,YMax=1.,SMin=32,SMax=64,SDeltaSigma=0.2,HDeltaArctanK=0.1,HDeltaArctanB=5,HDeltaRange=0.5,BSplineres=4096,GaussianFilterSigma=32,CurveNoise=0.01,CurveFreq=32,
        SInit=96,
        SinXDivXBeg=2.5,
        SinXDivXGap=0.5,
    ),
    dict(
        H=2048,W=2048,YMin=-0.,YMax=1.,SMin=32,SMax=64,SDeltaSigma=0.2,HDeltaArctanK=0.1,HDeltaArctanB=5,HDeltaRange=0.5,BSplineres=4096,GaussianFilterSigma=32,CurveNoise=0.01,CurveFreq=32,
        SInit=64,
        SinXDivXBeg=0.1,
        SinXDivXGap=0.3,
    ),
    dict(
        H=2048,W=2048,YMin=-0.,YMax=1.,SMin=32,SMax=64,SDeltaSigma=0.2,HDeltaArctanK=0.1,HDeltaArctanB=5,HDeltaRange=0.5,BSplineres=4096,GaussianFilterSigma=32,CurveNoise=0.01,CurveFreq=32,
        SInit=128,
        SinXDivXBeg=0.1,
        SinXDivXGap=0.3,
    )
]


river_bank_material_params = [dict(
        ice_param = 2., #10, 25
        ice_param_scale = 100., #
        ice_param_position = 0.1, #0.1, 0.2
        ),
        dict(
                ice_param = 10., #10, 25
                ice_param_scale = 100., #
                ice_param_position = 0.1, #0.1, 0.2
        ),
        dict(
                ice_param = 25., #10, 25
                ice_param_scale = 100., #
                ice_param_position = 0.1, #0.1, 0.2
        ),
        dict(
                ice_param = 50., #10, 25
                ice_param_scale = 500., #
                ice_param_position = 0.5, #0.1, 0.2
        ),
        dict(
                ice_param = 25., #10, 25
                ice_param_scale = 200., #
                ice_param_position = 0.2, #0.1, 0.2
        ),
]

snowfall_params = [
    dict(
        density = 800.0, #np.random.uniform(10.0, 1000.0),
        radius = 0.001
    ),
    dict(
        density = 1000.0, #np.random.uniform(10.0, 1000.0),
        radius = 0.005
    ),
    dict(
        density = 1500.0, #np.random.uniform(10.0, 1000.0),
        radius = 0.001
    ),
    dict(
        density = 800.0, #np.random.uniform(10.0, 1000.0),
        radius = 0.002
    ),
    dict(
        density = 800.0, #np.random.uniform(10.0, 1000.0),
        radius = 0.0005
    ),
]

MinSnowmanDeltaH = 0.3
MaxSnowmanDeltaH = 0.6
MaxSnowmanRot = 5
SnowmanBorder = 100
MinSnowmanRiverDist = 80

river_bank_geom_param_id = 6
river_bank_mat_parm_id = 2
snowfall_param_id = 1
NSnowman = 30
SnowmanGap = 100 

sky_lighting.add_lighting()

river_bank = RiverBank(        
    ice_param=river_bank_material_params[river_bank_mat_parm_id]['ice_param'],
    ice_param_scale=river_bank_material_params[river_bank_mat_parm_id]['ice_param_scale'],
    ice_param_position=river_bank_material_params[river_bank_mat_parm_id]['ice_param_position'],
    **river_bank_geom_params[river_bank_geom_param_id]
)
river_bank.create_asset()
snowfall = Snowfall(0, scale=np.array([35, 35, 35]), density = snowfall_params[snowfall_param_id]['density'], radius = snowfall_params[snowfall_param_id]['radius'])
snowfall.create_asset()

river = river_bank.river_mask()
hmap = river_bank.h_map()
xs, ys, zs = [], [], []
rxs, rys, rzs = [], [], []
snowmans = []
for i in range(NSnowman):
    while True:
        x = np.random.randint(low=SnowmanBorder, high=hmap.shape[0] - SnowmanBorder)
        y = np.random.randint(low=SnowmanBorder, high=hmap.shape[1] - SnowmanBorder)
        print(max(0, x-MinSnowmanRiverDist),min(hmap.shape[0], x+MinSnowmanRiverDist),max(0, y-MinSnowmanRiverDist),min(hmap.shape[1], y+MinSnowmanRiverDist))
        if river[max(0, x-MinSnowmanRiverDist):min(hmap.shape[0], x+MinSnowmanRiverDist),max(0, y-MinSnowmanRiverDist):min(hmap.shape[1], y+MinSnowmanRiverDist)].max() > 0:
            continue

        overlap = False
        for j in range(i):
            if x - SnowmanGap < xs[j] < x + SnowmanGap and y - SnowmanGap < ys[j] < y + SnowmanGap:
                overlap = True
                break

        if not overlap:
            xs.append((x / hmap.shape[0] - 0.5) * 100)
            ys.append((y / hmap.shape[1] - 0.5) * 100)
            zs.append(hmap[x][y] + np.random.uniform(MinSnowmanDeltaH, MaxSnowmanDeltaH))
            rxs.append(np.random.uniform(-MaxSnowmanRot, MaxSnowmanRot) / 180 * np.pi)
            rys.append(np.random.uniform(-MaxSnowmanRot, MaxSnowmanRot) / 180 * np.pi)
            rzs.append(np.random.uniform(0, np.pi * 2))
            snowmans.append(Snowman(0, f'snowman_{i}', trans=np.array([xs[-1], ys[-1], zs[-1]]), rot=np.array([rxs[-1], rys[-1], rzs[-1]])))
            break

for snowman in snowmans:
    snowman.create_asset()

print(os.path.join(os.path.abspath(os.curdir), f"generated_scene.blend"))
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(os.path.abspath(os.curdir), f"generated_scene.blend"))