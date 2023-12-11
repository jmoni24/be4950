# imports for GUI
import tkinter as tk  # python 3
from tkinter import font
from tkinter import *
from PIL import ImageTk, Image
from collections import deque
# imports for sensors
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
import time
import pigpio
from adafruit_mcp3xxx.analog_in import AnalogIn
#from time import sleep

# create readouts for pi sensors
# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D17)
# create the mcp object
mcp = MCP.MCP3008(spi, cs)
# create an analog input channel on pin 0
pH = AnalogIn(mcp, MCP.P2)
temp = AnalogIn(mcp, MCP.P1)
temp2 = AnalogIn(mcp, MCP.P0)
imp = AnalogIn(mcp, MCP.P4)

# Constants for image paths
LOGO_PATH = "/Users/jamiemoni/Downloads/logosafesleeve.png"
NAME_PATH = "/Users/jamiemoni/Downloads/brandnamesmartsleeve.png"
apath = "/Users/jamiemoni/Downloads/a_smartsleeve+.png"
jpath = "/Users/jamiemoni/Downloads/j_smartsleeve+.png"
ppath = "/Users/jamiemoni/Downloads/p_smartsleeve+.png"
gpath = "/Users/jamiemoni/Downloads/g_smartsleeve+.png"
pbepath = "/Users/jamiemoni/Downloads/pbe_smartsleeve+.png"

# pH value
dph = pH.voltage
# temperature value
dtp1 = temp.voltage
# calibrated temperature baseline
dtp1c = 96
# impedance value
dip1 = imp.voltage
# calibrated impedance value
dip1c = 100


class App(tk.Tk):

    def __init__(self, title, size):
        super().__init__()

        self.title(title)
        self.title_font = font.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (Home, Login, Data, Calibration, FAQ, AboutUs):
            page_name = F.__name__
            frame = F(master=container, controller=self)
            self.frames[page_name] = frame

            # put all the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Home")
        self.after(3000, self.home_delay)
        self.mainloop()

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()

    def home_delay(self):
        self.show_frame('Login')


class Home(tk.Frame):

    def __init__(self, master, controller):
        super().__init__(master, bg='light blue', height=700)
        self.home_nimage = None
        self.home_limage = None
        self.controller = controller
        self.home_widgets()

    def home_widgets(self):
        self.load_images_home()

    def load_images_home(self):
        home_logo = Image.open(LOGO_PATH)
        home_lresized = home_logo.resize((200, 200), Image.NEAREST)
        self.home_limage = ImageTk.PhotoImage(home_lresized)
        hlogo = tk.Label(self, image=self.home_limage, bg='light blue')
        hlogo.place(x=161.5, y=150, anchor=CENTER)

        home_name = Image.open(NAME_PATH)
        home_nresized = home_name.resize((300, 150), Image.NEAREST)
        self.home_nimage = ImageTk.PhotoImage(home_nresized)
        hname = tk.Label(self, image=self.home_nimage, bg='light blue')
        hname.place(x=161.5, y=350, anchor=CENTER)


class Login(tk.Frame):

    def __init__(self, master, controller):
        super().__init__(master, bg='light blue', height=700)
        self.login_nimage = None
        self.login_limage = None
        self.controller = controller
        self.up = None
        self.username_entry = None
        self.password_entry = None
        self.name_image1 = None
        self.logo_image1 = None
        self.login_widgets()

    def login_widgets(self):
        self.load_images_login()

        # Additional labels for the Login page
        username_label = tk.Label(self, text="Username", font=self.up, bg='light blue')
        username_label.place(x=161.5, y=315, anchor=CENTER)
        self.username_entry = tk.Entry(self, width=10, borderwidth=0, highlightthickness=0)
        self.username_entry.place(x=161.5, y=343, anchor=CENTER)

        # Create password label and entry on Home page
        password_label = tk.Label(self, text="Password", font=self.up, bg='light blue')
        password_label.place(x=161.5, y=385, anchor=CENTER)
        self.password_entry = tk.Entry(self, width=10, borderwidth=0, highlightthickness=0)
        self.password_entry.place(x=161.5, y=413, anchor=CENTER)

        login = tk.Button(self, text="Login", width=7, bg="gray", fg="black", highlightbackground='light blue',
                          command=lambda: self.controller.show_frame("Calibration"))
        login.place(x=161.5, y=490, anchor=CENTER)

    def load_images_login(self):
        login_logo = Image.open(LOGO_PATH)
        login_lresized = login_logo.resize((150, 150), Image.NEAREST)
        self.login_limage = ImageTk.PhotoImage(login_lresized)
        llogo = tk.Label(self, image=self.login_limage, bg='light blue')
        llogo.place(x=161.5, y=105, anchor=CENTER)

        login_name = Image.open(NAME_PATH)
        login_nresized = login_name.resize((230, 80), Image.NEAREST)
        self.login_nimage = ImageTk.PhotoImage(login_nresized)
        lname = tk.Label(self, image=self.login_nimage, bg='light blue')
        lname.place(x=161.5, y=231, anchor=CENTER)


