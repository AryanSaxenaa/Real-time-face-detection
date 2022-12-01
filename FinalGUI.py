import webbrowser
from tkinter import*#Slider ke chakkar mein Label banane ke liye import karna pada 
from Detector import main_app
from create_classifier import train_classifer
from create_dataset import start_capture
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox,PhotoImage
from tkinter import font
from PIL import ImageTk,Image
import time#slider mein sleep function ke liye duration ki delay lene ke liye 
names = set()


class MainUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global names
        with open("nameslist.txt", "r") as f:
            x = f.read()
            z = x.rstrip().split(" ")
            for i in z:
                names.add(i)
        self.title_font = tkfont.Font(family='Times New Roman', size=16, weight="bold")#Times New Roman
        self.title("Real Time Face Detector")#Face recognizer to this kyoki ye project name hai 
        self.resizable(False, False)
        self.geometry("410x240")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None 
        container = tk.Frame(self)
        container.grid(sticky="nsew")#sticky="nsew" to ns  kar diya koi fark nahi pada
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour, PageSix, PageSeven):#4 ke seedhe 6
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
            frame = self.frames[page_name]
            frame.tkraise()

    def on_closing(self):

        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names
            f =  open("nameslist.txt", "a+")
            for i in names:
                    f.write(i+" ")
            self.destroy()


