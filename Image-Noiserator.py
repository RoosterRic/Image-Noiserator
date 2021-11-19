from PIL import Image, ImageOps
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import random
import time
from noise import pnoise2

#-----Functions
def timer():    # Call timer once to start, and again to stop and print results
    if timer.start:
        timer.tic = time.perf_counter()
        timer.start = False
    else:
        timer.toc = time.perf_counter()
        print("Elapsed time:", timer.toc - timer.tic, "(s)")
        timer.start = True
timer.start = True
timer.tic = 0
timer.toc = 0

def open_file(): # loads file
  Tk().withdraw()
  while True:
      try:
          fileName = askopenfilename()
          im = Image.open(fileName)
          return im
      except AttributeError:
          while True:
              inp = input('Error: No file selected, try again? (y/n): ').lower()
              if inp == 'n':
                  quit()
              elif inp == 'y':
                  break

def save_file(file): # saves file
  Tk().withdraw()
  while True:
      try:
          fileName = asksaveasfilename(defaultextension='PNG')
          file.save(fileName)
          break
      except (AttributeError, ValueError):
          while True:
              inp = input('Error: No file selected, try again? (y/n): ').lower()
              if inp == 'n':
                  quit()
              elif inp == 'y':
                  break

def perlin_array(shape, # Generates perlin noise (engineeredjoy.com)
			scale=100, octaves = 15, 
			persistence = .1, 
			lacunarity = 0.1, 
			seed = None):
    if not seed:
        seed = np.random.randint(0, 100)
        print("seed was {}".format(seed))
    arr = np.zeros(shape)
    for i in range(shape[0]):
        for j in range(shape[1]):
            arr[i][j] = pnoise2(i / scale,
                                        j / scale,
                                        octaves=octaves,
                                        persistence=persistence,
                                        lacunarity=lacunarity,
                                        repeatx=1024,
                                        repeaty=1024,
                                        base=seed)
    max_arr = np.max(arr)
    min_arr = np.min(arr)
    norm_me = lambda x: (x-min_arr)/(max_arr - min_arr)
    norm_me = np.vectorize(norm_me)
    arr = norm_me(arr)
    return arr
#-----Body
im = open_file()
#-----Pre-processing and Setup
im = ImageOps.exif_transpose(im) # rotates image if needed
a = np.asarray(im)  # generates array from type Image
dim = a.shape   # array dimensions
print('Im shape: ', dim)
if dim[0] < 1000 or dim[1] < 1000:  # Increases image size if too small
    im = im.resize([dim[1]*2, dim[0]*2])    # ToDo: fix the rescaling to be more consistent AND optional
    a = np.asarray(im)
    dim = a.shape
# bw = np.empty((dim[0], dim[1]))
bw = im.convert('L')    # converts Image to Image color type L - grayscale channel
bw.show()
bw = np.asarray(bw)
points = np.full_like(bw, 255)  # generates white matrix of the same size as the scaled input image
print('Im shape: ', dim)
print('Pixels: ', dim[0]*dim[1])
#bw = np.sum(a, 2)/3 # WAY faster that doing this with for loops :o
#-----Generate Noisemap
seed = input('Set seed: ')
random.seed(seed)
timer()
try: # Use try-catch as cheap way of having 'seed' be optional input
    noiseMap = perlin_array([dim[0], dim[1]], seed=int(seed))*255
except:
    noiseMap = perlin_array([dim[0], dim[1]])*255
noiseIm = Image.fromarray(noiseMap).show()
timer()
#-----Process Image
timer()
for i in range(dim[0]):
    for j in range(dim[1]):
        if noiseMap[i,j] > bw[i,j]:
            points[i,j] = 0
timer()
#-----Show Processed Image
newPoints = Image.fromarray(points).convert(mode='L')
newPoints.show()
#-----Save Processed Image
save_file(newPoints)