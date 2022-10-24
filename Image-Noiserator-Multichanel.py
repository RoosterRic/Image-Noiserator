from PIL import Image, ImageOps
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import random
import time
from noise import pnoise2
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys



# ----Window Functions
class MainWindow(QMainWindow):
    # Indices: seed, scale, octaves, persistance, lacunarity. Chanels: red, green, blue
    values = [[0, 100, 15, 0.1, 0.1], [0, 100, 15, 0.1, 0.1], [0, 100, 15, 0.1, 0.1]]
    im = Image
    newPoints = Image

    def __init__(self):
        super().__init__()
        
        # win.setGeometry(200,200,1200,800)
        self.setWindowTitle("Noiserator")

        # ---- RED chanel GUI
        self.label_red = QLabel('Red Channel')
        self.label_red.setAlignment(Qt.AlignCenter)
        self.label_seed_r = QLabel('Seed')
        self.label_seed_r.setAlignment(Qt.AlignRight)
        self.spin_seed_r = QSpinBox()
        self.spin_seed_r.setRange(0, 9999999)
        self.spin_seed_r.setValue(0)
        self.spin_seed_r.valueChanged.connect(self.update_values)

        self.label_scale_r = QLabel('Scale')
        self.label_scale_r.setAlignment(Qt.AlignRight)
        self.spin_scale_r = QSpinBox()
        self.spin_scale_r.setRange(0,1024)
        self.spin_scale_r.setValue(100)
        self.spin_scale_r.valueChanged.connect(self.update_values)

        self.label_octaves_r = QLabel('Octaves')
        self.label_octaves_r.setAlignment(Qt.AlignRight)
        self.spin_octaves_r = QSpinBox()
        self.spin_octaves_r.setRange(-50, 50)
        self.spin_octaves_r.setValue(15)
        self.spin_octaves_r.valueChanged.connect(self.update_values)

        self.label_persistance_r = QLabel('Persistance')
        self.label_persistance_r.setAlignment(Qt.AlignRight)
        self.spin_persistance_r = QDoubleSpinBox()
        self.spin_persistance_r.setRange(-10, 10)
        self.spin_persistance_r.setValue(0.1)
        self.spin_persistance_r.valueChanged.connect(self.update_values)

        self.label_lacunarity_r = QLabel('Lacunarity')
        self.label_lacunarity_r.setAlignment(Qt.AlignRight)
        self.spin_lacunarity_r = QDoubleSpinBox()
        self.spin_lacunarity_r.setRange(-10, 10)
        self.spin_lacunarity_r.setValue(0.1)
        self.spin_lacunarity_r.valueChanged.connect(self.update_values)

        # ---- GREEN chanel GUI
        self.label_green = QLabel('Green Channel')
        self.label_green.setAlignment(Qt.AlignCenter)
        self.label_seed_g = QLabel('Seed')
        self.label_seed_g.setAlignment(Qt.AlignRight)
        self.spin_seed_g = QSpinBox()
        self.spin_seed_g.setRange(0, 9999999)
        self.spin_seed_g.setValue(0)
        self.spin_seed_g.valueChanged.connect(self.update_values)
        

        self.label_scale_g = QLabel('Scale')
        self.label_scale_g.setAlignment(Qt.AlignRight)
        self.spin_scale_g = QSpinBox()
        self.spin_scale_g.setRange(0,1024)
        self.spin_scale_g.setValue(100)
        self.spin_scale_g.valueChanged.connect(self.update_values)

        self.label_octaves_g = QLabel('Octaves')
        self.label_octaves_g.setAlignment(Qt.AlignRight)
        self.spin_octaves_g = QSpinBox()
        self.spin_octaves_g.setRange(-50, 50)
        self.spin_octaves_g.setValue(15)
        self.spin_octaves_g.valueChanged.connect(self.update_values)

        self.label_persistance_g = QLabel('Persistance')
        self.label_persistance_g.setAlignment(Qt.AlignRight)
        self.spin_persistance_g = QDoubleSpinBox()
        self.spin_persistance_g.setRange(-10, 10)
        self.spin_persistance_g.setValue(0.1)
        self.spin_persistance_g.valueChanged.connect(self.update_values)

        self.label_lacunarity_g = QLabel('Lacunarity')
        self.label_lacunarity_g.setAlignment(Qt.AlignRight)
        self.spin_lacunarity_g = QDoubleSpinBox()
        self.spin_lacunarity_g.setRange(-10, 10)
        self.spin_lacunarity_g.setValue(0.1)
        self.spin_lacunarity_g.valueChanged.connect(self.update_values)

        # ---- BLUE chanel GUI
        self.label_blue = QLabel('Blue Channel')
        self.label_blue.setAlignment(Qt.AlignCenter)
        self.label_seed_b = QLabel('Seed')
        self.label_seed_b.setAlignment(Qt.AlignRight)
        self.spin_seed_b = QSpinBox()
        self.spin_seed_b.setRange(0, 9999999)
        self.spin_seed_b.setValue(0)
        self.spin_seed_b.valueChanged.connect(self.update_values)

        self.label_scale_b = QLabel('Scale')
        self.label_scale_b.setAlignment(Qt.AlignRight)
        self.spin_scale_b = QSpinBox()
        self.spin_scale_b.setRange(0,1024)
        self.spin_scale_b.setValue(100)
        self.spin_scale_b.valueChanged.connect(self.update_values)

        self.label_octaves_b = QLabel('Octaves')
        self.label_octaves_b.setAlignment(Qt.AlignRight)
        self.spin_octaves_b = QSpinBox()
        self.spin_octaves_b.setRange(-50, 50)
        self.spin_octaves_b.setValue(15)
        self.spin_octaves_b.valueChanged.connect(self.update_values)

        self.label_persistance_b = QLabel('Persistance')
        self.label_persistance_b.setAlignment(Qt.AlignRight)
        self.spin_persistance_b = QDoubleSpinBox()
        self.spin_persistance_b.setRange(-10, 10)
        self.spin_persistance_b.setValue(0.1)
        self.spin_persistance_b.valueChanged.connect(self.update_values)

        self.label_lacunarity_b = QLabel('Lacunarity')
        self.label_lacunarity_b.setAlignment(Qt.AlignRight)
        self.spin_lacunarity_b = QDoubleSpinBox()
        self.spin_lacunarity_b.setRange(-10, 10)
        self.spin_lacunarity_b.setValue(0.1)
        self.spin_lacunarity_b.valueChanged.connect(self.update_values)

        self.button_load = QPushButton('Load File')
        self.button_load.clicked.connect(self.open_file)

        self.button_run = QPushButton('Run')
        self.button_run.clicked.connect(self.process_image)
        self.button_run.setDisabled(True)

        self.button_save = QPushButton('Save File')
        self.button_save.clicked.connect(self.save_file)
        self.button_save.setDisabled(True)

        # ---- LAYOUT
        lay = QGridLayout()
        # ---- RED layout
        lay.addWidget(self.label_red, 0, 0, 1, 3)
        lay.addWidget(self.label_seed_r, 1, 0, 1, 1)
        lay.addWidget(self.spin_seed_r, 1, 1, 1, 2)
        lay.addWidget(self.label_scale_r, 2, 0, 1, 1)
        lay.addWidget(self.spin_scale_r, 2, 1, 1, 2)
        lay.addWidget(self.label_octaves_r, 3, 0, 1, 1)
        lay.addWidget(self.spin_octaves_r, 3, 1, 1, 2)
        lay.addWidget(self.label_persistance_r, 4, 0, 1, 1)
        lay.addWidget(self.spin_persistance_r, 4, 1, 1, 2)
        lay.addWidget(self.label_lacunarity_r, 5, 0, 1, 1)
        lay.addWidget(self.spin_lacunarity_r, 5, 1, 1, 2)
        # ---- GREEN layout
        lay.addWidget(self.label_green, 0, 3, 1, 3)
        lay.addWidget(self.label_seed_g, 1, 3, 1, 1)
        lay.addWidget(self.spin_seed_g, 1, 4, 1, 2)
        lay.addWidget(self.label_scale_g, 2, 3, 1, 1)
        lay.addWidget(self.spin_scale_g, 2, 4, 1, 2)
        lay.addWidget(self.label_octaves_g, 3, 3, 1, 1)
        lay.addWidget(self.spin_octaves_g, 3, 4, 1, 2)
        lay.addWidget(self.label_persistance_g, 4, 3, 1, 1)
        lay.addWidget(self.spin_persistance_g, 4, 4, 1, 2)
        lay.addWidget(self.label_lacunarity_g, 5, 3, 1, 1)
        lay.addWidget(self.spin_lacunarity_g, 5, 4, 1, 2)
        # ---- BLUE layout
        lay.addWidget(self.label_blue, 0, 6, 1, 3)
        lay.addWidget(self.label_seed_b, 1, 6, 1, 1)
        lay.addWidget(self.spin_seed_b, 1, 7, 1, 2)
        lay.addWidget(self.label_scale_b, 2, 6, 1, 1)
        lay.addWidget(self.spin_scale_b, 2, 7, 1, 2)
        lay.addWidget(self.label_octaves_b, 3, 6, 1, 1)
        lay.addWidget(self.spin_octaves_b, 3, 7, 1, 2)
        lay.addWidget(self.label_persistance_b, 4, 6, 1, 1)
        lay.addWidget(self.spin_persistance_b, 4, 7, 1, 2)
        lay.addWidget(self.label_lacunarity_b, 5, 6, 1, 1)
        lay.addWidget(self.spin_lacunarity_b, 5, 7, 1, 2)

        lay.addWidget(self.button_load, 6, 0, 2, 3)

        lay.addWidget(self.button_run, 6, 3, 2, 3)

        lay.addWidget(self.button_save, 6, 6, 2, 3)

        win = QWidget()
        win.setLayout(lay)
        self.setCentralWidget(win)

    def update_values(self):
        self.values[0][0] = self.spin_seed_r.value()
        self.values[0][1] = self.spin_scale_r.value()
        self.values[0][2] = self.spin_octaves_r.value()
        self.values[0][3] = self.spin_persistance_r.value()
        self.values[0][4] = self.spin_lacunarity_r.value()

        self.values[1][0] = self.spin_seed_g.value()
        self.values[1][1] = self.spin_scale_g.value()
        self.values[1][2] = self.spin_octaves_g.value()
        self.values[1][3] = self.spin_persistance_g.value()
        self.values[1][4] = self.spin_lacunarity_g.value()

        self.values[2][0] = self.spin_seed_g.value()
        self.values[2][1] = self.spin_scale_g.value()
        self.values[2][2] = self.spin_octaves_g.value()
        self.values[2][3] = self.spin_persistance_g.value()
        self.values[2][4] = self.spin_lacunarity_g.value()

    def open_file(self): # loads file
        Tk().withdraw()
        while True:
            try:
                filename = askopenfilename()
                self.im = Image.open(filename)
                self.button_run.setDisabled(False)
                return
            except AttributeError:
                while True:
                    inp = input('Error: No file selected, try again? (y/n): ').lower()
                    if inp == 'n':
                        quit()
                    elif inp == 'y':
                        break

    def save_file(self): # saves file
        Tk().withdraw()
        while True:
            try:
                filename = asksaveasfilename(defaultextension='PNG')
                self.newPoints.save(filename)
                break
            except (AttributeError, ValueError):
                while True:
                    inp = input('Error: No file selected, try again? (y/n): ').lower()
                    if inp == 'n':
                        quit()
                    elif inp == 'y':
                        break

    def process_image(self): # processes image
        self.im = ImageOps.exif_transpose(self.im) # rotates image if needed
        a = np.asarray(self.im)  # generates array from type Image
        dim = a.shape   # array dimensions
        print('Im shape: ', dim)
        if dim[0] < 1000 or dim[1] < 1000:  # Increases image size if too small
            self.im = self.im.resize([dim[1]*2, dim[0]*2])    # ToDo: fix the rescaling to be more consistent AND optional
            a = np.asarray(self.im)
            dim = a.shape
        # bw = np.empty((dim[0], dim[1]))
        # bw = im.convert('L')    # converts Image to Image color type L - grayscale channel
        self.im.show()
        # bw = np.asarray(bw)
        im_r = np.asarray(self.im.getchannel(0))
        im_g = np.asarray(self.im.getchannel(1))
        im_b = np.asarray(self.im.getchannel(2))

        points = np.full_like(self.im, 0)  # generates white matrix of the same size as the scaled input image
        print(points.shape)
        print('Im shape: ', dim)
        print('Pixels: ', dim[0]*dim[1])
        print(self.values[0][0], self.values[0][1], self.values[0][2], self.values[0][3], self.values[0][4])
        timer()
        noiseMap_r = 255*perlin_array([dim[0], dim[1]], self.values[0][1], self.values[0][2], self.values[0][3], self.values[0][4], self.values[0][0])
        timer()
        timer()
        noiseMap_g = 255*perlin_array([dim[0], dim[1]], self.values[1][1], self.values[1][2], self.values[1][3], self.values[1][4], self.values[1][0])
        timer()
        timer()
        noiseMap_b = 255*perlin_array([dim[0], dim[1]], self.values[2][1], self.values[2][2], self.values[2][3], self.values[2][4], self.values[2][0])
        timer()
        timer()
        for i in range(dim[0]):
            for j in range(dim[1]):
                if noiseMap_r[i,j] > im_r[i,j]:
                    points[i,j,0] = noiseMap_r[i,j]
                if noiseMap_g[i,j] > im_g[i,j]:
                    points[i,j,1] = noiseMap_g[i,j]
                if noiseMap_b[i,j] > im_b[i,j]:
                    points[i,j,2] = noiseMap_b[i,j]
        timer()
        # ----Show Processed Image
        newPoints = Image.fromarray(points).convert(mode='RGB')
        newPoints.show()
        self.button_save.setDisabled(False)

