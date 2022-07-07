import tkinter
from tkinter import *
from tkinter import ttk, filedialog

import numpy as np
import scipy.stats as st
from PIL import Image, ImageTk
from scipy import signal
from skimage.morphology import erosion, dilation
# from skimage.filters import threshold_otsu
from skimage import measure, util
import scipy.stats as st
import numpy as np
from PIL import Image, ImageTk

# from PIL import Image, ImageFilter
# from scipy.ndimage.filters import convolve
# from scipy import signal
# import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
# import scipy.stats as st
# from skimage.morphology import erosion, dilation
# from scipy.ndimage import gaussian_filter
# from skimage.filters import threshold_otsu
# from skimage import measure, util

class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.width = 500
        self.height = 350
        self.image = []
        self.title("Lisence Plate Recognition")
        self.iconbitmap("ICON.ico")
        self.minsize(self.width, self.height)

        # Define a container name 'labelFrame'
        self.labelFrame = ttk.LabelFrame(self, text="Open File")

        # display labelFrame on grid layout
        self.labelFrame.grid(column=0, row=0, padx=(10, 10), pady=(10, 10))

        # self.fileBrowser()
        self.label = ttk.Label(self.labelFrame, text='Choose an image! ')
        self.button = ttk.Button(self.labelFrame, text="Browse A File", command=self.fileDialog)
        self.label.grid(column=1, row=0)
        self.button.grid(column=2, row=0)

        # Display image
        self.display_image = ttk.Label(self.labelFrame)
        self.display_image.grid(column=0, row=1, columnspan=3)

        self.license_plate = ttk.Label(self.labelFrame)
        self.license_plate.grid(column=0, row=2, columnspan=3)

        # self.canvas_img = Canvas(self.labelFrame, width=300, height=300, bg='gray')
        # self.canvas_img.grid(row=1, column=0)

    # def license_plate_display(self, image):
    #     img_display = ImageTk.PhotoImage(image)
    #     self.license_plate.configure(image=img_display)
    #     self.license_plate.image=img_display
    #     # self.imageEditTools(image)

    def fileDialog(self):
        filename = filedialog.askopenfilename(initialdir="C:/Users/", title="Select A File")

        self.label.configure(text='Opening:   ' + filename)

        img = Image.open(filename)
        self.image = img
        self.image_display(img)
        print("Image's size: ", img.size)

    def imageEditTools(self, image):  # image opened by PIL
        tools = ttk.LabelFrame(self, text='tools')
        tools.grid(column=11, row=0, padx=(10, 10), pady=(10, 10), sticky=tkinter.N)

        zoom_in = ttk.Button(tools, text='Zoom Out', command=lambda: self.imageZoomOut(image))
        zoom_in.grid(column=0, row=0)

        zoom_out = ttk.Button(tools, text='Zoom In', command=lambda: self.imageZoomIn(image))
        zoom_out.grid(column=0, row=1)

        gray_scale = ttk.Button(tools, text='2Gray', command=lambda: self.image2Gray(image))
        gray_scale.grid(column=0, row=2)

        blured_image = ttk.Button(tools, text='Gauss Blur', command=lambda: self.gaussian_blur(image))
        blured_image.grid(column=0, row=3)

        threshold_image = ttk.Button(tools, text='Otsu', command=lambda: self.threshold_otsu(image))
        threshold_image.grid(column=0, row=4)

        edge_detected = ttk.Button(tools, text='Edge Detect', command=lambda: self.sobel_edge_detect(image))
        edge_detected.grid(column=0, row=5)

        threshold = ttk.Button(tools, text='Threshold', command=lambda: self.threshold_otsu(image))
        threshold.grid(column=0, row=5)

        erosion = ttk.Button(tools, text='Erosion', command=lambda: self.eros_img(image))
        erosion.grid(column=0, row=6)

        dilation = ttk.Button(tools, text='Dilation', command=lambda: self.dilate_img(image))
        dilation.grid(column=0, row=7)

        opening = ttk.Button(tools, text='Opening', command=lambda: self._opening(image))
        opening.grid(column=0, row=8)

        closing = ttk.Button(tools, text='Closing', command=lambda: self._closing(image))
        closing.grid(column=0, row=9)

        reset = ttk.Button(tools, text='Reset', command=self.origin_img)
        reset.grid(column=0, row=10)

        negative_image = ttk.Button(tools, text='Negative', command=lambda: self.negative_image(image))
        negative_image.grid(column=0, row=11)

        labeled_image = ttk.Button(tools, text='Label', command=lambda: self.image_labels(image))
        labeled_image.grid(column=0, row=12)

    def image_labels(self, image):
        img = np.asarray(image)
        print(img.shape[0], img.shape[1])
        car_labeled = measure.label(img)
        img_displayed = Image.fromarray(car_labeled)
        # plate_dimensions = (0.03*car_labeled.shape[0], 0.2*car_labeled.shape[0], 0.15*car_labeled.shape[1], 0.4*car_labeled.shape[1])
        # min_height, max_height, min_width, max_width = plate_dimensions

        fix, ax = plt.subplots()
        ax.axis('off')
        ax.imshow(np.asarray(self.image), cmap='gray')
        for region in measure.regionprops(car_labeled):
            min_row, min_col, max_row, max_col = region.bbox
            _width = max_col - min_col
            _height = max_row - min_row
            ratio = _width / float(_height)

            region_area = region.area
            image_area = img.shape[0] * img.shape[1]

            if region_area < 0.01*image_area or region_area > 0.08*image_area:
                continue
            # if _height >= min_height and _height <= max_height and _width >= min_width and _width <= max_width and _width > _height:
            if (ratio > 1.0 and ratio < 1.8) or (ratio > 2.5 and ratio < 4.5):
                rect = mpatches.Rectangle((min_col, min_row), max_col - min_col, max_row - min_row, fill=False, edgecolor='red', linewidth=2)
                ax.add_patch(rect)

        plt.tight_layout()
        plt.savefig('tkinter_detected.png')
        plt.show()

        detected = Image.open('tkinter_detected.png')
        self.image_display(detected)
        # self.license_plate_display(img_displayed)

    def threshold_otsu(self, image):
        try:
            bins_num = 256
            hist, bin_edges = np.histogram(image, bins=bins_num)
            bin_mids = (bin_edges[:-1] + bin_edges[1:]) / 2.

            weight1 = np.cumsum(hist)
            weight2 = np.cumsum(hist[::-1])[::-1]

            mean1 = np.cumsum(hist * bin_mids) / weight1
            mean2 = (np.cumsum((hist * bin_mids)[::-1]) / weight2[::-1])[::-1]

            inter_class_variance = weight1[:-1] * \
                                   weight2[1:] * (mean1[:-1] - mean2[1:]) ** 2

            index_of_max_val = np.argmax(inter_class_variance)

            threshold = bin_mids[:-1][index_of_max_val]
            img = np.invert(threshold > image)
            img = Image.fromarray(img)
            self.image_display(img)
            print('LOG:. Threshold otsu')
        except EXCEPTION as e:
            print("ERROR:. Turn image to Gray first!")
            
    def negative_image(self, image):
        img = np.asarray(image)
        img = 255 - img
        image_displayed = Image.fromarray(img)
        self.image_display(image_displayed)

    def image_threshold(self, image):
        img = np.asarray(image)
        threshold_value = threshold_otsu(img)
        image_display = util.invert(img > threshold_value)
        image_display = Image.fromarray(image_display)
        self.image_display(image_display)

    def origin_img(self):
        self.image_display(self.image)
        print('LOG:. Reset')

    def image2Gray(self, image):
        # Convert image to gray
        image = image.convert('L')
        self.image_display(image)
        print('LOG:. 2Gray')

    # Zoom in image processing
    def imageZoomOut(self, image):
        ratio = 0.8
        width, height = image.size
        _size = (width * ratio, height * ratio)
        image.thumbnail(_size, Image.ANTIALIAS)
        self.image_display(image)
        print('LOG:. zoom_in')

    # zoom out image processing
    def imageZoomIn(self, image):
        ratio = 1.2
        width, height = image.size
        _size = (int(width * ratio), int(height * ratio))
        image = image.resize(_size)
        self.image_display(image)
        print('LOG:. zoom_out')

    def gaussian_filter(self, size, nsig=1):
        x = np.linspace(-nsig, nsig, size + 1)
        ker1d = np.diff(st.norm.cdf(x))
        ker2d = np.outer(ker1d, ker1d)
        return ker2d

    def gaussian_blur(self, image):
        try:
            blured_img = signal.convolve2d(image, self.gaussian_filter(kernel_size))
            img = Image.fromarray(blured_img)
            self.image_display(img)
            print('LOG:. blured')
            print('...', img.size)
        except Exception as e:
            print(e, '\nERROR: Gray scale first')

    def sobel_edge_detect(self, image):
        sobel_x = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]])
        sobel_y = np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]])

        try:
            image_x = signal.convolve2d(image, sobel_x)
            image_y = signal.convolve2d(image, sobel_y)
            edge_detected = np.sqrt(np.square(image_x) + np.square(image_y))

            img = Image.fromarray(edge_detected)
            self.image_display(img)
            print('LOG:. Sobel applied')
        except Exception as e:
            print(e, '\nERROR:. Gray scale image first!')

    def _erosion(self, image, filter=None):
        if filter is None:
            filter = []
        if not filter:
            erosion_filter = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])
        else:
            erosion_filter = np.array(filter)
        erosed = erosion(image, erosion_filter)
        return Image.fromarray(erosed)

    def _dilation(self, image, filter=None):
        if filter is None:
            filter = []
        if not filter:
            dilation_filter = np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]])
        else:
            dilation_filter = np.array(filter)
        dilated = dilation(image, dilation_filter)
        return Image.fromarray(dilated)

    def eros_img(self, image):
        try:
            erosed = self._erosion(image)
            self.image_display(erosed)
            print('LOG:. Erosion')
        except Exception as e:
            print('ERROR:. ', e, '\n\t => Gray scale first')

    def dilate_img(self, image):
        try:
            dilated = self._dilation(image)
            self.image_display(dilated)
            print('LOG:. Dilation')
        except Exception as e:
            print('ERROR:. ', e, '\n\t => Gray scale first')

    def _opening(self, image):
        try:
            filter = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
            img = self._erosion(image, filter)
            img = self._dilation(img, filter)
            self.image_display(img)
            print('LOG:. Opening')
        except Exception as e:
            print("ERROR:. Turn image to Gray first!")

    def _closing(self, image):
        try:
            filter = [[1, 0, 1], [0, 1, 0], [1, 0, 1]]
            img = self._dilation(image, filter)
            img = self._erosion(img, filter)
            self.image_display(img)
            print('LOG:. Closing')
        except Exception as e:
            print("ERROR:. Turn image to Gray first!")

    def threshold_otsu(self, image):
        try:
            bins_num = 256
            hist, bin_edges = np.histogram(image, bins=bins_num)
            bin_mids = (bin_edges[:-1] + bin_edges[1:]) / 2.

            weight1 = np.cumsum(hist)
            weight2 = np.cumsum(hist[::-1])[::-1]

            mean1 = np.cumsum(hist * bin_mids) / weight1
            mean2 = (np.cumsum((hist * bin_mids)[::-1]) / weight2[::-1])[::-1]

            inter_class_variance = weight1[:-1] * \
                                   weight2[1:] * (mean1[:-1] - mean2[1:]) ** 2

            index_of_max_val = np.argmax(inter_class_variance)

            threshold = bin_mids[:-1][index_of_max_val]
            img = np.invert(image > threshold)
            img = Image.fromarray(img)
            self.image_display(img)
            print('LOG:. Threshold otsu')
        except EXCEPTION as e:
            print("ERROR:. Turn image to Gray first!")

    def image_display(self, image):
        img_display = ImageTk.PhotoImage(image)
        self.display_image.configure(image=img_display)
        self.display_image.image = img_display
        self.imageEditTools(image)


root = Root()
root.mainloop()
