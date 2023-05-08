"""
The player UI
"""
import argparse
import textwrap
import xml.etree.ElementTree as ET
from tkinter import *
from PIL import Image, ImageTk
import pygame

""" 
Parse Arguments 
"""
def parse_params():
    parser = argparse.ArgumentParser(prog='player.py',
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     description=textwrap.dedent('''\
                                     mixerr player. Audio player and representative mixes visualization from the solution space.
                                     Default command-line (mixerr and player):
                                     f=Nerve9_PrayForTheRain; python -m mixerr --project=$f && python mixerr/player.py --project=$f
                                     player only command-line: python mixerr/player.py --project=Nerve9_PrayForTheRain
                                     '''))
    
    ## Input related to uniform solving and sampling
    basic_args = parser.add_argument_group("Basic Options")

    parser.add_argument("--project", type=str, default="Nerve9_PrayForTheRain",
                        help="The running project. Default: Nerve9_PrayForTheRain")
    parser.add_argument('--display', action='store_true',
                        help="Display additional information from the inner processes")

    return parser.parse_args()


## Arg parse
args = parse_params()
audio_project   = args.project
display         = args.display

project_path = "mixerr/results/%s/"%audio_project

print("Reading the XML file")
## Passing the path of the xml document to enable the parsing process
xml_file = project_path + "%s.xml"%audio_project
tree = ET.parse(xml_file)

## getting the parent tag of the xml document
root = tree.getroot()

## printing the root (parent) tag of the xml document, along with its memory location
print(root.tag)
## raise error if tag is not mixerr

## Get the project name
for child in root:
    if "project" == child.tag:
        print(child.attrib["name"])

mixes = {}
        
## Get the grid
for i in range(16):
    grid = root[1][i] 
    cell = int(str(grid.attrib["number"]))
    answer = grid.text
    if display:
        print(cell, answer)
    mixes[cell] = "Mix_Answer %s"%answer


print("Iniatializing the UI")

project = "mixerr/results/%s"%audio_project

current_track = 0

if display:
    for key, value in mixes.items():
        print(key, value)

## When each tile is pressed
def button_clicked(selected):
    ## Play the selected mix
    global current_track
    mix_path = "%s/mixes/%s.wav"%(project, mixes[selected])
    print("cell:", selected, ", Answer:",  mix_path)
    if current_track != selected:
        new_text = "Playing mix: %s"%selected
        selected_mix_number.set(new_text)
        pygame.mixer.music.load(mix_path)
        pygame.mixer.music.play()
        current_track = selected
    else:
        new_text = "Paused mix: %s"%selected
        selected_mix_number.set(new_text)
        pygame.mixer.music.stop()

    ## Update the new the plan
    txtarea.config(state= NORMAL)
    txtarea.delete("1.0","end")
    plan_path = "%s/plans/%s.txt"%(project, mixes[selected])
    f = open(plan_path)
    plan = f.read()
    f.close()
    txtarea.insert("1.0", plan)
    txtarea.config(state= DISABLED)

    ## Display the plots
    plot_path = "%s/plots/%s.png"%(project, mixes[selected])
    image = Image.open(plot_path)
    
    image = image.resize((750, 370))
    resized = ImageTk.PhotoImage(image)

    imagebox.config(image=resized)
    imagebox.image = resized 

## 12) Build the grid and the UI
    
# Create object
window = Tk()

# Adjust size
window.geometry("800x800")
window.resizable(False, False)

window.title('mixerr')

## The welcome message
welcome_text = "mixerr: Representative mixes from the solution space with Answer Set Programming."
top_text = Label(window,
                 text = welcome_text,
                 font=("Arial", 18)).place(x = 10,
                                           y = 2)

project_text = Label(window,
                     text = "Project: %s"%project,
                     font=("Arial", 14)).place(x = 10,
                                               y = 24)

mix_text = Label(window,
                 text = "Mix Space",
                 font=("Arial", 14)).place(x = 10,
                                           y = 47)
plan_text = Label(window,
                 text = "Plan",
                 font=("Arial", 14)).place(x = 350,
                                           y = 47)
plot_text = Label(window,
                 text = "Plot",
                 font=("Arial", 14)).place(x = 10,
                                           y = 390)



##   13) Build the player
pygame.mixer.init()

##   14) Build the grid

# create a StringVar class
selected_mix_number = StringVar()
selected_plan_data = StringVar()
 
# set the text
selected_mix_number.set("Playing mix: ")
selected_plan_data.set("")
 
