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


def shader_hat(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    noise_texture = nw.new_node(Nodes.NoiseTexture,
        input_kwargs={'Scale': 10.7000, 'Detail': 5.6000, 'Roughness': 0.0000, 'Distortion': 1.2000})
    
    color_ramp = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': noise_texture.outputs["Fac"]})
    color_ramp.color_ramp.elements[0].position = 0.0295
    color_ramp.color_ramp.elements[0].color = [1.0000, 0.1648, 0.0000, 1.0000]
    color_ramp.color_ramp.elements[1].position = 0.0818
    color_ramp.color_ramp.elements[1].color = [0.0000, 0.0000, 0.0000, 1.0000]
    
    noise_texture_1 = nw.new_node(Nodes.NoiseTexture,
        input_kwargs={'Scale': 7.2000, 'Detail': 15.0000, 'Roughness': 0.0000, 'Distortion': 1.2000})
    
    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF,
        input_kwargs={'Base Color': color_ramp.outputs["Color"], 'Roughness': noise_texture_1.outputs["Fac"]})
    
    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

def shader_arms(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    texture_coordinate = nw.new_node(Nodes.TextureCoord)
    
    mapping = nw.new_node(Nodes.Mapping,
        input_kwargs={'Vector': texture_coordinate.outputs["Object"], 'Scale': (1.4000, 1.0000, 1.0000)})
    
    musgrave_texture = nw.new_node(Nodes.MusgraveTexture, input_kwargs={'Vector': mapping})
    
    noise_texture = nw.new_node(Nodes.NoiseTexture,
        input_kwargs={'Vector': musgrave_texture, 'Scale': 2.0000, 'Detail': 18.0000, 'Roughness': 0.8125, 'Distortion': 0.8000})
    
    color_ramp = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': noise_texture.outputs["Fac"]})
    color_ramp.color_ramp.interpolation = "EASE"
    color_ramp.color_ramp.elements.new(0)
    color_ramp.color_ramp.elements[0].position = 0.3500
    color_ramp.color_ramp.elements[0].color = [1.0000, 0.2314, 0.0542, 1.0000]
    color_ramp.color_ramp.elements[1].position = 0.4977
    color_ramp.color_ramp.elements[1].color = [0.5000, 0.0889, 0.0000, 1.0000]
    color_ramp.color_ramp.elements[2].position = 0.8023
    color_ramp.color_ramp.elements[2].color = [0.0000, 0.0000, 0.0000, 1.0000]
    
    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF,
        input_kwargs={'Base Color': color_ramp.outputs["Color"], 'Subsurface Color': color_ramp.outputs["Color"], 'Roughness': 0.1000})
    
    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

def shader_eyes(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    texture_coordinate = nw.new_node(Nodes.TextureCoord)
    
    mapping = nw.new_node(Nodes.Mapping, input_kwargs={'Vector': texture_coordinate.outputs["Object"]})
    
    musgrave_texture = nw.new_node(Nodes.MusgraveTexture, input_kwargs={'Vector': mapping})
    
    noise_texture = nw.new_node(Nodes.NoiseTexture,
        input_kwargs={'Vector': musgrave_texture, 'Scale': 2.0000, 'Detail': 18.0000, 'Roughness': 0.4167, 'Distortion': 0.8000})
    
    color_ramp = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': noise_texture.outputs["Fac"]})
    color_ramp.color_ramp.elements[0].position = 0.0000
    color_ramp.color_ramp.elements[0].color = [1.0000, 1.0000, 1.0000, 1.0000]
    color_ramp.color_ramp.elements[1].position = 0.5068
    color_ramp.color_ramp.elements[1].color = [0.0000, 0.0000, 0.0000, 1.0000]
    
    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF,
        input_kwargs={'Base Color': color_ramp.outputs["Color"], 'Subsurface Color': color_ramp.outputs["Color"], 'Roughness': 0.1000})
    
    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

