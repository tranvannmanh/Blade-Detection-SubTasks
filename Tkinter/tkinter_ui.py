from tkinter import *
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.width = 500
        self.height = 350
        self.title("Tkinter GUI")
        self.iconbitmap("the_simpsons.ico")
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
        filename = filedialog.askopenfilename(initialdir = "C:/Users/T R N V A N M A N H/Desktop/Tkinter Tutal", title = "Select A File", filetype = (("all files","*.*"),("jpeg files","*.jpg")) )
        
        self.label.configure(text = 'Opening:   '+filename)

        img = Image.open(filename)
        photo = ImageTk.PhotoImage(img)

        self.display_image.configure(image=photo)
        self.display_image.image = photo

        self.imageEditTools(img)


    def imageEditTools(self, image): #image opened by PIL
        tools = ttk.LabelFrame(self, text='tools')
        tools.grid(column=11, row=0, padx=(0, 20), pady=(0, 10))

        zoom_in = ttk.Button(tools,text='Zoom Out', command=lambda : self.imageZoomOut(image))
        zoom_in.grid(column=0, row=0)

        zoom_out = ttk.Button(tools, text='Zoom In', command=lambda : self.imageZoomIn(image))
        zoom_out.grid(column=0, row=1)

        gray_scale = ttk.Button(tools, text='2Gray', command=lambda : self.image2Gray(image))
        gray_scale.grid(column=0, row=2)


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