class Calibration(tk.Frame):

    def __init__(self, master, controller):
        super().__init__(master, bg='light blue', height=700)
        self.controller = controller
        self.cf = font.Font(size=20)
        self.dtp1c_values = deque(maxlen=10)  # Keep the last 10 values for rolling average
        self.dip1c_values = deque(maxlen=10)  # Keep the last 10 values for rolling average
        self.calibration_widgets()

    def calibration_widgets(self):
        calibrate = tk.Button(self, text="Calibrate", width=15, height=3, font=self.cf, bg="gray", fg="black",
                              highlightbackground='light blue',
                              command=lambda: self.calibrate())
        calibrate.place(x=161.5, y=250, anchor=CENTER)

        calibrate = tk.Button(self, text="Already Calibrated", width=15, height=3, font=self.cf, bg="gray", fg="black",
                              highlightbackground=
                              'light blue', command=lambda: self.controller.show_frame("Data"))
        calibrate.place(x=161.5, y=400, anchor=CENTER)

    def calibrate(self):
        global dtp1c, dip1c

        # Simulate calibration process (replace this with actual calibration logic)
        self.dtp1c_values.append(dtp1c)
        self.dip1c_values.append(dip1c)

        # Calculate rolling average for temperature and impedance
        rolling_average_dtp1c = sum(self.dtp1c_values) / len(self.dtp1c_values)
        rolling_average_dip1c = sum(self.dip1c_values) / len(self.dip1c_values)

        dtp1c = rolling_average_dtp1c
        dip1c = rolling_average_dip1c

        self.after(3000)
        self.controller.show_frame("Data")


# change color based on read values
if dph > 7.3:
    cph = "red"
elif 5.6 <= dph <= 7.3:
    cph = "yellow"
else:
    cph = "green"

if dtp1 - 5.4 > dtp1c:
    ctp = "red"
elif dtp1 - 1.8 <= dtp1c <= dtp1 - 5.4:
    ctp = "yellow"
else:
    ctp = "green"

if dip1 < 0.8 * dip1c:
    cip = "red"
elif 0.8 * dip1c <= dip1 <= 0.9 * dip1c:
    cip = "yellow"
else:
    cip = "green"


class Data(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg='light blue', height=700)
        self.error_label = None
        self.login_nimage = None
        self.login_limage = None
        self.controller = controller
        self.dl = font.Font(size=30)
        self.dt = font.Font(size=25)
        self.dph = dph
        self.cph = cph
        self.dtp = f"{dtp1}\N{DEGREE SIGN}F"
        self.ctp = ctp
        self.dip = str(dip1) + " m\u03A9"
        self.cip = cip
        self.data_widgets()
        self.load_images_data()

    def data_widgets(self):
        # Create pH, temp, impedance labels on Data page
        pH_label = tk.Label(self, text='pH', font=self.dl, bg='light blue')
        pH_label.place(x=161.5, y=105, anchor=CENTER)
        pH_text = tk.Label(self, text=self.dph, font=self.dt, fg=self.cph, bg='light blue')
        pH_text.place(x=161.5, y=175, anchor=CENTER)

        temp_label = tk.Label(self, text='Temperature', font=self.dl, bg='light blue')
        temp_label.place(x=161.5, y=245, anchor=CENTER)
        temp_text = tk.Label(self, text=self.dtp, font=self.dt, fg=self.ctp, bg='light blue')
        temp_text.place(x=161.5, y=315, anchor=CENTER)

        imp_label = tk.Label(self, text='Impedance', font=self.dl, bg='light blue')
        imp_label.place(x=161.5, y=385, anchor=CENTER)
        imp_text = tk.Label(self, text=self.dip, font=self.dt, fg=self.cip, bg='light blue')
        imp_text.place(x=161.5, y=455, anchor=CENTER)

        # Check if two of cph, ctp, or cip are yellow or red
        error_condition = (self.cph in ['yellow', 'red']) + (self.ctp in ['yellow', 'red']) + (
                self.cip in ['yellow', 'red'])

        if error_condition >= 2:
            # Display message on the screen
            self.error_label = tk.Label(self, text="***Contact your Provider***", font=self.dt, fg='red', bg='white')
            self.error_label.place(x=161.5, y=500, anchor=CENTER)
            self.blink()

        sign_out = tk.Button(self, text="Sign Out", width=7, bg="gray", fg="black", highlightbackground='light blue',
                             command=lambda: self.go_to_login())
        sign_out.place(x=60, y=600, anchor=CENTER)

        faq = tk.Button(self, text="FAQ", width=7, bg="gray", fg="black", highlightbackground='light blue',
                        command=lambda: self.controller.show_frame("FAQ"))
        faq.place(x=263, y=600, anchor=CENTER)

    def blink(self):
        if self.error_label.winfo_ismapped():
            self.error_label.place_forget()
        else:
            self.error_label.place(x=161.5, y=550, anchor=CENTER)
        # Schedule the next blink after 500 milliseconds (adjust the value as needed)
        self.after(500, self.blink)

    def load_images_data(self):
        login_logo = Image.open(LOGO_PATH)
        login_lresized = login_logo.resize((75, 75), Image.NEAREST)
        self.login_limage = ImageTk.PhotoImage(login_lresized)
        llogo = tk.Label(self, image=self.login_limage, bg='light blue')
        llogo.place(x=161.5, y=600, anchor=CENTER)

        login_name = Image.open(NAME_PATH)
        login_nresized = login_name.resize((300, 100), Image.NEAREST)
        self.login_nimage = ImageTk.PhotoImage(login_nresized)
        lname = tk.Label(self, image=self.login_nimage, bg='light blue')
        lname.place(x=161.5, y=30, anchor=CENTER)

    def go_to_login(self):
        # Clear entry boxes before switching to the Login page
        login_frame = self.controller.frames["Login"]
        login_frame.username_entry.delete(0, tk.END)
        login_frame.password_entry.delete(0, tk.END)
        self.controller.show_frame("Login")