# ----Functions----------------------------------------


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

def perlin_array(shape, # Generates perlin noise (engineeredjoy.com)
			scale=100, octaves = 15, 
			persistence = .1, 
			lacunarity = 0.1, 
			seed = None):
    if not seed or seed == 0:
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
# ----Body
app = QApplication(sys.argv)

window = MainWindow()
window.show()
sys.exit(app.exec_())

# ----Pre-processing and Setup
im = ImageOps.exif_transpose(im) # rotates image if needed
a = np.asarray(im)  # generates array from type Image
dim = a.shape   # array dimensions
print('Im shape: ', dim)
if dim[0] < 1000 or dim[1] < 1000:  # Increases image size if too small
    im = im.resize([dim[1]*2, dim[0]*2])    # ToDo: fix the rescaling to be more consistent AND optional
    a = np.asarray(im)
    dim = a.shape
# bw = np.empty((dim[0], dim[1]))
# bw = im.convert('L')    # converts Image to Image color type L - grayscale channel
# bw.show()
# bw = np.asarray(bw)
im_r = np.asarray(im.getchannel(0))
im_g = np.asarray(im.getchannel(1))
im_b = np.asarray(im.getchannel(2))

points = np.full_like(im, 255)  # generates white matrix of the same size as the scaled input image
print(points.shape)
print('Im shape: ', dim)
print('Pixels: ', dim[0]*dim[1])
#bw = np.sum(a, 2)/3 # WAY faster that doing this with for loops :o