# create a label widget
my_label = Label(window,
                 textvariable = selected_mix_number,
                 font=("Arial", 16)).place(x = 10,
                                           y = 350)

photo1  = PhotoImage(file = r"mixerr/tiles/1.png")
photo2  = PhotoImage(file = r"mixerr/tiles/2.png")
photo3  = PhotoImage(file = r"mixerr/tiles/3.png")
photo4  = PhotoImage(file = r"mixerr/tiles/4.png")
photo5  = PhotoImage(file = r"mixerr/tiles/5.png")
photo6  = PhotoImage(file = r"mixerr/tiles/6.png")
photo7  = PhotoImage(file = r"mixerr/tiles/7.png")
photo8  = PhotoImage(file = r"mixerr/tiles/8.png")
photo9  = PhotoImage(file = r"mixerr/tiles/9.png")
photo10 = PhotoImage(file = r"mixerr/tiles/10.png")
photo11 = PhotoImage(file = r"mixerr/tiles/11.png")
photo12 = PhotoImage(file = r"mixerr/tiles/12.png")
photo13 = PhotoImage(file = r"mixerr/tiles/13.png")
photo14 = PhotoImage(file = r"mixerr/tiles/14.png")
photo15 = PhotoImage(file = r"mixerr/tiles/15.png")
photo16 = PhotoImage(file = r"mixerr/tiles/16.png")

x_ = 10
y_ = 70
w_ = 60

## First row
my_button = Button(window, image = photo1,  height=w_, width=w_, command=lambda: button_clicked(1))
my_button.place(x=x_, y=y_)

x_ += w_ + 9
my_button = Button(window, image = photo2,  height=w_, width=w_, command=lambda: button_clicked(2))
my_button.place(x=x_, y=y_)

x_ += w_ + 9
my_button = Button(window, image = photo3,  height=w_, width=w_, command=lambda: button_clicked(3))
my_button.place(x=x_, y=y_)

x_ += w_ + 9
my_button = Button(window, image = photo4,  height=w_, width=w_, command=lambda: button_clicked(4))
my_button.place(x=x_, y=y_)

## Second row
y_ += w_ + 9
x_ = 10
my_button = Button(window, image = photo5,  height=w_, width=w_, command=lambda: button_clicked(5))
my_button.place(x=x_, y=y_)

x_ += w_ + 9
my_button = Button(window, image = photo6,  height=w_, width=w_, command=lambda: button_clicked(6))
my_button.place(x=x_, y=y_)

x_ += w_ + 9
my_button = Button(window, image = photo7,  height=w_, width=w_, command=lambda: button_clicked(7))
my_button.place(x=x_, y=y_)

x_ += w_ + 9
my_button = Button(window, image = photo8,  height=w_, width=w_, command=lambda: button_clicked(8))
my_button.place(x=x_, y=y_)

## Third row
y_ += w_ + 9
x_ = 10
my_button = Button(window, image = photo9,  height=w_, width=w_, command=lambda: button_clicked(9))
my_button.place(x=x_, y=y_)

x_ += w_ + 9
my_button = Button(window, image = photo10,  height=w_, width=w_, command=lambda: button_clicked(10))
my_button.place(x=x_, y=y_)

x_ += w_ + 9
my_button = Button(window, image = photo11,  height=w_, width=w_, command=lambda: button_clicked(11))
my_button.place(x=x_, y=y_)

x_ += w_ + 9
my_button = Button(window, image = photo12,  height=w_, width=w_, command=lambda: button_clicked(12))
my_button.place(x=x_, y=y_)

## Fourth row
y_ += w_ + 9
x_ = 10
my_button = Button(window, image = photo13,  height=w_, width=w_, command=lambda: button_clicked(13))
my_button.place(x=x_, y=y_)

x_ += w_ + 9
my_button = Button(window, image = photo14,  height=w_, width=w_, command=lambda: button_clicked(14))
my_button.place(x=x_, y=y_)

x_ += w_ + 9
my_button = Button(window, image = photo15,  height=w_, width=w_, command=lambda: button_clicked(15))
my_button.place(x=x_, y=y_)

x_ += w_ + 9
my_button = Button(window, image = photo16,  height=w_, width=w_, command=lambda: button_clicked(16))
my_button.place(x=x_, y=y_)


##   15) Build the plan area

txtarea = Text(window, width=58, height=21)
txtarea.place(x=340, y=66)

##   16) Build the plots area
# label to show the image
imagebox = Label(window)
imagebox.place(x=10, y=410)


# Execute tkinter
window.mainloop()