class FAQ(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg='light blue', height=700)
        self.faq_limage = None
        self.controller = controller
        self.fl = font.Font(size=20)
        self.ft = font.Font(size=13)
        self.faq_widgets()
        self.load_images_faq()

    def faq_widgets(self):
        # Create descriptions for pH, temp, impedance labels on FAQ page (layman's terms)
        pH_def_q = tk.Label(self, text='What is pH?', font=self.fl, bg='light blue')
        pH_def_q.place(x=10, y=47)
        pH_def_a = tk.Label(self, text=
        "pH is a way to measure how acidic or basic a "
        "substance is. It's a scale from 0 to 14, where "
        "lower numbers mean something is more acidic, "
        "higher numbers mean its more basic, and 7 is "
        "neutral. The pH of a healthy person's skin is "
        "between 4.2 and 5.6. However after an infection, "
        "the pH of the skin will rise above 7.3.",
                            font=self.ft, bg='light blue', wraplength=300, justify="left")
        pH_def_a.place(x=10, y=72)

        temp_def_q = tk.Label(self, text=
        "What does temperature mean for "
        "my injury?",
                              font=self.fl, bg='light blue', wraplength=300, justify="left")
        temp_def_q.place(x=10, y=210)
        temp_def_a = tk.Label(self, text=
        "When it comes to checking for an infection "
        "if the area around the injury feels warmer "
        "than usual, it might mean there's inflammation "
        "and a possible infection. An increase of 1.8\N{DEGREE FAHRENHEIT} "
        "to 5.4\N{DEGREE FAHRENHEIT} from your normal skin temperature "
        "can be a cause for concern. ",
                              font=self.ft, bg='light blue', wraplength=300, justify="left")
        temp_def_a.place(x=10, y=262)

        imp_def_q = tk.Label(self, text='What is impedance?', font=self.fl, bg='light blue')
        imp_def_q.place(x=10, y=400)
        imp_def_a = tk.Label(self, text=
        "Skin impedance is the skin's resistance to "
        "electrical flow. Changes in skin impedance "
        "may potentially signal an infection due to inflammation, "
        "edema, or the presence of bacteria. If your impedance "
        "is lower than normal, it may be cause for concern.",
                             font=self.ft, bg='light blue', wraplength=300, justify="left")
        imp_def_a.place(x=10, y=425)

        sign_out = tk.Button(self, text="Sign Out", width=7, bg="gray", fg="black", highlightbackground='light blue',
                             command=lambda: self.go_to_login())
        sign_out.place(x=60, y=600, anchor=CENTER)

        data = tk.Button(self, text="Data", width=7, bg="gray", fg="black", highlightbackground='light blue',
                         command=lambda: self.controller.show_frame("Data"))
        data.place(x=263, y=600, anchor=CENTER)

        about_us = tk.Button(self, text="Meet the Team", width=9, bg="gray", fg='black',
                             highlightbackground='light blue', command=lambda: self.controller.show_frame("AboutUs"))
        about_us.place(x=161.5, y=660, anchor=CENTER)

    def go_to_login(self):
        # Clear entry boxes before switching to the Login page
        login_frame = self.controller.frames["Login"]
        login_frame.username_entry.delete(0, tk.END)
        login_frame.password_entry.delete(0, tk.END)
        self.controller.show_frame("Login")

    def load_images_faq(self):
        faq_logo = Image.open(LOGO_PATH)
        faq_lresized = faq_logo.resize((75, 75), Image.NEAREST)
        self.faq_limage = ImageTk.PhotoImage(faq_lresized)
        flogo = tk.Label(self, image=self.faq_limage, bg='light blue')
        flogo.place(x=161.5, y=600, anchor=CENTER)