class StartPage(tk.Frame):
        def openweb(self):
            webbrowser.open_new_tab("http://rpunitpoly.amu.ac.in/")

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            #load = Image.open("homepagepic.png")
            #load = load.resize((250, 250), Image.ANTIALIAS)
            #render = PhotoImage(file='homepagepic.png')
            #img = tk.Label(self, image=render)
            #img.image = render
            #img.grid(row=1, column=5, rowspan=4, sticky="nsew")
            label = tk.Label(self, text="University Polytechnic", font=self.controller.title_font,fg="#263942")
            label.grid(row=0,column=5,sticky="ew")

            Frame1=tk.Frame(self)#--->frame banaya hai es class ke andr
            Slider(Frame1)#----->slider banaya hai usmey ye upr jo frame banaya hai vhi pass krdiya,frame ka size change krna ho toh frame1 ka upr he krdeo


            button1 = tk.Button(self, text="   Add a User  ", fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame("PageOne"))
            button2 = tk.Button(self, text="   Check a User  ", fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame("PageTwo"))
            button3 = tk.Button(self, text="Quit", fg="#263942", bg="#ffffff", command=self.on_closing)
            button1.grid(row=1, column=0, ipady=3, ipadx=7)
            button2.grid(row=2, column=0, ipady=3, ipadx=2)
            button3.grid(row=3, column=0, ipady=3, ipadx=32)
            button4 = tk.Button(self, text="       Rp Unit     ", fg="#ffffff", bg="#263942",command=self.openweb)
            button5 = tk.Button(self, text="        Tutorial       ", fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame("PageSix"))
            button6 = tk.Button(self, text="Credits", fg="#ffffff", bg="#263942",command=lambda: self.controller.show_frame("PageSeven"))#iss button ki width ek raaz hai jo raaz reh jaaega
            button4.grid(row=1, column=7, ipady=3, ipadx=7,padx=10,pady=10)
            button5.grid(row=2, column=7, ipady=3, ipadx=2,padx=10,pady=10)
            button6.grid(row=3, column=7, ipady=3, ipadx=26,padx=10,pady=10)


        def on_closing(self):
            if messagebox.askokcancel("Quit", "Are you sure?"):
                global names
                with open("nameslist.txt", "w") as f:
                    for i in names:
                        f.write(i + " ")
                self.controller.destroy()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Enter the name", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, pady=10, padx=5)
        self.user_name = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.user_name.grid(row=0, column=1, pady=10, padx=10)
        self.buttoncanc = tk.Button(self, text="Cancel", bg="#ffffff", fg="#263942", command=lambda: controller.show_frame("StartPage"))
        self.buttonext = tk.Button(self, text="Next", fg="#ffffff", bg="#263942", command=self.start_training)
        self.buttoncanc.grid(row=1, column=0, pady=10, ipadx=5, ipady=4)
        self.buttonext.grid(row=1, column=1, pady=10, ipadx=5, ipady=4)
    def start_training(self):
        global names
        if self.user_name.get() == "None":
            messagebox.showerror("Error", "Name cannot be 'None'")
            return
        elif self.user_name.get() in names:
            messagebox.showerror("Error", "User already exists!")
            return
        elif len(self.user_name.get()) == 0:
            messagebox.showerror("Error", "Name cannot be empty!")
            return
        name = self.user_name.get()
        names.add(name)
        self.controller.active_name = name
        self.controller.frames["PageTwo"].refresh_names()
        self.controller.show_frame("PageThree")


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global names
        self.controller = controller
        tk.Label(self, text="Select user", fg="#263942", font='Helvetica 12 bold').grid(row=0, column=0, padx=10, pady=10)
        self.buttoncanc = tk.Button(self, text="    Cancel      ", command=lambda: controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        self.menuvar = tk.StringVar(self)
        self.dropdown = tk.OptionMenu(self, self.menuvar, *names)
        self.dropdown.config(bg="lightgrey")
        self.dropdown["menu"].config(bg="lightgrey")
        self.buttonext = tk.Button(self, text="     Next     ", command=self.nextfoo, fg="#ffffff", bg="#263942")
        self.dropdown.grid(row=0, column=1, ipadx=8, padx=10, pady=10)
        self.buttoncanc.grid(row=1, ipadx=5, ipady=4, column=0, pady=10)
        self.buttonext.grid(row=1, ipadx=5, ipady=4, column=2, pady=10)

    def nextfoo(self):
        if self.menuvar.get() == "None":
            messagebox.showerror("ERROR", "Name cannot be 'None'")
            return
        self.controller.active_name = self.menuvar.get()
        self.controller.show_frame("PageFour")

    def refresh_names(self):
        global names
        self.menuvar.set('')
        self.dropdown['menu'].delete(0, 'end')
        for name in names:
            self.dropdown['menu'].add_command(label=name, command=tk._setit(self.menuvar, name))

class PageThree(tk.Frame):#Called While Training Model

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.numimglabel = tk.Label(self, text=" Make sure your camera is enabled", font='Helvetica 12 bold', fg="#263942")
        self.numimglabel.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        self.capturebutton = tk.Button(self, text="Capture Data Set", fg="#ffffff", bg="#263942", command=self.capimg)
        self.trainbutton = tk.Button(self, text="Train The Model", fg="#ffffff", bg="#263942",command=self.trainmodel)
        self.capturebutton.grid(row=1, column=0, ipadx=5, ipady=4, padx=10, pady=20)
        self.trainbutton.grid(row=1, column=1, ipadx=5, ipady=4, padx=10, pady=20)

    def capimg(self):
        self.numimglabel.config(text=str("Capturing.........."))#Captured Images = 0 -org #300 aur 311 ka lafda khatam
        messagebox.showinfo("INSTRUCTIONS", "Images of your face will be captured make sure camera is attached to your device")#sentence badla
        x = start_capture(self.controller.active_name)
        self.controller.num_of_images = x
        self.numimglabel.config(text=str("Images Captured Successfully!"))#self.numimglabel.config(text=str("Number of images captured = "+str(x)))

    def trainmodel(self):
        if self.controller.num_of_images < 300:
            messagebox.showerror("ERROR", "No enough Data, Capture at least 300 images!")
            return
        train_classifer(self.controller.active_name)
        messagebox.showinfo("SUCCESS", "The module has been successfully trained!")
        self.controller.show_frame("PageFour")


class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="  Face Recognition", font='Helvetica 16 bold')
        label.grid(row=0,column=0, sticky="ew")
        button1 = tk.Button(self, text="Face Recognition", command=self.openwebcam, fg="#ffffff", bg="#263942")
        button4 = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        button1.grid(row=1,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        button4.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)

    def openwebcam(self):
        main_app(self.controller.active_name)


