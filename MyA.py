import matplotlib.pyplot as plt
from Tkinter import *
import tkFileDialog
import matplotlib
from collections import OrderedDict
from OutputDriver import OutputDriver

matplotlib.use('TkAgg')
from DraggablePoint import DraggablePoint
from contours import FindContours
from mypatches import MyCircle
from matplotlib.backend_bases import NavigationToolbar2
import json

sys.setrecursionlimit(10000)

class App:
    def __init__(self, master):
        self.mm = master
        frame = Frame(master)
        frame.pack(fill=BOTH, expand=YES)
        self.corners = OrderedDict()
        self.files = []
        self.pfiles = ['corners.json','files.json']
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
        f = self.zoom_factory(self.ax)

    #     self.fig.canvas.mpl_connect('key_press_event', self.press)
    #
    # def press(*args, **kwargs):
    #     print args[1].key

    def onselect(self, evt):
        # Note here that Tkinter passes an event object to onselect()
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        print 'You selected item %d: "%s"' % (index, value)
        self.myplot(value)

    def update_corner(self, num, value):
        self.fix[num] = value
        self.res.config(text=('corners:', self.fix))

    def zoom_factory(ax, base_scale=2.):
        ax = plt.gca()

        def zoom_fun(event):
            # get the current x and y limits
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()
            cur_xrange = (cur_xlim[1] - cur_xlim[0]) * .5
            cur_yrange = (cur_ylim[1] - cur_ylim[0]) * .5
            xmouse = event.xdata  # get event x location
            ymouse = event.ydata  # get event y location
            cur_xcentre = (cur_xlim[1] + cur_xlim[0]) * .5
            cur_ycentre = (cur_ylim[1] + cur_ylim[0]) * .5
            xdata = cur_xcentre + 0.25 * (xmouse - cur_xcentre)
            ydata = cur_ycentre + 0.25 * (ymouse - cur_ycentre)
            if event.button == 'up':
                # deal with zoom in
                scale_factor = .5
            elif event.button == 'down':
                # deal with zoom out
                scale_factor = 1.2
            else:
                # deal with something that should never happen
                scale_factor = 1
                print event.button
            # set new limits
            ax.set_xlim([xdata - cur_xrange * scale_factor,
                         xdata + cur_xrange * scale_factor])
            ax.set_ylim([ydata - cur_yrange * scale_factor,
                         ydata + cur_yrange * scale_factor])
            plt.draw()  # force re-draw

        # fig = ax.get_figure()
        # attach the call back
        plt.gcf().canvas.mpl_connect('scroll_event', zoom_fun)

        # return the function
        return zoom_fun

    def myplot(self, ipath):
        plt.cla()
        # Path = mpath.Path
        # path_data = [
        #     (Path.MOVETO, [1, 2]),
        #     (Path.LINETO, [0, 2]),
        #     (Path.LINETO, [0, 3]),
        #     (Path.LINETO, [1, 3]),
        #     (Path.LINETO, [1, 4]),
        #     (Path.LINETO, [2, 4]),
        #     (Path.LINETO, [2, 3]),
        #     (Path.LINETO, [3, 3]),
        #     (Path.LINETO, [3, 2]),
        #     (Path.LINETO, [2, 2]),
        #     (Path.LINETO, [2, 1]),
        #     (Path.LINETO, [1, 1]),
        #     (Path.LINETO, [1, 2]),
        #     (Path.LINETO, [2, 3]),
        #     (Path.LINETO, [2, 2]),
        #     (Path.LINETO, [1, 3]),
        #     (Path.LINETO, [1, 2]),
        #     (Path.CLOSEPOLY, [1, 2])
        # ]
        # codes, verts = zip(*path_data)
        # path = mpath.Path(verts, codes)
        img = plt.imread(ipath)
        s = img.shape
        implot = plt.imshow(img, extent=[0, img.shape[1], img.shape[0], 0])
        # try:
        F = FindContours(ipath)
        cnt = F.find(ipath)
        name = ipath.split("/")
        self.addPoints(cnt, name[len(name) - 1])
        # except Exception:
        #     print Exception.message
        #     pass
        plt.show()

    def addPoints(self, cnt, name):
        print 'trying adding point'
        fig = plt.gcf()
        ax = fig.add_subplot(111)
        drs = []

        crs = ["tl", "bl", "br", "tr"]
        i = 0
        for cr in crs:
            if cr in self.corners[name]:
                pass
            else:
                self.corners[name][cr] = cnt[i]
            i = i + 1

        circles = [
            MyCircle(self.corners[name]["tl"], 2, 2, "tl", name, fc='r', alpha=0.1),
            MyCircle(self.corners[name]["bl"], 2, 2, "bl", name, fc='g', alpha=0.1),
            MyCircle(self.corners[name]["br"], 2, 2, "br", name, fc='b', alpha=0.1),
            MyCircle(self.corners[name]["tr"], 2, 2, "tr", name, fc='m', alpha=0.1)
        ]

        for circ in circles:
            ax.add_patch(circ)
            dr = DraggablePoint(circ, cb=self.onSetPoint)
            dr.connect()
            drs.append(dr)
        plt.show()

    def onSetPoint(self, point):
        self.corners[point.name][point.corner] = point.center
        print point.corner
        print self.corners

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
        temp=self.pfiles[0]
        if "corners.json" in self.pfiles[1]:
            self.pfiles[0]=self.pfiles[1]
            self.pfiles[1]=temp
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
                                                   initialdir='/home/mohammad/Documents/software/cv-work/0scan/ds/0/')
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


def nextImage(self, *args, **kwargs):
    print 'next'
    idx = app.lb.curselection()[0]
    ln = len(app.lb.get(0, END))
    print ln
    if idx < ln - 1:
        idx = idx + 1
    app.lb.selection_clear(0, END)
    app.lb.selection_set(idx)
    app.lb.select_set(idx)
    app.lb.event_generate("<<ListboxSelect>>")


def prevImage(self, *args, **kwargs):
    print 'prev'
    idx = app.lb.curselection()[0]
    print idx
    if idx > 0:
        idx = idx - 1
    app.lb.selection_clear(0, END)
    app.lb.selection_set(idx)
    app.lb.select_set(idx)
    app.lb.event_generate("<<ListboxSelect>>")


NavigationToolbar2.back = prevImage
NavigationToolbar2.forward = nextImage
global app
root = Tk()
root.minsize(300, 300)
root.wm_title("PAn")
# menu = App.MyMenu
app = App(root)
root.mainloop()
