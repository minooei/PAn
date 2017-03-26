import matplotlib.pyplot as plt
from Tkinter import *
import tkFileDialog
import matplotlib.path as mpath
import matplotlib
matplotlib.use('TkAgg')
from DraggablePoint import DraggablePoint
from contours import FindContours
from mypatches import MyCircle

class App:
    def __init__(self, master):
        self.mm = master
        frame = Frame(master)
        frame.pack(fill=BOTH, expand=YES)
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
        # self.myplot("/home/mohammad/Documents/software/cv-work/0scan/ds/0/p56.png")
        plt.clf()
        self.ax = plt.gca()
        self.fig = plt.gcf()

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
        Path = mpath.Path
        path_data = [
            (Path.MOVETO, [1, 2]),
            (Path.LINETO, [0, 2]),
            (Path.LINETO, [0, 3]),
            (Path.LINETO, [1, 3]),
            (Path.LINETO, [1, 4]),
            (Path.LINETO, [2, 4]),
            (Path.LINETO, [2, 3]),
            (Path.LINETO, [3, 3]),
            (Path.LINETO, [3, 2]),
            (Path.LINETO, [2, 2]),
            (Path.LINETO, [2, 1]),
            (Path.LINETO, [1, 1]),
            (Path.LINETO, [1, 2]),
            (Path.LINETO, [2, 3]),
            (Path.LINETO, [2, 2]),
            (Path.LINETO, [1, 3]),
            (Path.LINETO, [1, 2]),
            (Path.CLOSEPOLY, [1, 2])
        ]
        codes, verts = zip(*path_data)
        path = mpath.Path(verts, codes)

        f = self.zoom_factory(self.ax)

        img = plt.imread(ipath)
        s = img.shape
        implot = plt.imshow(img, extent=[0, img.shape[1], img.shape[0], 0])
        try:
            f = FindContours(ipath, self.add_points)
        except Exception:
            print Exception.message
            pass
        plt.show()

    def add_points(self, cnt):
        fig = plt.gcf()
        ax = fig.add_subplot(111)
        drs = []
        circles = [
            MyCircle(cnt[0], 1, 1, fc='r', alpha=0.2),
            MyCircle(cnt[1], 1, 1, fc='r', alpha=0.2),
            MyCircle(cnt[2], 1, 1, fc='r', alpha=0.2),
            MyCircle(cnt[3], 1, 1, fc='r', alpha=0.2)
        ]
        for circ in circles:
            ax.add_patch(circ)
            dr = DraggablePoint(circ)
            dr.connect()
            drs.append(dr)
        plt.show()

    def MyMenu(self, master):
        menu = Menu(master)
        root.config(menu=menu)

        file_menu = Menu(menu)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="open files", command=lambda: self.browse_for_file(master))
        file_menu.add_command(label="save", command=root.quit)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)

    def browse_for_file(self, master):
        files = tkFileDialog.askopenfilenames(parent=master, title='Open files',
                                              initialdir='/home/mohammad/Documents/software/cv-work/0scan/ds/0/')
        i = 0
        for f in files:
            self.lb.insert(i, f)
            i = i + 1
        print files

    def change_frame(self, param):
        pass


root = Tk()
root.wm_title("PAn")
# menu = App.MyMenu
app = App(root)
root.mainloop()
