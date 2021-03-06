input_file = "tube-tester"

drill_in = open(input_file + ".drd",'r')
mill_in = open(input_file + ".mil",'r')
code_out = "./tap/" + input_file + "-drill-mill.tap"
tap_out = open(code_out,'w')
feed_rate = "500"
mill_feed = "100"
drill_list = {}

tap_out.write("(Project " + input_file + " )\n")
tap_out.write("(generated by iStivi python script drill+mill_genarator.py)\n")
tap_out.write("G71 G90" + "\n") #metric, absolute coord

line = drill_in.readline()
line = drill_in.readline()
while line != "%\n":
   m_find = line.find('M')
   tool_find = line.find('T')
   print(line)
   if m_find >= 0:
      print("command")
   if tool_find >= 0:
      tool_name = line[:3]
      tool_size = line[-7:-1]
      drill_list[tool_name] = tool_size
      tap_out.write("( " + tool_name + " : " + tool_size + " )\n")
   line = drill_in.readline()
   
tap_out.write("F" + feed_rate + "\n")
tap_out.write("G0 Z5" + "\n")


for line in drill_in:
   x_start = line.find('X')
   y_start = line.find('Y')
   tool_set = line.find('T') 

   if tool_set == 0:
       tap_out.write("G0 Z20" + "\n")
       tap_out.write(line[:-1] + " M6 (" + drill_list[line[:-1]] + ")" + "\n")
   elif x_start > -1:
      x_pos = line[x_start+1:y_start]
      y_pos = line[y_start+1:]
      tap_out.write("G0 X" + x_pos[:-3] + "." + x_pos[-3:] + " Y" + y_pos[:-4] + "." + y_pos[-4:-1] + "\n")
      tap_out.write("G1 Z-2" + "\n")
      tap_out.write("G4 P0.1" + "\n")
      tap_out.write("G0 Z2" + "\n")

drill_in.close()

tap_out.write("(start milling routine)\n")
tap_out.write("F" + mill_feed + "\n")
tap_out.write("T201 M6 (1mm mill)\n")

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
          tap_out.write(z_height + " X" + x_cut_start + " Y" + y_cut_start + "\n")
      elif move_type == "D01":
         x_cut_end = x_pos[:-3] + "." + x_pos[-3:]
         y_cut_end = y_pos[:-3] + "." + y_pos[-3:]
         tap_out.write("G1 Z-0.5\n")
         tap_out.write("G1 X" + x_cut_end + " Y" + y_cut_end + "\n")
         tap_out.write("G1 Z1\n")
         tap_out.write("G0 X" + x_cut_start + " Y" + y_cut_start + "\n")
         tap_out.write("G1 Z-1\n")
         tap_out.write("G1 X" + x_cut_end + " Y" + y_cut_end + "\n")
         tap_out.write("G1 Z1\n")
         tap_out.write("G0 X" + x_cut_start + " Y" + y_cut_start + "\n")
         tap_out.write("G1 Z-1.5\n")
         tap_out.write("G1 X" + x_cut_end + " Y" + y_cut_end + "\n")
         tap_out.write("G1 Z1\n")
         tap_out.write("G0 Z1 X" + x_cut_start + " Y" + y_cut_start + "\n")
         tap_out.write("G1 Z-2\n")
         tap_out.write("G1 X" + x_cut_end + " Y" + y_cut_end + "\n")
         tap_out.write("G0 Z5\n")
         
tap_out.write("M30" + "\n")      

mill_in.close()
tap_out.close()

   
