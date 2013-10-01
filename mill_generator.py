input_file = "180V_power"

mill_in = open(input_file + ".mil",'r')
code_out = input_file + "-mill.txt"
mill_out = open(code_out,'w')
feed_rate = "300"

mill_out.write("G71 G90" + "\n") #metric, absolute coord
mill_out.write("F" + feed_rate + "\n")
mill_out.write("M6 (1mm mill)\n")

for line in mill_in:
   x_start = line.find('X')
   y_start = line.find('Y')
   mill_start = line.find('D') 

   if x_start != -1:
      x_pos = line[x_start+1:y_start]
      y_pos = line[y_start+1:mill_start]
      move_type = line[mill_start:mill_start+3]
      if move_type == "D02":
          z_height = "G0 Z5"
          x_cut_start = x_pos[:-3] + "." + x_pos[-3:]
          y_cut_start = y_pos[:-3] + "." + y_pos[-3:]
          mill_out.write(z_height + " X" + x_cut_start + " Y" + y_cut_start + "\n")
      elif move_type == "D01":
         x_cut_end = x_pos[:-3] + "." + x_pos[-3:]
         y_cut_end = y_pos[:-3] + "." + y_pos[-3:]
         mill_out.write("G1 Z-0.5 X" + x_cut_end + " Y" + y_cut_end + "\n")
         mill_out.write("G0 Z1 X" + x_cut_start + " Y" + y_cut_start + "\n")
         mill_out.write("G1 Z-1 X" + x_cut_end + " Y" + y_cut_end + "\n")
         mill_out.write("G0 Z1 X" + x_cut_start + " Y" + y_cut_start + "\n")
         mill_out.write("G1 Z-1.5 X" + x_cut_end + " Y" + y_cut_end + "\n")
         mill_out.write("G0 Z1 X" + x_cut_start + " Y" + y_cut_start + "\n")
         mill_out.write("G1 Z-2 X" + x_cut_end + " Y" + y_cut_end + "\n")
         mill_out.write("G0 Z5\n")

mill_out.write("M30")
mill_in.close()
mill_out.close()

   
