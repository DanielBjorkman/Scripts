


directory = '//cern.ch/dfs/Users/c/cbjorkma/Documents'
filename = 'Problem2Bias.new.inp'

Envfilename = 'Env' + filename

import os
os.chdir(directory)

from shutil import copyfile
copyfile(filename, Envfilename)

info = {'Geobegin':[],'end1':[],'end2':[],'newline':[],'position':[], 'BLCKHOLE':[]}


row = 0
with open(filename) as file:
     for line in file.readlines():
         line_content = line.split()
         if row ==107:
            a = 0
         if line.lstrip(' ').partition(' ')[0] == 'GEOBEGIN':
             info['Geobegin'].append(row)
         if line.lstrip(' ').partition(' ')[0] == 'END\n':
             if len(info['end1']) == 0:
                info['end1'].append(row)
             else:
                info['end2'].append(row)
         if line.lstrip(' ').partition(' ')[0] == 'ASSIGNMA' and line_content[1] == 'BLCKHOLE' :
            info['BLCKHOLE'].append(line_content[2])
         row = row +1

#print(info['Geobegin'][0])
#print(info['end1'][0])
#print(info['end2'][0])

String = '+Envelope '
negString = '-Envelope '

EnvelopeBody = 'RPP Envelope   -100.00 100.00 -100.00 100.00 -100.00 100.00'


#Overwrites all relevant lines
row = 0
with open(filename) as file, open(Envfilename, 'w') as output_file:
     for line in file.readlines():
         row = row + 1
         if row <= info['end1'][0] or row > info['end2'][0]:
            output_file.write(line)
 #        if row == info['Geobegin'][0]+2:
  #          output_file.insert(EnvelopeBody)
         #Regions
         if row > info['end1'][0] +1 and row <= info['end2'][0] :
            line_content = line.split()
            if line_content[0] != '*':
                if line_content[0] != info['BLCKHOLE'][0]:
                    info['newline'].append(line[:15] + String + line[15:])
                    info['position'].append(row)
                    output_file.write(line[:15] + String + line[15:])
                else:
                    info['newline'].append(line[:15] + negString + line[15:])
                    info['position'].append(row)
                    output_file.write(line[:15] + negString + '\n')
            else:
                output_file.write(line)


#f = open(Envfilename,"r+")
#lines = f.readlines()
#lines.insert(info['Geobegin'][0]+2,EnvelopeBody)
#f.close()

with open(Envfilename, 'r+') as output:
    output.seek(40,0)
    output.write(EnvelopeBody)

    #info['Geobegin'][0]+2
a = 0
#with open(Envfilename) as file, open(Envfilename, 'w') as output:
 #   output.insert(EnvelopeBody)
    
    #for line in file.readlines():
     #   if row == info['Geobegin'][0]+2:
      #      output_file.write(EnvelopeBody)         
       # else:
        #    output_file.write(line)

   
   # for line in file.readlines():
    #     if row == info['Geobegin'][0]+2:
     #            output_file.write(EnvelopeBody)
      #   row = row + 1

#f = open("Envfilename", "r")
#contents = f.readlines()
#f.close()

#contents.insert(info['Geobegin'][0]+2, EnvelopeBody)

#f = open("path_to_file", "w")
#contents = "".join(contents)
#f.write(contents)
#f.close()


#for r in range(0,len(info['position'])):
 #   row = 0
  #  if row == 66:
   #     a = 0
    #with open(filename, 'r') as input_file, open(Envfilename, 'w') as output_file:
     #   for line in input_file:
      #      if info['position'][r] == row:
       #         output_file.write(info['newline'][r] + '\n')
        #    else:
         #       output_file.write(line)
        #row = row +1 
