# settings
step = +0.1  # um, + move up, - move down
count = 100 # total step numbers
frames_per_step = 1 # number of image captured at each step
exposure = 100  # ms
file_prefix = 'IMG_'


# PIZStage, TIPFSOffset change z scan device between these three
z_device = 'TIPFSOffset'


import time
import numpy as np
from PIL import Image
import MMCorePy


mmc = MMCorePy.CMMCore()

# Intialize devices, change if needed.

#### mmc.loadDevice('HamamatsuHam_DCAM','HamamatsuHam','HamamatsuHam_DCAM')
mmc.loadDevice('TIScope','NikonTI','TIScope')
initial_pos=None

if  z_device=='TIPFSOffset':
    mmc.loadDevice('TIPFSOffset','NikonTI','TIPFSOffset')

else:
    mmc.loadDevice('COM4', 'SerialManager', 'COM4')
    mmc.loadDevice('E-709','PI_GCS_2','E-709')
    mmc.loadDevice('PIZStage','PI_GCS_2','PIZStage')
    mmc.setProperty('E-709','Port','COM4')
    mmc.setProperty('PIZStage','Axis','z')
    mmc.setProperty('PIZStage','Controller Name','E-709')
    mmc.setProperty('PIZStage','Limit_um','100.0000')
    initial_pos=50

mmc.initializeAllDevices()
#### mmc.setCameraDevice('HamamatsuHam_DCAM')


mmc.setExposure(exposure)
if initial_pos !=None:
    mmc.setPosition(z_device,initial_pos)
	
	
fp=open('position.txt','w')  # save position of the z device to a txt file
file_count = 0

mmc.setROI(0, 0, 512, 512)  # (int x, int y, int xSize, int ySize)  # specify ROI

for i in range(count):
        #### for j in range(frames_per_step):
        #### mmc.snapImage()
        #### imgData = mmc.getImage()
        ####   # imgData=imgData[1:512,1:512] # another way to get ROI images by cropping out the specific region
        #### Image.fromarray(imgData, 'I;16').save('result/' + file_prefix + str(file_count) + '.tif')
        #### print ('saved ' + 'result/' + file_prefix + str(file_count) + '.tif')
        #### file_count +=1
    try:
        mmc.setRelativePosition(z_device, step)
    except:
        print('com err')
    time.sleep(0.1) # delay time 0.1 s = 100 ms
    pos=mmc.getPosition(z_device)
    print('moved to ' + str(pos))
    fp.write('%f\n' % pos)
if initial_pos !=None:
    mmc.setPosition(z_device,initial_pos)
fp.close()