def shader_nose(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    texture_coordinate = nw.new_node(Nodes.TextureCoord)
    
    mapping = nw.new_node(Nodes.Mapping, input_kwargs={'Vector': texture_coordinate.outputs["Object"]})
    
    wave_texture = nw.new_node(Nodes.WaveTexture,
        input_kwargs={'Vector': mapping, 'Scale': 4.0000, 'Distortion': 14.8000, 'Detail': 11.0000, 'Detail Roughness': 0.6038},
        attrs={'bands_direction': 'Y'})
    
    noise_texture = nw.new_node(Nodes.NoiseTexture,
        input_kwargs={'Vector': wave_texture.outputs["Color"], 'Scale': 10.7000, 'Detail': 5.6000, 'Roughness': 0.0000, 'Distortion': 1.2000})
    
    color_ramp = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': noise_texture.outputs["Fac"]})
    color_ramp.color_ramp.elements[0].position = 0.0000
    color_ramp.color_ramp.elements[0].color = [0.0000, 0.0000, 0.0000, 1.0000]
    color_ramp.color_ramp.elements[1].position = 0.3091
    color_ramp.color_ramp.elements[1].color = [1.0000, 0.2196, 0.0000, 1.0000]
    
    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF,
        input_kwargs={'Base Color': color_ramp.outputs["Color"], 'Subsurface Color': color_ramp.outputs["Color"], 'Roughness': 0.1000})
    
    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

def shader_material_002(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    texture_coordinate = nw.new_node(Nodes.TextureCoord)
    
    mapping = nw.new_node(Nodes.Mapping, input_kwargs={'Vector': texture_coordinate.outputs["Object"]})
    
    voronoi_texture = nw.new_node(Nodes.VoronoiTexture, input_kwargs={'Vector': mapping, 'Scale': 4.5000})
    
    voronoi_texture_1 = nw.new_node(Nodes.VoronoiTexture, input_kwargs={'Vector': mapping, 'Scale': 50.0000})
    
    mix = nw.new_node(Nodes.Mix,
        input_kwargs={6: voronoi_texture.outputs["Distance"], 7: voronoi_texture_1.outputs["Distance"]},
        attrs={'data_type': 'RGBA'})
    
    color_ramp = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': mix.outputs[2]})
    color_ramp.color_ramp.elements[0].position = 0.0000
    color_ramp.color_ramp.elements[0].color = [0.6418, 0.7974, 1.0000, 1.0000]
    color_ramp.color_ramp.elements[1].position = 1.0000
    color_ramp.color_ramp.elements[1].color = [1.0000, 1.0000, 1.0000, 1.0000]
    
    noise_texture = nw.new_node(Nodes.NoiseTexture, input_kwargs={'Vector': mapping})
    
    bump = nw.new_node('ShaderNodeBump', input_kwargs={'Strength': 0.1000, 'Height': color_ramp.outputs["Color"]})
    
    bump_1 = nw.new_node('ShaderNodeBump',
        input_kwargs={'Strength': 0.0875, 'Height': noise_texture.outputs["Fac"], 'Normal': bump})
    
    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF,
        input_kwargs={'Base Color': color_ramp.outputs["Color"], 'Roughness': 0.1000, 'Normal': bump_1})
    
    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

