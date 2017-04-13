
# Python function for parsing FLUKA ASCII formatted USRBIN into 3D Matrix called cube
# 
# call: cube = Flukato3dMatrix(filename, directory,1)
# np.save('filename', cube)
# #np.load('filename.npy')
# Input file needs to be in ASCII format
# Output cube is 3D matrix numpy array
# The last input value can be set to 0 if no plotting of the cubes are desired
#
# Required python libraries: Numpy, Matplotlib
#
# Developed by Daniel Bjorkman at CERN 2016
# daniel.bjorkman@cern.ch
def Flukato3dMatrix(filename, directory,plot):

    import os
    import time

    startTime = time.time()
    os.chdir(directory)

    RPZ = 0
    RZ = 0
    CAR = 0
    row = 0

    #Predefine information into info directory and find starting position
    with open(filename) as file:
        for line in file.readlines():
            line_content = line.split()
            row = row + 1
            if len(line_content) > 5:
                if line_content[5] == 'A(ir,ip,iz),':
                    info = {'rbin':[],'zbin':[],'pbin':[], 'rmin':[],'rmax':[], 'zmin':[],'zmax':[], 'rwidth':[], 'zwidth':[],'prad':[]}
                    RPZ = 1
                    print('R-Phi-Z binning detected')
                if line_content[5] == 'A(ix,iy,iz),':
                    info = {'xbin':[], 'ybin':[],'zbin':[], 'xmin':[],'xmax':[], 'ymin':[],'ymax':[], 'zmin':[],'zmax':[], 'xwidth':[], 'ywidth':[], 'zwidth':[]}
                    CAR = 1
                    print('Cartesian binning detected')
                if line_content[5] == 'A(ir,iz),':
                    info = {'rbin':[],'zbin':[],'pbin':[], 'rmin':[],'rmax':[], 'zmin':[],'zmax':[], 'rwidth':[], 'zwidth':[],'prad':[]}
                    info['pbin'].append(float(1))
                    RZ = 1
                    print('R-Z binning detected')
                try:
                    a = float(line_content[0])
                    if isinstance(a, float) and len(line_content) > 1:
                        start = row
                        break
                except Exception as e:
                    pass

    #Return if file is of wrong format
    if not (RPZ or RZ or CAR):
        print("Unable to read file")
        return

    #Extract dimensional information
    if RPZ or RZ:
        with open(filename) as file:
            for line in file.readlines():
                line_content = line.split()
                if line.lstrip(' ').partition(' ')[0] == 'R':
                    if line_content[1] != '-':
                        info['rbin'].append(float(line_content[7]))
                        info['rmin'].append(float(line_content[3]))
                        info['rmax'].append(float(line_content[5]))
                        info['rwidth'].append(float(line_content[10]))
                if line.lstrip(' ').partition(' ')[0] == 'Z':
                    info['zbin'].append(float(line_content[7]))
                    info['zmin'].append(float(line_content[3]))
                    info['zmax'].append(float(line_content[5]))
                    info['zwidth'].append(float(line_content[10]))
                if line.lstrip(' ').partition(' ')[0] == 'P':
                    info['pbin'].append(float(line_content[7]))
                    info['prad'].append(float(line_content[10]))
    elif CAR:
         with open(filename) as file:
            for line in file.readlines():
                 line_content = line.split()
                 if line.lstrip(' ').partition(' ')[0] == 'X':
                     info['xbin'].append(float(line_content[7]))
                     info['xmin'].append(float(line_content[3]))
                     info['xmax'].append(float(line_content[5]))
                     info['xwidth'].append(float(line_content[10]))
                 if line.lstrip(' ').partition(' ')[0] == 'Y':
                     info['ybin'].append(float(line_content[7]))
                     info['ymin'].append(float(line_content[3]))
                     info['ymax'].append(float(line_content[5]))
                     info['ywidth'].append(float(line_content[10]))
                 if line.lstrip(' ').partition(' ')[0] == 'Z':
                     info['zbin'].append(float(line_content[7]))
                     info['zmin'].append(float(line_content[3]))
                     info['zmax'].append(float(line_content[5]))
                     info['zwidth'].append(float(line_content[10]))

    if (RZ or RPZ) and not info['rmin'][0] == 0 :
        print("Function currently not defined for minimum rbins other than 0")
        return;

    #Reads in all elements horisontally and puts them into list
    list = []
    row = 0
    with open(filename) as file:
        for line in file.readlines():
            row = row + 1
            if row >= start:
                line_content = line.split()
                if not line_content:
                    break 
                for i in range(0,10):
                    list.append(float(line_content[i]))
    if RPZ or RZ: 
        print(str(len(list)) + " elements read out of " + str(int(info['zbin'][0] * info['rbin'][0] * info['pbin'][0])) + " from file.")
    else:
        print(str(len(list)) + " elements read out of " + str(int(info['zbin'][0] * info['xbin'][0] * info['ybin'][0])) + " from file.")
       

    import math
    import numpy as np

    #Cube reconstruction from list
    print("Reconstructing 3D cube...")
    if RPZ:
        cube = np.zeros((int(info['rbin'][0]) * 2,int(info['rbin'][0]) * 2,int(info['zbin'][0])))
        phiBinAngle = int(360 / info['pbin'][0])
        checkedVal = np.zeros((int(info['rbin'][0]) * 2,int(info['rbin'][0]) * 2,int(info['zbin'][0])))
        x0 = int(info['rbin'][0]) - 0.5
        y0 = int(info['rbin'][0]) - 0.5
        stepConverter = 100

        #Reconstructs the R-Phi-Z binning into cartesian coordinate system
        for z in range(0, int(info['zbin'][0])):
            for phi in range(0,int(info['pbin'][0])):
                Rvector = list[0:int(info['rbin'][0])]
                del list[:int(info['rbin'][0])]
                for r in range(0,int(info['rbin'][0])):
                    val = Rvector[r]
                    steps = int(math.ceil(math.pi * (r + 1) * float(phiBinAngle) / 180))
                    for p in range(0,stepConverter * phiBinAngle, stepConverter * phiBinAngle / steps):
                        angle = p * math.pi / (180 * stepConverter) + phi * phiBinAngle * math.pi / 180
                        x = int(round(x0 + (r + 0.5) * math.cos(angle)))
                        y = int(round(y0 + (r + 0.5) * math.sin(angle)))
                        if checkedVal[x,y,z] == 0:
                            cube[x, y,z] = val
                            checkedVal[x,y,z] = 1

        #Interpolating missing values
        print("Interpolating missing values...")
        for z in range(0,cube.shape[2]-1):
            for x in range(0,cube.shape[0] -1):
                for y in range(0,cube.shape[1] -1):
                    if not checkedVal[x,y,z] and math.sqrt(math.pow(x-x0,2) + math.pow(y-y0,2)) < info['rbin'][0]:
                        sum = 0
                        sumCh = 0
                        for i in range(-1,2):
                            for ii in range(-1,2):
                                sum = sum + cube[x+i,y+ii,z]
                                sumCh = sumCh + checkedVal[x+i,y+ii,z]
                        cube[x,y,z] = sum/sumCh
                        checkedVal[x,y,z] = 1
        print("Missing values interpolated")
        cube = np.rot90(cube)
        cube = np.fliplr(cube)

    elif RZ:
        cube = np.zeros((int(info['rbin'][0]) * 2,int(info['rbin'][0]) * 2,int(info['zbin'][0])))
        phiBinAngle = int(360 / 4)
        checkedVal = np.zeros((int(info['rbin'][0]) * 2,int(info['rbin'][0]) * 2,int(info['zbin'][0])))
        x0 = int(info['rbin'][0]) - 0.5
        y0 = int(info['rbin'][0]) - 0.5
        stepConverter = 100      

        #Reconstructs the R-Z binning into cartesian coordinate system
        for z in range(0, int(info['zbin'][0])):
                Rvector = list[0:int(info['rbin'][0])]
                del list[:int(info['rbin'][0])]
                for r in range(0,int(info['rbin'][0])):
                    val = Rvector[r]
                    steps = int(math.ceil(math.pi * (r + 1) * float(phiBinAngle) / 180))
                    for p in range(0,stepConverter * phiBinAngle, stepConverter * phiBinAngle / steps):
                        angle = p * math.pi / (180 * stepConverter)
                        x = int(round(x0 + (r + 0.5) * math.cos(angle)))
                        y = int(round(y0 + (r + 0.5) * math.sin(angle)))
                        if checkedVal[x,y,z] == 0:
                            cube[x, y,z] = val
                            checkedVal[x,y,z] = 1

        #Interpolating missing values
        print("Interpolating missing values...")
        for z in range(0,cube.shape[2]-1):
            for x in range(int(cube.shape[0]/2),cube.shape[0] -1):
                for y in range(int(cube.shape[1]/2),cube.shape[1] -1):
                    if not checkedVal[x,y,z] and math.sqrt(math.pow(x-x0,2) + math.pow(y-y0,2)) < info['rbin'][0]:
                        sum = 0
                        sumCh = 0
                        for i in range(-1,2):
                            for ii in range(-1,2):
                                sum = sum + cube[x+i,y+ii,z]
                                sumCh = sumCh + checkedVal[x+i,y+ii,z]
                        cube[x,y,z] = sum/sumCh
                        checkedVal[x,y,z] = 1
        print("Missing values interpolated")

        tmpCube = np.fliplr(cube)
        cube = cube + tmpCube
        tmpCube = np.flipud(cube)
        cube = cube + tmpCube

    else:
         cube = np.zeros((int(info['xbin'][0]),int(info['ybin'][0]),int(info['zbin'][0])))

         for z in range(0,int(info['zbin'][0])):
              for y in range(0,int(info['ybin'][0])):
                   for x in range(0,int(info['xbin'][0])):
                        cube[x,y,z] = list.pop(0)

    end = time.time()
    print("Cube reconstructed in " + str(round(end - startTime,2)) + " seconds")


    if plot:
        import matplotlib.pyplot as plt
        from matplotlib.colors import LogNorm
        import matplotlib.gridspec as gridspec

        #Determines the indecies of maxiumum value in cube
        i,j,k = np.unravel_index(cube.argmax(), cube.shape)

        #Arbitrary scaling     
        vmax = cube.max()
        vmin = np.min(cube[np.nonzero(cube)])
        if int(math.log10(vmax)) - int(math.log10(vmin)) > 14 :
            vmin = vmax * math.pow(10,-14)

        gs0 = gridspec.GridSpec(1, 3)
        gs00 = gridspec.GridSpecFromSubplotSpec(3, 1, subplot_spec=gs0[0])
        ax = plt.subplot(gs0[1:])
        image = cube[0:,0:,k]
        image = np.rot90(image,3)
        def y_fmt(x, y):
            return cube.shape[0] - x
        ax.xaxis.set_major_formatter(tick.FuncFormatter(y_fmt))
        plt.pcolor(image, norm=LogNorm(vmin=vmin, vmax=vmax), cmap='jet')
        plt.colorbar()
        plt.title('Z plane')
        plt.xlabel('X- axis [Currently reversed order]')
        plt.ylabel('Y- axis')

        plt.subplot(gs00[0])
        image = cube[i,0:,0:]
        plt.pcolor(image, norm=LogNorm(vmin=vmin, vmax=vmax), cmap='jet')
        plt.title('X plane')
        plt.xlabel('Z- axis')
        plt.ylabel('Y- axis')

        plt.subplot(gs00[1])
        image = cube[0:,j,0:]
        plt.pcolor(image, norm=LogNorm(vmin=vmin, vmax=vmax), cmap='jet')
        plt.title('Y plane')
        plt.xlabel('Z- axis')
        plt.ylabel('X- axis')

        plt.subplot(gs00[2])
        vector = np.zeros((cube.shape[2]))
        for r in range(0,cube.shape[2]):
            vector[r] = np.sum(cube[0:,0:,r])
        plt.plot(range(0,cube.shape[2]),vector)
        plt.title('Integrated depth deposition')
        plt.xlabel('Z- axis')
        plt.grid()

        plt.show()


    return cube;

