import matplotlib.patches as patches
import matplotlib.transforms as transforms
import matplotlib.path as mpath

class MyCircle(patches.Patch):
    def __str__(self):
        return "Ellipse(%s,%s;%sx%s)" % (self.center[0], self.center[1],
                                         self.width, self.height)

    def __init__(self, xy, width, height, angle=0.0, **kwargs):
        patches.Patch.__init__(self, **kwargs)

        self.center = xy
        self.width, self.height = width, height
        self.angle = angle
        self._path = patches.Path.unit_circle()
        # Note: This cannot be calculated until this is added to an Axes
        self._patch_transform = transforms.IdentityTransform()

    def _recompute_transform(self):
        """NOTE: This cannot be called until after this has been added
                 to an Axes, otherwise unit conversion will fail. This
                 maxes it very important to call the accessor method and
                 not directly access the transformation member variable.
        """
        center = (self.convert_xunits(self.center[0]),
                  self.convert_yunits(self.center[1]))
        width = self.convert_xunits(self.width)
        height = self.convert_yunits(self.height)
        self._patch_transform = transforms.Affine2D() \
            .scale(width * 0.5, height * 0.5) \
            .rotate_deg(self.angle) \
            .translate(*center)

    def get_path(self):
        """
        Return the vertices of the rectangle
        """
        Path = mpath.Path
        path_data = [
            (Path.MOVETO, [0, 0]),
            (Path.LINETO, [-1.5, 1.5]),
            (Path.LINETO, [-1.5, -1.5]),
            (Path.LINETO, [1.5, 1.5]),
            (Path.LINETO, [1.5, -1.5]),
            (Path.LINETO, [-1.5, -1.5]),
            (Path.LINETO, [-3.5, -1.5]),
            (Path.LINETO, [-3.5, 1.5]),
            (Path.LINETO, [-1.5, 1.5]),
            (Path.LINETO, [-1.5, 3.5]),
            (Path.LINETO, [ 1.5, 3.5]),
            (Path.LINETO, [ 1.5, 1.5]),
            (Path.LINETO, [3.5,  1.5]),
            (Path.LINETO, [3.5, -1.5]),
            (Path.LINETO, [ 1.5, -1.5]),
            (Path.LINETO, [ 1.5, -3.5]),
            (Path.LINETO, [-1.5, -3.5]),
            (Path.LINETO, [-1.5, -1.5]),
            (Path.CLOSEPOLY, [-1.5, -1.5])
        ]
        codes, verts = zip(*path_data)
        path = mpath.Path(verts , codes)
        self._path=path
        return self._path

    def get_patch_transform(self):
        self._recompute_transform()
        return self._patch_transform
