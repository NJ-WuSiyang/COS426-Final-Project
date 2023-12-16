import bpy
import bpy
import mathutils
from numpy.random import uniform, normal, randint
from infinigen.core.nodes.node_wrangler import Nodes, NodeWrangler
from infinigen.core.nodes import node_utils
from infinigen.core.util.color import color_category
from infinigen.core import surface



def shader_snow_terrain(nw: NodeWrangler, params):
    # Code generated using version 2.6.5 of the node_transpiler

    texture_coordinate = nw.new_node(Nodes.TextureCoord)
    
    noise_texture_3 = nw.new_node(Nodes.NoiseTexture,
        input_kwargs={'Vector': texture_coordinate.outputs["Object"], 'Detail': 15.0000, 'Roughness': 0.3583})
    
    color_ramp_1 = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': noise_texture_3.outputs["Fac"]})
    color_ramp_1.color_ramp.elements[0].position = params['position']
    color_ramp_1.color_ramp.elements[0].color = [0.1580, 0.3596, 0.9650, 1.0000]
    color_ramp_1.color_ramp.elements[1].position = 0.2636
    color_ramp_1.color_ramp.elements[1].color = [1.0000, 1.0000, 1.0000, 1.0000]
    
    noise_texture_2 = nw.new_node(Nodes.NoiseTexture,
        input_kwargs={'Vector': texture_coordinate.outputs["Object"], 'Scale': 90.2000, 'Detail': 15.0000, 'Roughness': 0.3292})
    
    mix_1 = nw.new_node(Nodes.Mix,
        input_kwargs={0: 0.8000, 7: noise_texture_2.outputs["Color"]},
        attrs={'blend_type': 'LINEAR_LIGHT', 'data_type': 'RGBA'})
    
    voronoi_texture_2 = nw.new_node(Nodes.VoronoiTexture,
        input_kwargs={'Vector': mix_1.outputs[2], 'Scale': 40.0000},
        attrs={'feature': 'DISTANCE_TO_EDGE'})
    
    mapping = nw.new_node(Nodes.Mapping, input_kwargs={'Vector': texture_coordinate.outputs["Object"]})
    
    voronoi_texture = nw.new_node(Nodes.VoronoiTexture, input_kwargs={'Vector': mapping, 'Scale': 4.5000})
    
    voronoi_texture_1 = nw.new_node(Nodes.VoronoiTexture, input_kwargs={'Vector': mapping, 'Scale': 50.0000})
    
    mix = nw.new_node(Nodes.Mix,
        input_kwargs={6: voronoi_texture.outputs["Distance"], 7: voronoi_texture_1.outputs["Distance"]},
        attrs={'data_type': 'RGBA'})
    
    color_ramp = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': mix.outputs[2]})
    color_ramp.color_ramp.elements[0].position = 0.0000
    color_ramp.color_ramp.elements[0].color = [0.6418, 0.7974, 1.0000, 1.0000]
    color_ramp.color_ramp.elements[1].position = 0.6136
    color_ramp.color_ramp.elements[1].color = [1.0000, 1.0000, 1.0000, 1.0000]
    
    mix_2 = nw.new_node(Nodes.Mix,
        input_kwargs={0: color_ramp_1.outputs["Color"], 6: voronoi_texture_2.outputs["Distance"], 7: color_ramp.outputs["Color"]},
        attrs={'clamp_factor': False, 'data_type': 'RGBA'})
    
    noise_texture_1 = nw.new_node(Nodes.NoiseTexture, input_kwargs={'Vector': mapping, 'Scale': params['scale']})
    
    bump_2 = nw.new_node('ShaderNodeBump',
        input_kwargs={'Strength': 0.3250, 'Height': noise_texture_1.outputs["Fac"], 'Normal': color_ramp.outputs["Alpha"]})
    
    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF,
        input_kwargs={'Base Color': mix_2.outputs[2], 'Roughness': 1.0000, 'Clearcoat Roughness': 0.0800, 'Normal': bump_2})
    
    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': principled_bsdf}, attrs={'is_active_output': True})
    return principled_bsdf



def apply(obj, selection=None, **kwargs):
    surface.add_material(obj, shader_snow_terrain, selection=selection)