import tkinter as tk
from tkinter import filedialog
from tkinter import *
import cv2
import PIL.Image,PIL.ImageTk
from PIL import ImageTk, Image
import time
import os
from scipy.interpolate import UnivariateSpline
import numpy as np
from tkinter import messagebox
from tkinter import font as tkfont


#create folder directory to save images
folder = r"\FilterX"
home = os.path.expanduser('~')  #it gets the user's home directory by using the expanduser method
location = os.path.join(home, 'Pictures') #adds the folder you want to store the file in
path = location+folder
if not os.path.exists(path):
    os.makedirs(path)


#create a dictionary for the filters
fil = ['color', 'gray', 'warm','vintage', 'cold', 'edges', 'blue','cartoon']
filter_dic = {}
def select_filter(filter, status):
    #change required filter to true
    filter_dic = {x:False for x in fil}
    if filter in filter_dic:
        assert type(status) == bool
        filter_dic[filter] = status
    return filter_dic


def spreadLookupTable(x,y): #used for cool and warm filters
        spline = UnivariateSpline(x,y)
        return spline(range(256))

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")


        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self['background']='#ffffff'

        title = Label(self, text="Login", font=("Raleway", 35, "bold", 'italic'), fg="#FFDE59", bg="white").place(x=90, y=30)
        username = Label(self, text="Username", font=("Raleway", 15, "bold"), fg="gray",
                         bg="white").place(x=90, y=140)
        txt_user = Entry(self, font=("Raleway", 15), bg="lightgray")
        txt_user.place(x=90, y=170, width=350, height=35)

        password = Label(self, text="Password", font=("Raleway", 15, "bold"), fg="gray",
                         bg="white").place(x=90, y=210)
        txt_pass = Entry(self, font=("Raleway", 15), bg="lightgray")
        txt_pass.place(x=90, y=240, width=350, height=35)
        login_btn = Button(self, text="Login", fg="white", bg="#FFDE59", cursor="hand2",
                           font=("Raleway", 15), command=lambda: controller.show_frame("PageTwo"), height=2,
                           width=15).place(x=90,y=290,width=180,height=40)
        sign_up = Button(self, text="Not Registered? Sign Up Here", command=lambda: controller.show_frame("PageOne"), bg="white", fg="#d77337", bd=0, cursor="hand2",
                        font=("Raleway", 8)).place(x=90, y=330)



class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self['background'] = '#ffffff'
        title1 = Label(self, text="Register", font=("Raleway", 35,'italic'), fg="#FFDE59", bg="white").place(x=90, y=30)
        username1 = Label(self, text="Email", font=("Raleway", 15, "bold"), fg="gray",
                          bg="white").place(x=90, y=140)
        txt_user1 = Entry(self, font=("Raleway", 15), bg="lightgray")
        txt_user1.place(x=90, y=170, width=350, height=35)

        password1 = Label(self, text="Password", font=("Raleway", 15, "bold"), fg="gray",
                          bg="white").place(x=90, y=210)
        txt_pass1 = Entry(self, font=("Raleway", 15), bg="lightgray")
        txt_pass1.place(x=90, y=240, width=350, height=35)

        reg_btn = Button(self, text="Register", fg="white", bg="#FFDE59", cursor="hand2",
                           font=("Raleway", 15), command=lambda: controller.show_frame("PageTwo"), height=2,
                           width=15).place(x=90, y=290, width=180, height=40)
        sign_up = Button(self, text="Already Registered? Sign In Here", command=lambda: controller.show_frame("StartPage"),
                         bg="white", fg="#d77337", bd=0, cursor="hand2",
                         font=("Raleway", 8)).place(x=90, y=330)



