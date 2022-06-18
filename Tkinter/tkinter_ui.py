from tkinter import *
from tkinter import ttk, filedialog

import numpy as np
import scipy.stats as st
from PIL import Image, ImageTk
from scipy import signal
from skimage.morphology import erosion, dilation


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.width = 500
        self.height = 350
        self.image = []
        self.title("Plate recognition")
        self.iconbitmap("ICON.ico")
        self.minsize(self.width, self.height)

        # Define a container name 'labelFrame'
        self.labelFrame = ttk.LabelFrame(self, text="Open File")

        # display labelFrame on grid layout
        self.labelFrame.grid(column=0, row=0, padx=(20, 20), pady=(20, 20))

        # self.fileBrowser()
        self.label = ttk.Label(self.labelFrame, text='Choose an image! ')
        self.button = ttk.Button(self.labelFrame, text="Browse A File", command=self.fileDialog)
        self.label.grid(column=1, row=0)
        self.button.grid(column=2, row=0)

        # Display image
        self.display_image = ttk.Label(self.labelFrame)
        self.display_image.grid(column=0, row=1, columnspan=3)

    def fileDialog(self):
        filename = filedialog.askopenfilename(initialdir="C:/Users/", title="Select A File")

        self.label.configure(text='Opening:   ' + filename)

        img = Image.open(filename)
        self.image = img
        photo = ImageTk.PhotoImage(img)
        self.display_image.configure(image=photo)
        self.display_image.image = photo

        self.imageEditTools(img)

    def imageEditTools(self, image):  # image opened by PIL
        tools = ttk.LabelFrame(self, text='tools')
        tools.grid(column=11, row=0, padx=(0, 20), pady=(0, 10), )

        zoom_in = ttk.Button(tools, text='Zoom Out', command=lambda: self.imageZoomOut(image))
        zoom_in.grid(column=0, row=0)

        zoom_out = ttk.Button(tools, text='Zoom In', command=lambda: self.imageZoomIn(image))
        zoom_out.grid(column=0, row=1)

        gray_scale = ttk.Button(tools, text='2Gray', command=lambda: self.image2Gray(image))
        gray_scale.grid(column=0, row=2)

        sobel_edge = ttk.Button(tools, text='sobel', command=lambda: self.sobel_edge_detect(image))
        sobel_edge.grid(column=0, row=3)

        blured_image = ttk.Button(tools, text='Gauss Blur', command=lambda: self.gaussian_blur(image))
        blured_image.grid(column=0, row=3)

        edge_detected = ttk.Button(tools, text='Edge Detect', command=lambda: self.sobel_edge_detect(image))
        edge_detected.grid(column=0, row=4)

        erosion = ttk.Button(tools, text='Erosion', command=lambda: self.eros_img(image))
        erosion.grid(column=0, row=5)

        dilation = ttk.Button(tools, text='Dilation', command=lambda: self.dilate_img(image))
        dilation.grid(column=0, row=6)

        reset = ttk.Button(tools, text='Reset', command=self.origin_img)
        reset.grid(column=0, row=7)

    def origin_img(self):
        photo = ImageTk.PhotoImage(self.image)
        self.display_image.configure(image=photo)
        self.display_image.image = photo
        self.imageEditTools(self.image)
        print('LOG:. Reseted')
        self.imageEditTools(self.image)
        print('LOG:. Sobel')

    def image2Gray(self, image):
        # Convert image to gray
        image = image.convert('L')
        image_gray = ImageTk.PhotoImage(image)

        self.display_image.configure(image=image_gray)
        self.display_image.image = image_gray

        self.imageEditTools(image)
        print('LOG:. 2Gray')

    # Zoom in image processing
    def imageZoomOut(self, image):
        ratio = 0.8
        width, height = image.size
        _size = (width * ratio, height * ratio)
        image.thumbnail(_size, Image.ANTIALIAS)

        image_resized = ImageTk.PhotoImage(image)
        self.display_image.configure(image=image_resized)
        self.display_image.image = image_resized
        print('LOG:. zoom_in')

        self.imageEditTools(image)

    # zoom out image processing
    def imageZoomIn(self, image):
        ratio = 1.2
        width, height = image.size
        _size = (int(width * ratio), int(height * ratio))
        image = image.resize(_size)

        image_resize = ImageTk.PhotoImage(image)
        self.display_image.configure(image=image_resize)  # Update image displayed
        self.display_image.image = image_resize

        self.imageEditTools(image)
        print('LOG:. zoom_out')

    def gaussian_filter(self, size, nsig=1):
        x = np.linspace(-nsig, nsig, size + 1)
        ker1d = np.diff(st.norm.cdf(x))
        ker2d = np.outer(ker1d, ker1d)
        return ker2d

    def gaussian_blur(self, image):
        try:
            blured_img = signal.convolve2d(image, self.gaussian_filter(5))
            img = Image.fromarray(blured_img)
            img_display = ImageTk.PhotoImage(img)
            self.display_image.configure(image=img_display)
            self.display_image.image = img_display

            self.imageEditTools(img)
            print('LOG:. blured')
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

            img_display = ImageTk.PhotoImage(img)
            self.display_image.configure(image=img_display)
            self.display_image.image = img_display

            # update image to edit tools
            self.imageEditTools(img)
            print('LOG:. Sobel applied')
        except Exception as e:
            print(e, '\nERROR:. Gray scale image first!')

    def eros_img(self, image):
        eros_filter = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])

        try:
            erosed = erosion(image, eros_filter)
            # Numpy array to Image
            img = Image.fromarray(erosed)
            img_display = ImageTk.PhotoImage(img)
            self.display_image.configure(image=img_display)
            self.display_image.image = img_display
            self.imageEditTools(img)
            print('LOG:. Erosion')
        except Exception as e:
            print('ERROR:. ', e, '\n\t => Gray scale first')

    def dilate_img(self, image):
        dilation_filter = np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]])

        # apply dilation to image
        try:
            dilated = dilation(image, dilation_filter)
            img = Image.fromarray(dilated)
            img_display = ImageTk.PhotoImage(img)
            self.display_image.configure(image=img_display)
            self.display_image.image = img_display
            self.imageEditTools(img)
            print('LOG:. Dilation')
        except Exception as e:
            print('ERROR:. ', e, '\n\t => Gray scale first')


root = Root()
root.mainloop()
