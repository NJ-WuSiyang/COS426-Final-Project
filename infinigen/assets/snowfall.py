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



def shader_snow(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF)
    
    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})

def shader_material_002(nw: NodeWrangler):
    # Code generated using version 2.6.5 of the node_transpiler

    texture_coordinate = nw.new_node(Nodes.TextureCoord)
    
    mapping = nw.new_node(Nodes.Mapping, input_kwargs={'Vector': texture_coordinate.outputs["Object"]})
    
    voronoi_texture = nw.new_node(Nodes.VoronoiTexture, input_kwargs={'Vector': mapping, 'Scale': 27.7000})
    
    voronoi_texture_1 = nw.new_node(Nodes.VoronoiTexture, input_kwargs={'Vector': mapping, 'Scale': 200.0000})
    
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
        input_kwargs={'Base Color': color_ramp.outputs["Color"], 'Subsurface': 1.0000, 'Subsurface Radius': (0.2000, 0.2000, 0.2000), 'Roughness': 0.1000, 'Normal': bump_1})
    
    translucent_bsdf = nw.new_node(Nodes.TranslucentBSDF, input_kwargs={'Color': color_ramp.outputs["Color"]})
    
    mix_shader = nw.new_node(Nodes.MixShader, input_kwargs={'Fac': 0.2250, 1: principled_bsdf, 2: translucent_bsdf})
    
    rgb = nw.new_node(Nodes.RGB)
    rgb.outputs[0].default_value = (0.7835, 0.9568, 1.0000, 1.0000)
    
    # volume_absorption = nw.new_node('ShaderNodeVolumeAbsorption', input_kwargs={'Color': rgb, 'Density': 5.6000})
    
    material_output = nw.new_node(Nodes.MaterialOutput,
        # input_kwargs={'Surface': mix_shader, 'Volume': volume_absorption},
        input_kwargs={'Surface': mix_shader},

        attrs={'is_active_output': True})

def geometry_nodes(nw: NodeWrangler, params):
    # Code generated using version 2.6.5 of the node_transpiler

    grid = nw.new_node(Nodes.MeshGrid, input_kwargs={'Size X': 3.0000, 'Size Y': 3.0000})
    
    distribute_points_on_faces = nw.new_node(Nodes.DistributePointsOnFaces, input_kwargs={'Mesh': grid.outputs["Mesh"], 'Density': params['density']})
    
    ico_sphere = nw.new_node(Nodes.MeshIcoSphere, input_kwargs={'Radius':params['radius'] })
    
    instance_on_points = nw.new_node(Nodes.InstanceOnPoints,
        input_kwargs={'Points': distribute_points_on_faces.outputs["Points"], 'Instance': ico_sphere.outputs["Mesh"]})
    
    set_material_1 = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': instance_on_points, 'Material': surface.shaderfunc_to_material(shader_material_002)})
    
    f_r_a_m_e_s = nw.new_node(Nodes.Value, label='FRAMES')
    f_r_a_m_e_s.outputs[0].default_value = 201.0000
    driver = f_r_a_m_e_s.outputs[0].driver_add("default_value")
    driver.driver.expression = 'frame'
    bpy.context.view_layer.update()
    
    index = nw.new_node(Nodes.Index)
    
    random_value = nw.new_node(Nodes.RandomValue, input_kwargs={5: 800, 'ID': index}, attrs={'data_type': 'INT'})
    
    subtract = nw.new_node(Nodes.Math, input_kwargs={0: f_r_a_m_e_s, 1: random_value.outputs[2]}, attrs={'operation': 'SUBTRACT'})
    
    divide = nw.new_node(Nodes.Math, input_kwargs={0: subtract, 1: -200.0000}, attrs={'operation': 'DIVIDE'})
    
    combine_xyz = nw.new_node(Nodes.CombineXYZ, input_kwargs={'Z': divide})
    
    set_position = nw.new_node(Nodes.SetPosition, input_kwargs={'Geometry': set_material_1, 'Offset': combine_xyz})
    
    subdivision_surface = nw.new_node(Nodes.SubdivisionSurface, input_kwargs={'Mesh': set_position, 'Vertex Crease': 0.1615})
    
    divide_1 = nw.new_node(Nodes.Math, input_kwargs={0: f_r_a_m_e_s, 1: 10.0000}, attrs={'operation': 'DIVIDE'})
    
    random_value_2 = nw.new_node(Nodes.RandomValue, input_kwargs={3: 1.5000})
    
    multiply = nw.new_node(Nodes.Math, input_kwargs={0: divide_1, 1: random_value_2.outputs[1]}, attrs={'operation': 'MULTIPLY'})
    
    combine_xyz_1 = nw.new_node(Nodes.CombineXYZ, input_kwargs={'Z': multiply})
    
    value_1 = nw.new_node(Nodes.Value)
    value_1.outputs[0].default_value = 0.0500
    
    multiply_1 = nw.new_node(Nodes.Math, input_kwargs={0: value_1, 1: -1.0000}, attrs={'operation': 'MULTIPLY'})
    
    random_value_1 = nw.new_node(Nodes.RandomValue, input_kwargs={0: multiply_1, 1: value_1}, attrs={'data_type': 'FLOAT_VECTOR'})
    
    rotate_instances = nw.new_node(Nodes.RotateInstances,
        input_kwargs={'Instances': subdivision_surface, 'Rotation': combine_xyz_1, 'Pivot Point': random_value_1.outputs["Value"]})
    
    set_material = nw.new_node(Nodes.SetMaterial,
        input_kwargs={'Geometry': rotate_instances, 'Material': surface.shaderfunc_to_material(shader_snow)})
    
    group_output = nw.new_node(Nodes.GroupOutput, input_kwargs={'Geometry': set_material}, attrs={'is_active_output': True})


def apply(obj, params, selection=None, **kwargs):
    surface.add_geomod(obj, geometry_nodes, selection=selection, attributes=[], input_kwargs={'params': params})
    surface.add_material(obj, shader_material_002, selection=selection)
    


class Snowfall(AssetFactory):

    def __init__(self, factory_seed, name='snowfall', trans=np.array([0, 0, 0]), rot=np.array([0, 0, 0]), scale=np.array([1, 1, 1]), density = 10.0, radius = 0.0001):
        super().__init__(factory_seed)
        self._name = name
        self._trans = trans.copy()
        self._rot = rot.copy()
        self._scale = scale.copy()
        self.params = {
            'density': density,
            'radius' : radius
        }

    def create_asset(self, **kwargs):
        obj = butil.spawn_vert(self._name) # dummy empty object to apply on
        apply(obj, self.params)
        for i in range(3):
            obj.location[i] = self._trans[i]
        for i in range(3):
            obj.rotation_euler[i] = self._rot[i]
        for i in range(3):
            obj.scale[i] = self._scale[i]
        return obj