class PageSix(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
    
        tk.Label(self, text="Tutorial", font='Helvetica 10 bold').place(x=180,y=3)
        tk.Label(self, text="1) To add a new user click on 'Add User' button", font='comicsans 10 bold').place(x=0,y=30)
        tk.Label(self, text="2) Enter the new user name and click next", font='TimesNewRoman 10 bold').place(x=0,y=50)
        tk.Label(self, text="3) Click on 'Capture the data' and wait for the application to", font='Helvetica 10 bold').place(x=0,y=70)
        tk.Label(self, text=" the images of the new user", font='Helvetica 10 bold').place(x=0,y=90)
        tk.Label(self, text="4) Click on 'Train the classifier' ", font='Helvetica 10 bold').place(x=0,y=110)
        tk.Label(self, text="5) Click on 'Face recognition' to begin the face recognition ", font='Helvetica 10 bold').place(x=0,y=130)
        tk.Label(self, text="process ", font='Helvetica 10 bold').place(x=0,y=150)
    
       
        buttonhome = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        buttonhome.place( x=150,y=170)



class PageSeven(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        tk.Label(self,text="Credits",font="helvetica 13 bold",).grid(column=3)
        render1=Image.open("front-end-logo.png")                         
        resize=render1.resize((100,100),Image.ANTIALIAS)       
        render1 = ImageTk.PhotoImage(resize)
        
        img = tk.Label(self, image=render1)
        img.image = render1
        img.grid(row=1, column=0)
        
        render2=Image.open("back-end-logo.png")                             
        resiz=render2.resize((100,100),Image.ANTIALIAS)
        render2 = ImageTk.PhotoImage(resiz)
        
        img1 = tk.Label(self, image=render2)
        img1.image = render2
        img1.grid(row=1, column=5)

        label = tk.Label(self, text="Front End", font='Helvetica 12 bold')
        label.grid(row=3,column=0, sticky="ew")
        label = tk.Label(self, text="     •) Aryan Saxena", font='Helvetica 10 bold')
        label.grid(row=4,column=0, sticky="ew")
        label = tk.Label(self, text="•) Vatsal Jain", font='Helvetica 10 bold')
        label.grid(row=5,column=0, sticky="ew")

        label = tk.Label(self, text="Back End", font='Helvetica 12 bold')
        label.grid(row=3,column=5, sticky="ew")
        label = tk.Label(self, text="    •)Shravan saraswat", font='Helvetica 10 bold')
        label.grid(row=4,column=5, sticky="ew")
        label = tk.Label(self, text="•)Krishna yadav", font='Helvetica 10 bold')
        label.grid(row=5,column=5, sticky="ew")
        buttonhome = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"), bg="#ffffff", fg="#263942")
        buttonhome.grid(row=6,column=3, ipadx=5, ipady=4, padx=10, pady=10)


class Slider:
    def __init__(self,Frame): #root ke vajye frame pass kiya hai
            self.Frame1=Frame #frame banaya hai na ki root
            self.image1=ImageTk.PhotoImage(file="logoAmu.png")#-------->koi bhi image dal liyo
            self.image2=ImageTk.PhotoImage(file="facelogo.png")#-------->koi bhi image dal liyo   
            #Frame_slider=Frame(self.root)
            #Frame_slider.place(x=100,y=50,width=300,height=200)
            self.Frame1.place(x=106,y=30,width=200,height=950)

            self.lbl1=Label(self.Frame1,image=self.image1,bd=0)
            self.lbl1.place(x=0,y=0) 
            self.lbl2=Label(self.Frame1,image=self.image1,bd=0)
            self.lbl2.place(x=0,y=0) 
            self.x=300
            self.slider_func()
    
    def slider_func(self):
        self.x-=1
        if self.x==0:
            self.x=1100
            time.sleep(1)
            #----------Swap-----------------
            self.new_im=self.image1
            self.image1=self.image2
            self.image2=self.new_im
            self.lbl1.config(image=self.image1)
            self.lbl2.config(image=self.image2)
        self.lbl2.place(x=self.x,y=0) 
        self.lbl2.after(1,self.slider_func)  #after ----------> ek Thread Katha        

app = MainUI()
app.iconphoto(False, tk.PhotoImage(file='logoAmu.png'))#Aligarh Muslim University logo
app.mainloop()

