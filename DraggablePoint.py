class DraggablePoint:
    lock = None  # only one can be animated at a time

    def __init__(self, point, **kwargs):
        # print 'init'
        self.cb = kwargs.get("cb", 0)
        self.point = point
        self.press = None
        self.background = None

    def connect(self):
        # print 'connect to all the events we need'
        self.cidpress = self.point.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.point.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.point.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        if event.inaxes != self.point.axes: return
        if DraggablePoint.lock is not None: return
        contains, attrd = self.point.contains(event)
        if not contains: return
        self.press = (self.point.center), event.xdata, event.ydata
        print (self.press)
        DraggablePoint.lock = self

        # print 'draw everything but the selected rectangle and store the pixel buffer'
        canvas = self.point.figure.canvas
        axes = self.point.axes
        self.point.set_animated(True)
        canvas.draw()
        self.background = canvas.copy_from_bbox(self.point.axes.bbox)

        # print 'now redraw just the rectangle'
        axes.draw_artist(self.point)

        # print 'and blit just the redrawn area'
        canvas.blit(axes.bbox)

    def on_motion(self, event):
        if DraggablePoint.lock is not self:
            return
        if event.inaxes != self.point.axes: return
        self.point.center, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        self.point.center = (self.point.center[0] + dx, self.point.center[1] + dy)

        canvas = self.point.figure.canvas
        axes = self.point.axes
        # print 'restore the background region'
        canvas.restore_region(self.background)

        # print 'redraw just the current rectangle'
        axes.draw_artist(self.point)

        # print 'blit just the redrawn area'
        canvas.blit(axes.bbox)

    def on_release(self, event):
        # print 'on release we reset the press data'
        if DraggablePoint.lock is not self:
            return
        # print self.point.center
        self.cb(self.point)
        self.press = None
        DraggablePoint.lock = None

        # turn off the rect animation property and reset the background
        self.point.set_animated(False)
        self.background = None

        # redraw the full figure
        self.point.figure.canvas.draw()

    def disconnect(self):
        # print 'disconnect all the stored connection ids'
        self.point.figure.canvas.mpl_disconnect(self.cidpress)
        self.point.figure.canvas.mpl_disconnect(self.cidrelease)
        self.point.figure.canvas.mpl_disconnect(self.cidmotion)