# ----Generate Noisemap

seed = input('Set seed for channel(R): ')   # RED
random.seed(seed)
timer()
try: # Use try-catch as cheap way of having 'seed' be optional input
    noiseMap_r = perlin_array([dim[0], dim[1]], seed=int(seed))*255
except ValueError:
    noiseMap_r = perlin_array([dim[0], dim[1]])*255
noiseIm = Image.fromarray(noiseMap_r).show(),
timer()

seed = input('Set seed for channel(G): ')   # GREEN
random.seed(seed)
timer()
try: # Use try-catch as cheap way of having 'seed' be optional input
    noiseMap_g = perlin_array([dim[0], dim[1]], seed=int(seed))*255
except ValueError:
    noiseMap_g = perlin_array([dim[0], dim[1]])*255
noiseIm = Image.fromarray(noiseMap_g).show(),
timer()

seed = input('Set seed for channel(B): ')   # BLUE
random.seed(seed)
timer()
try: # Use try-catch as cheap way of having 'seed' be optional input
    noiseMap_b = perlin_array([dim[0], dim[1]], seed=int(seed))*255
except ValueError:
    noiseMap_b = perlin_array([dim[0], dim[1]])*255
noiseIm = Image.fromarray(noiseMap_b).show(),
timer()


# ----Process Image
timer()
for i in range(dim[0]):
    for j in range(dim[1]):
        if noiseMap_r[i,j] > im_r[i,j]:
            points[i,j,0] = noiseMap_r[i,j]
        if noiseMap_g[i,j] > im_g[i,j]:
            points[i,j,1] = noiseMap_g[i,j]
        if noiseMap_b[i,j] > im_b[i,j]:
            points[i,j,2] = noiseMap_b[i,j]
timer()
# ----Show Processed Image
newPoints = Image.fromarray(points).convert(mode='RGB')
newPoints.show()
# ----Save Processed Image
save_file(newPoints)