class AboutUs(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg='#0c246a', height=700)
        self.pbe_image = None
        self.p_image = None
        self.g_image = None
        self.a_image = None
        self.j_image = None
        self.nt = font.Font(size=15)
        self.controller = controller
        self.about_us_widgets()
        self.load_images_au()

    def about_us_widgets(self):
        sign_out = tk.Button(self, text="Sign Out", width=7, bg="gray", fg="black", highlightbackground='#0c246a',
                             command=lambda: self.go_to_login())
        sign_out.place(x=60, y=600, anchor=CENTER)

        faq = tk.Button(self, text="FAQ", width=7, bg="gray", fg="black", highlightbackground='#0c246a',
                        command=lambda: self.controller.show_frame("FAQ"))
        faq.place(x=263, y=600, anchor=CENTER)

    def go_to_login(self):
        # Clear entry boxes before switching to the Login page
        login_frame = self.controller.frames["Login"]
        login_frame.username_entry.delete(0, tk.END)
        login_frame.password_entry.delete(0, tk.END)
        self.controller.show_frame("Login")

    def load_images_au(self):
        aphoto = Image.open(apath)
        aphoto_resized = aphoto.resize((150, 150), Image.NEAREST)
        self.a_image = ImageTk.PhotoImage(aphoto_resized)
        apic = tk.Label(self, image=self.a_image, bg='#0c246a')
        apic.place(x=81.5, y=100, anchor=CENTER)

        apicl = tk.Label(self, text='Ajit Saran', font=self.nt, bg='#0c246a', fg='white', width=15)
        apicl.place(x=81.5, y=200, anchor=CENTER)

        jphoto = Image.open(jpath)
        jphoto_resized = jphoto.resize((150, 150), Image.NEAREST)
        self.j_image = ImageTk.PhotoImage(jphoto_resized)
        jpic = tk.Label(self, image=self.j_image, bg='#0c246a')
        jpic.place(x=241.5, y=100, anchor=CENTER)

        jpicl = tk.Label(self, text='Jamie Moni', font=self.nt, bg='#0c246a', fg='white', width=15)
        jpicl.place(x=241.5, y=200, anchor=CENTER)

        gphoto = Image.open(gpath)
        gphoto_resized = gphoto.resize((150, 150), Image.NEAREST)
        self.g_image = ImageTk.PhotoImage(gphoto_resized)
        gpic = tk.Label(self, image=self.g_image, bg='#0c246a')
        gpic.place(x=81.5, y=300, anchor=CENTER)

        gpicl = tk.Label(self, text='Gautham Nair', font=self.nt, bg='#0c246a', fg='white', width=15)
        gpicl.place(x=81.5, y=400, anchor=CENTER)

        pphoto = Image.open(ppath)
        pphoto_resized = pphoto.resize((150, 150), Image.NEAREST)
        self.p_image = ImageTk.PhotoImage(pphoto_resized)
        ppic = tk.Label(self, image=self.p_image, bg='#0c246a')
        ppic.place(x=241.5, y=300, anchor=CENTER)

        ppicl = tk.Label(self, text='Pavan Raghupathy', font=self.nt, bg='#0c246a', fg='white', width=15)
        ppicl.place(x=241.5, y=400, anchor=CENTER)

        pbephoto = Image.open(pbepath)
        pbephoto_resized = pbephoto.resize((330, 110), Image.NEAREST)
        self.pbe_image = ImageTk.PhotoImage(pbephoto_resized)
        pbepic = tk.Label(self, image=self.pbe_image, bg='#0c246a')
        pbepic.place(x=161.5, y=500, anchor=CENTER)


if __name__ == "__main__":
    App('SmartSleeve+', (323, 700))
