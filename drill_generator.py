input_file = "tube-tester"

drill_in = open(input_file + ".drd",'r')
code_out = input_file + "-drill.tap"
drill_out = open(code_out,'w')
feed_rate = "500"

drill_out.write("G71 G90" + "\n") #metric, absolute coord
drill_out.write("F" + feed_rate + "\n")
drill_out.write("G0 Z5" + "\n")

drill_in.readline()



for line in drill_in:
   x_start = line.find('X')
   y_start = line.find('Y')
   tool_set = line.find('T') 

   if tool_set == 0:
       drill_out.write("G0 Z20" + "\n")
       drill_out.write("M6" + "  (" + line[:-2] + ")" + "\n")
   elif x_start > -1:
      x_pos = line[x_start+1:y_start]
      y_pos = line[y_start+1:]
      drill_out.write("G0 X" + x_pos[:-3] + "." + x_pos[-3:] + " Y" + y_pos[:-4] + "." + y_pos[-4:-1] + "\n")
      drill_out.write("M98 P00001" + "\n")

drill_out.write("M30" + "\n")      
drill_out.write("O00001" + "\n")
drill_out.write("G1 Z-2" + "\n")
drill_out.write("G4 P0.1" + "\n")
drill_out.write("G0 Z5" + "\n")
drill_out.write("M99" + "\n")

drill_in.close()
drill_out.close()

   