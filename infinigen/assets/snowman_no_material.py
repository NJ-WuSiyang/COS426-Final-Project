import bpy
import mathutils
import numpy as np
from numpy.random import uniform, normal, randint
from infinigen.core.nodes.node_wrangler import Nodes, NodeWrangler
from infinigen.core.nodes import node_utils
from infinigen.core.util.color import color_category
from infinigen.core import surface

from infinigen.core.placement.factory import AssetFactory
from infinigen.core.util.math import FixedSeed
from infinigen.core.util import blender as butil


def geometry_nodes(nw: NodeWrangler, params):
    # Code generated using version 2.6.5 of the node_transpiler

    cylinder = nw.new_node('GeometryNodeMeshCylinder', input_kwargs={'Vertices': 30, 'Radius': 0.3000, 'Depth': 0.6000})
    
    body_input = nw.new_node(Nodes.GroupInput,
        label='BodyInput',
        expose_input=[('NodeSocketGeometry', 'Geometry', None),
            ('NodeSocketFloat', 'BottomRadius', params['BottomRadius']),
            ('NodeSocketFloat', 'BottomX', 0.0000),
            ('NodeSocketFloat', 'BottomY', 0.0000),
            ('NodeSocketFloat', 'BottomZ', 0.0000),
            ('NodeSocketFloat', 'BottomXYScale', params['BottomXYScale']),
            ('NodeSocketFloat', 'MiddleScale', params['MiddleScale']),
            ('NodeSocketFloat', 'MiddleXYScale', params['MiddleXYScale']),
            ('NodeSocketFloat', 'TopScale', params['TopScale'])])
    
    reroute = nw.new_node(Nodes.Reroute, input_kwargs={'Input': body_input.outputs["BottomRadius"]})
    
    top_radius = nw.new_node(Nodes.Math,
        input_kwargs={0: reroute, 1: body_input.outputs["TopScale"]},
        label='TopRadius',
        attrs={'operation': 'MULTIPLY'})
    
    middle_radius = nw.new_node(Nodes.Math,
        input_kwargs={0: reroute, 1: body_input.outputs["MiddleScale"]},
        label='MiddleRadius',
        attrs={'operation': 'MULTIPLY'})
    
    m_t_dist = nw.new_node(Nodes.Math, input_kwargs={0: middle_radius, 1: top_radius}, label='MTDist')
    
    m_t_scaled_dist = nw.new_node(Nodes.Math, input_kwargs={0: m_t_dist, 1: 0.8000}, label='MTScaledDist', attrs={'operation': 'MULTIPLY'})
    
    b_m_dist = nw.new_node(Nodes.Math, input_kwargs={0: middle_radius, 1: body_input.outputs["BottomRadius"]}, label='BMDist')
    
    b_m_scaled_dist = nw.new_node(Nodes.Math, input_kwargs={0: b_m_dist, 1: 0.8000}, label='BMScaledDist', attrs={'operation': 'MULTIPLY'})
    
    middle_z = nw.new_node(Nodes.Math, input_kwargs={0: b_m_scaled_dist, 1: body_input.outputs["BottomZ"]}, label='MiddleZ')
    
    top_z = nw.new_node(Nodes.Math, input_kwargs={0: m_t_scaled_dist, 1: middle_z}, label='TopZ')
    
    hat_z = nw.new_node(Nodes.Math, input_kwargs={0: top_radius, 1: top_z}, label='HatZ')
    
    hat_top_z = nw.new_node(Nodes.Math, input_kwargs={0: hat_z, 1: 0.2000}, label='HatTopZ')
    
    hat_top_trans = nw.new_node(Nodes.CombineXYZ,
        input_kwargs={'X': body_input.outputs["BottomX"], 'Y': body_input.outputs["BottomY"], 'Z': hat_top_z},
        label='HatTopTrans')
    
    transform_geometry_7 = nw.new_node(Nodes.Transform, input_kwargs={'Geometry': cylinder.outputs["Mesh"], 'Translation': hat_top_trans})
    
    cube = nw.new_node(Nodes.MeshCube, input_kwargs={'Size': (1.9500, 0.1000, 0.1000)})
    
    middle_translation = nw.new_node(Nodes.CombineXYZ,
        input_kwargs={'X': body_input.outputs["BottomX"], 'Y': body_input.outputs["BottomY"], 'Z': middle_z},
        label='MiddleTranslation')
    
    value = nw.new_node(Nodes.Value)
    value.outputs[0].default_value = 0.4000
    
    combine_xyz = nw.new_node(Nodes.CombineXYZ, input_kwargs={'Y': value})
    
    transform_geometry_5 = nw.new_node(Nodes.Transform,
        input_kwargs={'Geometry': cube.outputs["Mesh"], 'Translation': middle_translation, 'Rotation': combine_xyz})
    
    uv_sphere_1 = nw.new_node(Nodes.MeshUVSphere, input_kwargs={'Radius': 0.1000})
    
    delta_x = nw.new_node(Nodes.Math, input_kwargs={0: -0.3600, 1: top_radius}, label='DeltaX', attrs={'operation': 'MULTIPLY'})
    
    delta_y = nw.new_node(Nodes.Math, input_kwargs={0: -0.9000, 1: top_radius}, label='DeltaY', attrs={'operation': 'MULTIPLY'})
    
    delta_z = nw.new_node(Nodes.Math, input_kwargs={0: 0.4000, 1: top_radius}, label='DeltaZ', attrs={'operation': 'MULTIPLY'})
    
    delta = nw.new_node(Nodes.CombineXYZ, input_kwargs={'X': delta_x, 'Y': delta_y, 'Z': delta_z}, label='Delta')
    
    delta1 = nw.new_node(Nodes.VectorMath,
        input_kwargs={0: delta, 1: (1.0000, 1.0000, 1.0000)},
        label='Delta1',
        attrs={'operation': 'MULTIPLY'})
    
    top_translation = nw.new_node(Nodes.CombineXYZ,
        input_kwargs={'X': body_input.outputs["BottomX"], 'Y': body_input.outputs["BottomY"], 'Z': top_z},
        label='TopTranslation')
    
    trans1 = nw.new_node(Nodes.VectorMath, input_kwargs={0: delta1.outputs["Vector"], 1: top_translation}, label='Trans1')
    
    top_x_y_scale = nw.new_node(Nodes.Math, input_kwargs={0: top_radius, 1: 1.0000}, label='TopXYScale', attrs={'operation': 'MULTIPLY'})
    
    combine_xyz_6 = nw.new_node(Nodes.CombineXYZ, input_kwargs={'X': top_x_y_scale, 'Y': top_x_y_scale, 'Z': top_radius})
    
    scale = nw.new_node(Nodes.VectorMath,
        input_kwargs={0: combine_xyz_6, 1: (1.4000, 1.0000, 2.0000)},
        label='scale',
        attrs={'operation': 'MULTIPLY'})
    
    transform_geometry_3 = nw.new_node(Nodes.Transform,
        input_kwargs={'Geometry': uv_sphere_1.outputs["Mesh"], 'Translation': trans1.outputs["Vector"], 'Rotation': (-0.2112, -0.0279, 0.0000), 'Scale': scale.outputs["Vector"]})
    
    cone = nw.new_node('GeometryNodeMeshCone', input_kwargs={'Radius Bottom': 0.1500, 'Depth': 0.5900})
    
    node_y_trans = nw.new_node(Nodes.Math,
        input_kwargs={0: top_x_y_scale, 1: -0.8000},
        label='NodeYTrans',
        attrs={'operation': 'MULTIPLY'})
    
    combine_xyz_10 = nw.new_node(Nodes.CombineXYZ, input_kwargs={'Y': node_y_trans})
    
    add = nw.new_node(Nodes.VectorMath, input_kwargs={0: top_translation, 1: combine_xyz_10})
    
    multiply = nw.new_node(Nodes.VectorMath,
        input_kwargs={0: combine_xyz_6, 1: (1.0000, 1.0000, 1.0000)},
        attrs={'operation': 'MULTIPLY'})
    
    transform_geometry_2 = nw.new_node(Nodes.Transform,
        input_kwargs={'Geometry': cone.outputs["Mesh"], 'Translation': add.outputs["Vector"], 'Rotation': (1.5708, 0.0000, 0.0000), 'Scale': multiply.outputs["Vector"]})
    
    uv_sphere = nw.new_node(Nodes.MeshUVSphere, input_kwargs={'Segments': 64, 'Rings': 32, 'Radius': reroute})
    
    middle_x_y_scale = nw.new_node(Nodes.Math,
        input_kwargs={0: middle_radius, 1: body_input.outputs["MiddleXYScale"]},
        label='MiddleXYScale',
        attrs={'operation': 'MULTIPLY'})
    
    middle_scale = nw.new_node(Nodes.CombineXYZ,
        input_kwargs={'X': middle_x_y_scale, 'Y': middle_x_y_scale, 'Z': middle_radius},
        label='MiddleScale')
    
    transform_geometry = nw.new_node(Nodes.Transform,
        input_kwargs={'Geometry': uv_sphere.outputs["Mesh"], 'Translation': middle_translation, 'Scale': middle_scale})
    
    bottom_trans = nw.new_node(Nodes.CombineXYZ,
        input_kwargs={'X': body_input.outputs["BottomX"], 'Y': body_input.outputs["BottomY"], 'Z': body_input.outputs["BottomZ"]},
        label='BottomTrans')
    
    bottom_scale = nw.new_node(Nodes.CombineXYZ,
        input_kwargs={'X': body_input.outputs["BottomXYScale"], 'Y': body_input.outputs["BottomXYScale"], 'Z': 1.0000},
        label='BottomScale')
    
    transform_geometry_9 = nw.new_node(Nodes.Transform,
        input_kwargs={'Geometry': uv_sphere.outputs["Mesh"], 'Translation': bottom_trans, 'Scale': bottom_scale})
    
    transform_geometry_1 = nw.new_node(Nodes.Transform,
        input_kwargs={'Geometry': uv_sphere.outputs["Mesh"], 'Translation': top_translation, 'Scale': combine_xyz_6})
    
    join_geometry = nw.new_node(Nodes.JoinGeometry,
        input_kwargs={'Geometry': [transform_geometry, transform_geometry_9, transform_geometry_1]})
    
    join_geometry_1 = nw.new_node(Nodes.JoinGeometry, input_kwargs={'Geometry': [transform_geometry_2, join_geometry]})
    
    delta2 = nw.new_node(Nodes.VectorMath,
        input_kwargs={0: delta, 1: (-1.0000, 1.0000, 1.0000)},
        label='Delta2',
        attrs={'operation': 'MULTIPLY'})
    
    trans2 = nw.new_node(Nodes.VectorMath, input_kwargs={0: top_translation, 1: delta2.outputs["Vector"]}, label='Trans2')
    
    transform_geometry_4 = nw.new_node(Nodes.Transform,
        input_kwargs={'Geometry': uv_sphere_1.outputs["Mesh"], 'Translation': trans2.outputs["Vector"], 'Rotation': (-0.2112, 0.0279, 0.0000), 'Scale': scale.outputs["Vector"]})
    
    join_geometry_2 = nw.new_node(Nodes.JoinGeometry,
        input_kwargs={'Geometry': [transform_geometry_3, join_geometry_1, transform_geometry_4]})
    
    multiply_1 = nw.new_node(Nodes.Math, input_kwargs={0: value, 1: -1.0000}, attrs={'operation': 'MULTIPLY'})
    
    combine_xyz_1 = nw.new_node(Nodes.CombineXYZ, input_kwargs={'Y': multiply_1})
    
    transform_geometry_6 = nw.new_node(Nodes.Transform,
        input_kwargs={'Geometry': cube.outputs["Mesh"], 'Translation': middle_translation, 'Rotation': combine_xyz_1})
    
    join_geometry_3 = nw.new_node(Nodes.JoinGeometry,
        input_kwargs={'Geometry': [transform_geometry_5, join_geometry_2, transform_geometry_6]})
    
    hat_bottom_z = nw.new_node(Nodes.Math, input_kwargs={0: hat_z, 1: -0.1000}, label='HatBottomZ')
    
    hat_bottom_trans = nw.new_node(Nodes.CombineXYZ,
        input_kwargs={'X': body_input.outputs["BottomX"], 'Y': body_input.outputs["BottomY"], 'Z': hat_bottom_z},
        label='HatBottomTrans')
    
    transform_geometry_8 = nw.new_node(Nodes.Transform,
        input_kwargs={'Geometry': cylinder.outputs["Mesh"], 'Translation': hat_bottom_trans, 'Scale': (1.5000, 1.5000, 0.1000)})
    
    join_geometry_4 = nw.new_node(Nodes.JoinGeometry,
        input_kwargs={'Geometry': [transform_geometry_7, join_geometry_3, transform_geometry_8]})
    
    group_output = nw.new_node(Nodes.GroupOutput,
        input_kwargs={'Geometry': join_geometry_4, 1: m_t_dist, 2: middle_z, 3: top_z},
        attrs={'is_active_output': True})


def apply(obj, params, selection=None, **kwargs):
    surface.add_geomod(obj, geometry_nodes, selection=selection, attributes=[], input_kwargs={'params': params})

class Snowman(AssetFactory):

    def __init__(self, factory_seed, name='snowman', trans=np.array([0, 0, 0]), rot=np.array([0, 0, 0])):
        super().__init__(factory_seed)
        self._name = name
        self._trans = trans.copy()
        self._rot = rot.copy()
        with FixedSeed(factory_seed):
            self.params = {
                'BottomRadius': np.random.uniform(0.9, 1.0),
                'BottomXYScale': np.random.uniform(1.0, 1.2),
                'MiddleScale': np.random.uniform(0.65, 0.75),
                'MiddleXYScale': np.random.uniform(1.0, 1.1),
                'TopScale': np.random.uniform(0.45, 0.55),
            }

    def create_asset(self, **kwargs):
        obj = butil.spawn_vert(self._name) # dummy empty object to apply on
        apply(obj, self.params)
        for i in range(3):
            obj.location[i] = self._trans[i]
        for i in range(3):
            obj.rotation_euler[i] = self._rot[i]
        return obj
