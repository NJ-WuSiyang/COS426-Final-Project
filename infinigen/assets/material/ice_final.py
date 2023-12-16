import bpy
import bpy
import mathutils
from numpy.random import uniform, normal, randint
from infinigen.core.nodes.node_wrangler import Nodes, NodeWrangler
from infinigen.core.nodes import node_utils
from infinigen.core.util.color import color_category
from infinigen.core import surface



def shader_ice_final(nw: NodeWrangler, params):
    # Code generated using version 2.6.5 of the node_transpiler

    texture_coordinate = nw.new_node(Nodes.TextureCoord)
    
    noise_texture_3 = nw.new_node(Nodes.NoiseTexture,
        input_kwargs={'Vector': texture_coordinate.outputs["Object"], 'Detail': 15.0000, 'Roughness': 0.3583})
    
    color_ramp_1 = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': noise_texture_3.outputs["Fac"]})
    color_ramp_1.color_ramp.elements[0].position = 0.0000
    color_ramp_1.color_ramp.elements[0].color = [0.1580, 0.3596, 0.9650, 1.0000]
    color_ramp_1.color_ramp.elements[1].position = 0.2636
    color_ramp_1.color_ramp.elements[1].color = [1.0000, 1.0000, 1.0000, 1.0000]
    
    noise_texture_2 = nw.new_node(Nodes.NoiseTexture,
        input_kwargs={'Vector': texture_coordinate.outputs["Object"], 'Scale': 90.2000, 'Detail': 15.0000, 'Roughness': 0.3292})
    
    mix_1 = nw.new_node(Nodes.Mix,
        input_kwargs={0: 0.8000, 7: noise_texture_2.outputs["Color"]},
        attrs={'blend_type': 'LINEAR_LIGHT', 'data_type': 'RGBA'})
    
    voronoi_texture_2 = nw.new_node(Nodes.VoronoiTexture,
        input_kwargs={'Vector': mix_1.outputs[2], 'Scale': params['ice_param']},
        attrs={'feature': 'DISTANCE_TO_EDGE'})
    
    mapping = nw.new_node(Nodes.Mapping, input_kwargs={'Vector': texture_coordinate.outputs["Object"]})
    
    voronoi_texture = nw.new_node(Nodes.VoronoiTexture, input_kwargs={'Vector': mapping, 'Scale': 2.1000})
    
    voronoi_texture_1 = nw.new_node(Nodes.VoronoiTexture, input_kwargs={'Vector': mapping, 'Scale': -2.4000})
    
    mix = nw.new_node(Nodes.Mix,
        input_kwargs={6: voronoi_texture.outputs["Distance"], 7: voronoi_texture_1.outputs["Distance"]},
        attrs={'data_type': 'RGBA'})
    
    color_ramp = nw.new_node(Nodes.ColorRamp, input_kwargs={'Fac': mix.outputs[2]})
    color_ramp.color_ramp.elements[0].position = 0.6114
    color_ramp.color_ramp.elements[0].color = [0.5456, 0.8622, 1.0000, 1.0000]
    color_ramp.color_ramp.elements[1].position = 1.0000
    color_ramp.color_ramp.elements[1].color = [1.0000, 1.0000, 1.0000, 1.0000]
    
    mix_2 = nw.new_node(Nodes.Mix,
        input_kwargs={0: color_ramp_1.outputs["Color"], 6: voronoi_texture_2.outputs["Distance"], 7: color_ramp.outputs["Color"]},
        attrs={'clamp_factor': False, 'data_type': 'RGBA'})
    
    noise_texture_1 = nw.new_node(Nodes.NoiseTexture, input_kwargs={'Vector': mapping, 'Scale': 170.0000})
    
    bump_2 = nw.new_node('ShaderNodeBump',
        input_kwargs={'Strength': 0.1125, 'Height': noise_texture_1.outputs["Fac"], 'Normal': color_ramp.outputs["Color"]})
    
    principled_bsdf = nw.new_node(Nodes.PrincipledBSDF,
        input_kwargs={'Base Color': mix_2.outputs[2], 'Roughness': 0.1000, 'Normal': bump_2})
    
    translucent_bsdf = nw.new_node(Nodes.TranslucentBSDF, input_kwargs={'Color': color_ramp.outputs["Color"]})
    
    mix_shader = nw.new_node(Nodes.MixShader, input_kwargs={1: principled_bsdf, 2: translucent_bsdf})
    
    material_output = nw.new_node(Nodes.MaterialOutput, input_kwargs={'Surface': mix_shader}, attrs={'is_active_output': True})
    return mix_shader



def apply(obj, selection=None, **kwargs):
    surface.add_material(obj, shader_ice_final, selection=selection)