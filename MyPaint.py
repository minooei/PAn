import matplotlib.pyplot as plt

try:
    # for Python2
    from Tkinter import *
    import tkFileDialog
except ImportError:
    # for Python3
    from tkinter import *
    import tkinter.filedialog as tkFileDialog
import matplotlib
from collections import OrderedDict
from OutputDriver import OutputDriver
import numpy as np

matplotlib.use('TkAgg')
from DraggablePoint import DraggablePoint
from contours import FindContours
from mypatches import MyCircle
from matplotlib.backend_bases import NavigationToolbar2
import json
import matplotlib.lines as mlines
import cv2

sys.setrecursionlimit(10000)


class App:
    def __init__(self, master):
        self.mm = master
        frame = Frame(master)
        frame.pack(fill=BOTH, expand=YES)
        self.current = ''
        self.polygon = ''
        self.corners = OrderedDict()
        self.files = []
        self.pfiles = ['corners.json', 'files.json']
        self.menu = self.MyMenu(master)
        self.label = [0, 0, 0, 0]
        self.fix = [0, 0, 0, 0]
        self.button = Button(frame,
                             text="QUIT", fg="red",
                             command=quit)
        self.button.pack(side=BOTTOM)
        self.res = Label(frame, text="corners", fg="white")
        self.res.pack(side=BOTTOM)

        self.lb = Listbox(frame, name='lb', fg="white")
        self.lb.bind('<<ListboxSelect>>', self.onselect)
        self.lb.config(width=0, height=0)
        self.lb.pack(side=TOP)

        plt.clf()
        self.ax = plt.gca()
        self.fig = plt.gcf()
        self.drawing = False
        self.ix, self.iy = -1, -1

    def onselect(self, evt):
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        print('You selected item %d: "%s"' % (index, value))
        self.myplot(value)

    def update_corner(self, num, value):
        self.fix[num] = value
        self.res.config(text=('corners:', self.fix))

    def myplot(self, ipath):

        self.img = cv2.imread(ipath)
        height, width = self.img.shape[:2]

        self.mask = np.zeros((height, width, 3), np.uint8)

        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.draw_circle)
        while (1):
            cv2.imshow('image', self.img)
            k = cv2.waitKey(1) & 0xFF
            if k == 27:
                break
        cv2.destroyAllWindows()

    def saveProject(self):
        with open(self.pfiles[0], 'w') as fp:
            json.dump(self.corners, fp, indent=4)
        with open(self.pfiles[1], 'w') as fp:
            json.dump(self.files, fp, indent=4)
        output = OutputDriver(self.corners)
        output.exportToFile()

    def loadProject(self, master):
        self.pfiles = tkFileDialog.askopenfilenames(parent=master, title='Open files',
                                                    initialdir='/home/mohammad/Documents/software/cv-work/0scan/ds/0/')
        temp = self.pfiles[0]
        if "corners.json" in self.pfiles[1]:
            self.pfiles[0] = self.pfiles[1]
            self.pfiles[1] = temp
        with open(self.pfiles[0], 'r') as fp:
            self.corners = json.load(fp)
        with open(self.pfiles[1], 'r') as fp:
            self.files = json.load(fp)
        self.showFiles()

    def MyMenu(self, master):
        menu = Menu(master)
        root.config(menu=menu)

        file_menu = Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="open files", command=lambda: self.browse_for_file(master))
        file_menu.add_command(label="save project", command=lambda: self.saveProject())
        file_menu.add_command(label="load project", command=lambda: self.loadProject(master))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)

    def browse_for_file(self, master):
        self.files = tkFileDialog.askopenfilenames(parent=master, title='Open files',
                                                   initialdir='/home/mohammad/software/sources/sync/0scan/ds/0/')
        i = 0
        for f in self.files:
            self.lb.insert(i, f)
            i = i + 1
            name = f.split("/")
            name = name[len(name) - 1]
            if name in self.corners:
                pass
            else:
                self.corners[name] = {}

    def showFiles(self):
        i = 0
        for f in self.files:
            self.lb.insert(i, f)
            i = i + 1

    def draw_circle(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.ix, self.iy = x, y
            # cv2.circle(self.img, (x, y), 5, (55, 55, 0), -1)
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing:
                cv2.line(self.mask, (self.ix, self.iy), (x, y), (255, 255, 255), 5)
                cv2.line(self.img, (self.ix, self.iy), (x, y), (255, 255, 255), 5)
                self.ix, self.iy = x, y
                # cv2.circle(self.img, (x, y), 5, (0, 255, 0), -1)
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            # cv2.circle(self.img, (x, y), 5, (0, 0, 255), -1)
            cv2.line(self.mask, (self.ix, self.iy), (x, y), (255, 255, 255), 5)
            cv2.line(self.img, (self.ix, self.iy), (x, y), (255, 255, 255), 5)

            cv2.imwrite("mask.png", self.mask)


global app
root = Tk()
root.minsize(300, 300)
root.wm_title("PAn")
# menu = App.MyMenu
app = App(root)
root.mainloop()