def geometry_nodes(nw: NodeWrangler, params):
    # Code generated using version 2.6.5 of the node_transpiler

    cone = nw.new_node('GeometryNodeMeshCone', input_kwargs={'Vertices': 150, 'Radius Bottom': 0.1500, 'Depth': 0.5900})
    
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
    
    middle_radius = nw.new_node(Nodes.Math,
        input_kwargs={0: reroute, 1: body_input.outputs["MiddleScale"]},
        label='MiddleRadius',
        attrs={'operation': 'MULTIPLY'})
    
    top_radius = nw.new_node(Nodes.Math,
        input_kwargs={0: reroute, 1: body_input.outputs["TopScale"]},
        label='TopRadius',
        attrs={'operation': 'MULTIPLY'})
    
    m_t_dist = nw.new_node(Nodes.Math, input_kwargs={0: middle_radius, 1: top_radius}, label='MTDist')
    
    m_t_scaled_dist = nw.new_node(Nodes.Math, input_kwargs={0: m_t_dist, 1: 0.8000}, label='MTScaledDist', attrs={'operation': 'MULTIPLY'})
    
    b_m_dist = nw.new_node(Nodes.Math, input_kwargs={0: middle_radius, 1: body_input.outputs["BottomRadius"]}, label='BMDist')
    
    b_m_scaled_dist = nw.new_node(Nodes.Math, input_kwargs={0: b_m_dist, 1: 0.8000}, label='BMScaledDist', attrs={'operation': 'MULTIPLY'})
    
    middle_z = nw.new_node(Nodes.Math, input_kwargs={0: b_m_scaled_dist, 1: body_input.outputs["BottomZ"]}, label='MiddleZ')
    
    top_z = nw.new_node(Nodes.Math, input_kwargs={0: m_t_scaled_dist, 1: middle_z}, label='TopZ')
    
    top_translation = nw.new_node(Nodes.CombineXYZ,
        input_kwargs={'X': body_input.outputs["BottomX"], 'Y': body_input.outputs["BottomY"], 'Z': top_z},
        label='TopTranslation')
    
    top_x_y_scale = nw.new_node(Nodes.Math, input_kwargs={0: top_radius, 1: 1.0000}, label='TopXYScale', attrs={'operation': 'MULTIPLY'})
    
    node_y_trans = nw.new_node(Nodes.Math,
        input_kwargs={0: top_x_y_scale, 1: -0.8000},
        label='NodeYTrans',
        attrs={'operation': 'MULTIPLY'})
    
    combine_xyz_10 = nw.new_node(Nodes.CombineXYZ, input_kwargs={'Y': node_y_trans})
    
    add = nw.new_node(Nodes.VectorMath, input_kwargs={0: top_translation, 1: combine_xyz_10})
    
    combine_xyz_6 = nw.new_node(Nodes.CombineXYZ, input_kwargs={'X': top_x_y_scale, 'Y': top_x_y_scale, 'Z': top_radius})
    
    multiply = nw.new_node(Nodes.VectorMath,
        input_kwargs={0: combine_xyz_6, 1: (1.0000, 1.0000, 1.0000)},
        attrs={'operation': 'MULTIPLY'})
    
    transform_geometry_2 = nw.new_node(Nodes.Transform,
        input_kwargs={'Geometry': cone.outputs["Mesh"], 'Translation': add.outputs["Vector"], 'Rotation': (1.5708, 0.0000, 0.0000), 'Scale': multiply.outputs["Vector"]})
    
    set_material_3 = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': transform_geometry_2, 'Material': surface.shaderfunc_to_material(shader_nose)})
    
    uv_sphere = nw.new_node(Nodes.MeshUVSphere, input_kwargs={'Segments': 64, 'Rings': 32, 'Radius': reroute})
    
    middle_translation = nw.new_node(Nodes.CombineXYZ,
        input_kwargs={'X': body_input.outputs["BottomX"], 'Y': body_input.outputs["BottomY"], 'Z': middle_z},
        label='MiddleTranslation')
    
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
    
    set_material = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': join_geometry, 'Material': surface.shaderfunc_to_material(shader_material_002)})
    
    join_geometry_1 = nw.new_node(Nodes.JoinGeometry, input_kwargs={'Geometry': [set_material_3, set_material]})
    
    uv_sphere_1 = nw.new_node(Nodes.MeshUVSphere, input_kwargs={'Segments': 274, 'Rings': 154, 'Radius': 0.1000})
    
    delta_x = nw.new_node(Nodes.Math, input_kwargs={0: -0.3600, 1: top_radius}, label='DeltaX', attrs={'operation': 'MULTIPLY'})
    
    delta_y = nw.new_node(Nodes.Math, input_kwargs={0: -0.9000, 1: top_radius}, label='DeltaY', attrs={'operation': 'MULTIPLY'})
    
    delta_z = nw.new_node(Nodes.Math, input_kwargs={0: 0.4000, 1: top_radius}, label='DeltaZ', attrs={'operation': 'MULTIPLY'})
    
    delta = nw.new_node(Nodes.CombineXYZ, input_kwargs={'X': delta_x, 'Y': delta_y, 'Z': delta_z}, label='Delta')
    
    delta2 = nw.new_node(Nodes.VectorMath,
        input_kwargs={0: delta, 1: (-1.0000, 1.0000, 1.0000)},
        label='Delta2',
        attrs={'operation': 'MULTIPLY'})
    
    trans2 = nw.new_node(Nodes.VectorMath, input_kwargs={0: top_translation, 1: delta2.outputs["Vector"]}, label='Trans2')
    
    scale = nw.new_node(Nodes.VectorMath,
        input_kwargs={0: combine_xyz_6, 1: (1.4000, 1.0000, 2.0000)},
        label='scale',
        attrs={'operation': 'MULTIPLY'})
    
    transform_geometry_4 = nw.new_node(Nodes.Transform,
        input_kwargs={'Geometry': uv_sphere_1.outputs["Mesh"], 'Translation': trans2.outputs["Vector"], 'Rotation': (-0.2112, 0.0279, 0.0000), 'Scale': scale.outputs["Vector"]})
    
    delta1 = nw.new_node(Nodes.VectorMath,
        input_kwargs={0: delta, 1: (1.0000, 1.0000, 1.0000)},
        label='Delta1',
        attrs={'operation': 'MULTIPLY'})
    
    trans1 = nw.new_node(Nodes.VectorMath, input_kwargs={0: delta1.outputs["Vector"], 1: top_translation}, label='Trans1')
    
    transform_geometry_3 = nw.new_node(Nodes.Transform,
        input_kwargs={'Geometry': uv_sphere_1.outputs["Mesh"], 'Translation': trans1.outputs["Vector"], 'Rotation': (-0.2112, -0.0279, 0.0000), 'Scale': scale.outputs["Vector"]})
    
    join_geometry_5 = nw.new_node(Nodes.JoinGeometry, input_kwargs={'Geometry': [transform_geometry_4, transform_geometry_3]})
    
    set_material_2 = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': join_geometry_5, 'Material': surface.shaderfunc_to_material(shader_eyes)})
    
    join_geometry_2 = nw.new_node(Nodes.JoinGeometry, input_kwargs={'Geometry': [join_geometry_1, set_material_2]})
    
    cube = nw.new_node(Nodes.MeshCube, input_kwargs={'Size': (1.9500, 0.1000, 0.1000)})
    
    value = nw.new_node(Nodes.Value)
    value.outputs[0].default_value = 0.4000
    
    combine_xyz = nw.new_node(Nodes.CombineXYZ, input_kwargs={'Y': value})
    
    transform_geometry_5 = nw.new_node(Nodes.Transform,
        input_kwargs={'Geometry': cube.outputs["Mesh"], 'Translation': middle_translation, 'Rotation': combine_xyz})
    
    multiply_1 = nw.new_node(Nodes.Math, input_kwargs={0: value, 1: -1.0000}, attrs={'operation': 'MULTIPLY'})
    
    combine_xyz_1 = nw.new_node(Nodes.CombineXYZ, input_kwargs={'Y': multiply_1})
    
    transform_geometry_6 = nw.new_node(Nodes.Transform,
        input_kwargs={'Geometry': cube.outputs["Mesh"], 'Translation': middle_translation, 'Rotation': combine_xyz_1})
    
    join_geometry_6 = nw.new_node(Nodes.JoinGeometry, input_kwargs={'Geometry': [transform_geometry_5, transform_geometry_6]})
    
    set_material_1 = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': join_geometry_6, 'Material': surface.shaderfunc_to_material(shader_arms)})
    
    join_geometry_3 = nw.new_node(Nodes.JoinGeometry, input_kwargs={'Geometry': [join_geometry_2, set_material_1]})
    
    cylinder = nw.new_node('GeometryNodeMeshCylinder',
        input_kwargs={'Vertices': 152, 'Side Segments': 40, 'Radius': 0.3000, 'Depth': 0.6000})
    
    hat_z = nw.new_node(Nodes.Math, input_kwargs={0: top_radius, 1: top_z}, label='HatZ')
    
    hat_top_z = nw.new_node(Nodes.Math, input_kwargs={0: hat_z, 1: 0.2000}, label='HatTopZ')
    
    hat_top_trans = nw.new_node(Nodes.CombineXYZ,
        input_kwargs={'X': body_input.outputs["BottomX"], 'Y': body_input.outputs["BottomY"], 'Z': hat_top_z},
        label='HatTopTrans')
    
    transform_geometry_7 = nw.new_node(Nodes.Transform, input_kwargs={'Geometry': cylinder.outputs["Mesh"], 'Translation': hat_top_trans})
    
    hat_bottom_z = nw.new_node(Nodes.Math, input_kwargs={0: hat_z, 1: -0.1000}, label='HatBottomZ')
    
    hat_bottom_trans = nw.new_node(Nodes.CombineXYZ,
        input_kwargs={'X': body_input.outputs["BottomX"], 'Y': body_input.outputs["BottomY"], 'Z': hat_bottom_z},
        label='HatBottomTrans')
    
    transform_geometry_8 = nw.new_node(Nodes.Transform,
        input_kwargs={'Geometry': cylinder.outputs["Mesh"], 'Translation': hat_bottom_trans, 'Scale': (1.5000, 1.5000, 0.1000)})
    
    join_geometry_7 = nw.new_node(Nodes.JoinGeometry, input_kwargs={'Geometry': [transform_geometry_7, transform_geometry_8]})
    
    set_material_4 = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': join_geometry_7, 'Material': surface.shaderfunc_to_material(shader_hat)})
    
    join_geometry_4 = nw.new_node(Nodes.JoinGeometry, input_kwargs={'Geometry': [join_geometry_3, set_material_4]})
    
    group_output = nw.new_node(Nodes.GroupOutput, input_kwargs={'Geometry': join_geometry_4}, attrs={'is_active_output': True})


def apply(obj, params, selection=None, **kwargs):
    surface.add_geomod(obj, geometry_nodes, selection=selection, attributes=[], input_kwargs={'params': params})
    surface.add_material(obj, shader_material_002, selection=selection)


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
