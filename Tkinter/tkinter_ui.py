from tkinter import *
from tkinter import ttk, filedialog
from scipy import signal
from skimage.morphology import erosion, dilation
import scipy.stats as st
from scipy.ndimage import zoom
import numpy as np
from PIL import Image, ImageTk

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
        self.labelFrame = ttk.LabelFrame(self, text = "Open File")

        # display labelFrame on grid layout
        self.labelFrame.grid(column = 0, row = 0, padx=(20, 20), pady=(20,20))

        # self.fileBrowser()
        self.label = ttk.Label(self.labelFrame, text='Choose an image! ')
        self.button = ttk.Button(self.labelFrame, text = "Browse A File",command = self.fileDialog)
        self.label.grid(column=1, row=0)
        self.button.grid(column=2, row = 0)

        # Display image
        self.display_image = ttk.Label(self.labelFrame)
        self.display_image.grid(column=0, row=1, columnspan=3)


    def fileDialog(self):
        filename = filedialog.askopenfilename(initialdir = "C:/Users/", title = "Select A File")
        
        self.label.configure(text = 'Opening:   '+filename)

        img = Image.open(filename)
        self.image= img
        photo = ImageTk.PhotoImage(img)
        self.display_image.configure(image=photo)
        self.display_image.image = photo

        self.imageEditTools(img)


    def imageEditTools(self, image): #image opened by PIL
        tools = ttk.LabelFrame(self, text='tools')
        tools.grid(column=11, row=0, padx=(0, 20), pady=(0, 10),)

        zoom_in = ttk.Button(tools,text='Zoom Out', command=lambda : self.imageZoomOut(image))
        zoom_in.grid(column=0, row=0)

        zoom_out = ttk.Button(tools, text='Zoom In', command=lambda : self.imageZoomIn(image))
        zoom_out.grid(column=0, row=1)

        gray_scale = ttk.Button(tools, text='2Gray', command=lambda : self.image2Gray(image))
        gray_scale.grid(column=0, row=2)

        sobel_edge = ttk.Button(tools, text='sobel', command=lambda : self.sobel_edge_detect(image))
        sobel_edge.grid(column=0,row=3)

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
        self.display_image.image=image_gray

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
        self.display_image.image=image_resized
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
        self.display_image.image=image_resize

        self.imageEditTools(image)
        print('LOG:. zoom_out')

    def gaussian_filter(self, size, nsig=1):
        x = np.linspace(-nsig, nsig, size+1)
        ker1d = np.diff(st.norm.cdf(x))
        ker2d = np.outer(ker1d, ker1d)
        return ker2d

    def gaussian_blur(self, image, kernel_size=5):
        try:
            blured_img = signal.convolve2d(image, self.gaussian_filter(5))
            img = Image.fromarray(blured_img)
            img_display = ImageTk.PhotoImage(img)
            self.display_image.configure(image=img_display)
            self.display_image.image = img_display

            self.imageEditTools(img)
            print('LOG:. blured')
        except Exception as e:
            print(e,'\nERROR: Gray scale first')
        

    def sobel_edge_detect(self, image):
        sobel_x = np.array([[1, 0, -1], [2, 0 ,-2], [1, 0, -1]])
        sobel_y = np.array([[1, 2, 1], [0, 0 ,0], [-1, -2, -1]])

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
            print(e,'\nERROR:. Gray scale image first!')
        


    def eros_img(self, image, epoch=1):
        eros_filter = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])

        try:
            erosed = erosion(image, eros_filter)
            # Numpy array to Image
            img = Image.fromarray(erosed)
            img_display = ImageTk.PhotoImage(img)
            self.display_image.configure(image=img_display)
            self.display_image.image=img_display
            self.imageEditTools(img)
            print('LOG:. Erosion')
        except Exception as e:
            print('ERROR:. ',e, '\n\t => Gray scale first')
        
        
    def dilate_img(self, image, epoch=1):
        dilation_filter = np.array([[1, 0, 1], [0, 1, 0], [1, 0, 1]])

        # apply dilation to image
        try:
            dilated = dilation(image, dilation_filter)
            img = Image.fromarray(dilated)
            img_display = ImageTk.PhotoImage(img)
            self.display_image.configure(image=img_display)
            self.display_image.image=img_display
            self.imageEditTools(img)
            print('LOG:. Dilation')
        except Exception as e:
            print('ERROR:. ',e, '\n\t => Gray scale first')


    # def clipped_zoom(img, zoom_factor, **kwargs):

    #     h, w = img.shape[:2]

    #     # For multichannel images we don't want to apply the zoom factor to the RGB
    #     # dimension, so instead we create a tuple of zoom factors, one per array
    #     # dimension, with 1's for any trailing dimensions after the width and height.
    #     zoom_tuple = (zoom_factor,) * 2 + (1,) * (img.ndim - 2)

    #     # Zooming out
    #     if zoom_factor < 1:

    #         # Bounding box of the zoomed-out image within the output array
    #         zh = int(np.round(h * zoom_factor))
    #         zw = int(np.round(w * zoom_factor))
    #         top = (h - zh) // 2
    #         left = (w - zw) // 2

    #         # Zero-padding
    #         out = np.zeros_like(img)
    #         out[top:top+zh, left:left+zw] = zoom(img, zoom_tuple, **kwargs)

    #     # Zooming in
    #     elif zoom_factor > 1:

    #         # Bounding box of the zoomed-in region within the input array
    #         zh = int(np.round(h / zoom_factor))
    #         zw = int(np.round(w / zoom_factor))
    #         top = (h - zh) // 2
    #         left = (w - zw) // 2

    #         out = zoom(img[top:top+zh, left:left+zw], zoom_tuple, **kwargs)

    #         # `out` might still be slightly larger than `img` due to rounding, so
    #         # trim off any extra pixels at the edges
    #         trim_top = ((out.shape[0] - h) // 2)
    #         trim_left = ((out.shape[1] - w) // 2)
    #         out = out[trim_top:trim_top+h, trim_left:trim_left+w]

    #     # If zoom_factor == 1, just return the input array
    #     else:
    #         out = img
    #     return out

root = Root()
root.mainloop()









# from tkinter import *
# from tkinter import ttk
# app = Tk()

# def submit():
#     print(dirname.get(), "-", type(dirname.get()))
# # labelText=StringVar()
# # labelText.set("Enter directory of log files ::. ")
# labelDir=Label(app, text="Enter directory of log files ::. ", height=4)
# labelDir.pack(side="left")

# directory=StringVar()
# dirname=Entry(app,textvariable=directory, width=20)
# dirname.pack(side="left")

# button = ttk.Button(text='submit', command=submit)
# button.pack()

# app.mainloop()