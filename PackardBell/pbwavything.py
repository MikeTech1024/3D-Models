# This script generates the 'wavy' pattern profile of the side cladding found on mid-1990s Packard Bell computers.
# The wavy pattern is the 'killer app' here, as the parameters below can be modified to re-create the cladding 
# found on the tower versions of this family of systems.
# -Mike

import FreeCAD as App
import Part
import math

doc = App.activeDocument() or App.newDocument("PBWavyCladding")

# Main size and wave parameters
total_length = 42.75      # Total profile length
total_max_height = 5.5    # Height of highest wave 'peak'
amplitude = 0.6           # mm (Peak-to-peak = 1.2mm)
num_cycles = 4.0          # 4 complete peaks uniform across the top surface
wavelength = total_length / num_cycles  # Size of the wave I guess...
wave_mean_y = total_max_height - amplitude  # Try to find the wave 'center'

# Define the 'Step'
step_x = 34.0             # X position where the bottom step begins
step_height = 3.3         # Height of the bottom step cut-out

# Use fancy science math to generate the wavy part
pts_wave = []
num_pts = 80

for i in range(num_pts + 1):
    x = total_length * (i / num_pts)
    y = wave_mean_y + amplitude * math.sin((2 * math.pi / wavelength) * x - (math.pi / 2))
    pts_wave.append(App.Vector(x, y, 0))

# Interpolate points into a single continuous B-Spline curve
spline = Part.BSplineCurve()
spline.interpolate(pts_wave)
wave_edge = Part.Edge(spline)

# Drawing with code...
p_top_right  = pts_wave[-1]
p_bot_right  = App.Vector(total_length, step_height, 0)
p_step_inner = App.Vector(step_x, step_height, 0)
p_step_down  = App.Vector(step_x, 0, 0)
p_bot_left   = App.Vector(0, 0, 0)
p_top_left   = pts_wave[0]

right_v_edge  = Part.makeLine(p_top_right, p_bot_right)
step_h_edge   = Part.makeLine(p_bot_right, p_step_inner)
step_v_edge   = Part.makeLine(p_step_inner, p_step_down)
bot_main_edge = Part.makeLine(p_step_down, p_bot_left)
left_v_edge   = Part.makeLine(p_bot_left, p_top_left)

# Bring it all together...
profile_wire = Part.Wire([
    wave_edge, right_v_edge, step_h_edge, 
    step_v_edge, bot_main_edge, left_v_edge
])

profile_face = Part.Face(profile_wire)

# Put it in FreeCAD finally
obj = doc.addObject("Part::Feature", "PBWavyCladding")
obj.Shape = profile_face
doc.recompute()