class PageTwo(tk.Frame):

    def __init__(self, parent, controller,video_source = 0):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.video_source = video_source
        self.vid = MyVideoCapture(self.video_source)
        # initialize the filters
        self.all_filters = select_filter('color', True)
        self.frame_edges = None
        self['background'] = '#ffffff'
        # Labels
        label1 = tk.Label(self, text="Filters",font=("Raleway", 30,'bold'), fg="#FFDE59", bg="white")
        label1.grid(row=0, column=13, columnspan=5)

        label2 = tk.Label(self, text="Saving",font=("Raleway", 30,'bold'), fg="#59DCFF", bg="white")
        label2.grid(row=8, column=13, columnspan=5)

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(self, width=self.vid.width, height=self.vid.height)
        self.canvas.grid(row=0, column=1, rowspan=15, columnspan=5)

        # Button that lets the user take a capture
        self.b_snap = tk.Button(self, text="Capture", width=50, font=("Raleway",12),command=self.capture,fg="white", bg="#59DCFF", cursor="hand2")
        self.b_snap.grid(row=12, column=3, rowspan=7)


        # Button for applying the other filters!
        self.b1 = tk.Button(self, text="Warm Summer", width=13, font=("Raleway", 12),command=self.warm_filter,fg="white", bg="#59DCFF", cursor="hand2",)
        self.b1.grid(row=1, column=13)

        self.b2 = tk.Button(self, text="Cold Winter", width=13, font=("Raleway", 12),command=self.cold_filter,fg="white", bg="#FFDE59", cursor="hand2",)
        self.b2.grid(row=1, column=17)

        self.b3 = tk.Button(self, text="Throwback", width=13, font=("Raleway", 12),command=self.vintage_filter,fg="white", bg="#59DCFF", cursor="hand2",)
        self.b3.grid(row=2, column=13)

        self.b7 = tk.Button(self, text="Cookies & Cream", width=13, font=("Raleway", 12),command=self.gray_filter,fg="white", bg="#FFDE59", cursor="hand2",)
        self.b7.grid(row=2, column=17)

        self.b3_2 = tk.Button(self, text="Off-White", width=13,font=("Raleway", 12), command=self.vintage_filter_plus,fg="white", bg="#59DCFF", cursor="hand2",)
        self.b3_2.grid(row=3, column=13)

        self.b6 = tk.Button(self, text="Galactic", width=13, font=("Raleway", 12),command=self.blue_filter,fg="white", bg="#FFDE59", cursor="hand2",)
        self.b6.grid(row=3, column=17)

        self.b8 = tk.Button(self, text="Fairytale", width=13, font=("Raleway", 12),command=self.cartoon_filter,fg="white", bg="#59DCFF", cursor="hand2",)
        self.b8.grid(row=4, column=13)

        self.b8 = tk.Button(self, text="Color/No Filter", width=13, font=("Raleway", 12),command=self.no_filter,fg="white", bg="#FFDE59", cursor="hand2",)
        self.b8.grid(row=4, column=17)

        self.b10 = tk.Button(self, text="Close Program", font=("Raleway", 12),command=self.destroy,fg="white", bg="#FFDE59", cursor="hand2",)
        self.b10.grid(row=9, rowspan=2, column=17, columnspan=2)

        self.delay = 15
        self.update()


    def capture(self):
        cv2.imwrite(path + r"\frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + '.jpg', self.frame)

    def update(self):
    
        ret, frame, frame1 = self.vid.get_frame()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if self.all_filters['color'] == True:
            pass

        elif self.all_filters['gray'] == True:
            frame = gray
        elif self.all_filters['warm'] == True:
            increaseLookupTable = spreadLookupTable([0, 64, 128, 256], [0, 50, 100, 256])
            decreaseLookupTable = spreadLookupTable([0, 64, 128, 256], [0, 80, 160, 256])
            red_channel, green_channel, blue_channel = cv2.split(frame)
            red_channel = cv2.LUT(red_channel, increaseLookupTable).astype(np.uint8)
            blue_channel = cv2.LUT(blue_channel, decreaseLookupTable).astype(np.uint8)
            frame = cv2.merge((red_channel, green_channel, blue_channel))

        elif self.all_filters['cold'] == True:
            increaseLookupTable = spreadLookupTable([0, 60, 128, 256], [0, 50, 135, 256])
            decreaseLookupTable = spreadLookupTable([0, 64, 128, 256], [0, 80, 160, 256])
            red_channel, green_channel, blue_channel = cv2.split(frame)
            red_channel = cv2.LUT(red_channel, decreaseLookupTable).astype(np.uint8)
            blue_channel = cv2.LUT(blue_channel, increaseLookupTable).astype(np.uint8)
            frame = cv2.merge((red_channel, green_channel, blue_channel))

        elif self.all_filters['vintage'] == True:
            img = np.array(frame, dtype=np.float64)  # converting to float to prevent loss
            img = cv2.transform(img, np.matrix([[0.272, 0.534, 0.131],
                                                [0.349, 0.686, 0.168],
                                                [0.393, 0.769, 0.189]]))  # multipying image with special sepia matrix
            img[np.where(img > 255)] = 255  # normalizing values greater than 255 to 255
            img = np.array(img, dtype=np.uint8)  # converting back to int
            frame = img

        elif self.all_filters['edges'] == True:
            edges = cv2.Canny(frame, 100, 200)
            frame = edges

        elif self.all_filters['blue'] == True:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        elif self.all_filters['cartoon'] == True:
            #EDGES
            gray = cv2.medianBlur(gray,3)
            edges = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 4)
            #COLOR
            color = cv2.bilateralFilter(frame, 9, 300, 300)
            #CARTOON
            cartoon = cv2.bitwise_and(color, color, mask=edges)
            frame = cartoon
        
        if ret:
            self.frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(self.frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.after(self.delay, self.update)

        # update frames for capture
        self.frame = frame

        # all filters
    def gray_filter(self):
        self.all_filters = select_filter('gray', True)

    def vintage_filter_plus(self):
        self.frame_edges = None
        self.all_filters = select_filter('edges', True)

    def warm_filter(self):
        self.all_filters = select_filter('warm', True)

    def vintage_filter(self):
        self.all_filters = select_filter('vintage', True)

    def cold_filter(self):
        self.all_filters = select_filter('cold', True)

    def no_filter(self):
        self.all_filters = select_filter('color', True)

    def blue_filter(self):
        self.all_filters = select_filter('blue', True)

    def cartoon_filter(self):
        self.all_filters = select_filter('cartoon', True)

class MyVideoCapture:
    def __init__(self, video_source=0):
        # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        global_frame1 = None
        self.frame1 = global_frame1

    def get_frame(self):
        ret, frame = self.vid.read()
        if self.vid.isOpened():

            if self.frame1 is None:
                self.frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if ret:
                return (ret, frame, self.frame1)
            else:
                return (ret, None)
        else:
            return (ret, None)

    #clear the video when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

if __name__ == "__main__":

    splash_root = Tk()
    splash_root.title("FilterX")
    icon = ImageTk.PhotoImage(file="icon.ico")
    splash_root.iconphoto(False, icon)
    splash_root.geometry("1000x1000+100+50")
    splash_root.resizable(False, False)
    splash_root['background'] = '#ffffff'
    bg = ImageTk.PhotoImage(file="background.jpg")
    bg_image = Label(splash_root, image=bg).place(x=0, y=0, relwidth=1, relheight=1)
    bg1 = ImageTk.PhotoImage(file="FilterX.png")
    bg_image1 = Label(splash_root, image=bg1).place(x=180, y=100, relwidth=0.6, relheight=0.6)



    def main_window():
        splash_root.destroy()
        app = SampleApp()
        app.title("FilterX")
        icon = ImageTk.PhotoImage(file="icon.ico")
        app.iconphoto(False, icon)
        app['background']='#856ff8'

        app.resizable(False, False) #disable ability to maximize screen

    # Splash screen timer
    splash_root.after(3000, main_window)

    mainloop()

