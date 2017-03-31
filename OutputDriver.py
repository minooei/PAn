import datetime


class OutputDriver(object):
    """
    Very simple driver for XML result output.
    """

    def __init__(self, corners):
        self.source_sample_file = "data"
        self.software_used = "pan"
        self.software_version = "1"
        # self.segmentation_results = []
        self.corners = corners
        self.xmlfile = "/home/mohammad/Documents/software/cv-work/0scan/gt.xml"

    def exportToFile(self):
        with open(self.xmlfile, "w") as out:
            out.write("<?xml version='1.0' encoding='utf-8'?>\n")
            out.write("<seg_result version=\"0.2\" generated=\"%s\">\n" % datetime.datetime.now().isoformat())
            out.write("  <software_used name=\"%s\" version=\"%s\"/>\n" % (self.software_used, self.software_version))
            out.write("  <source_sample_file>%s</source_sample_file>\n" % self.source_sample_file)
            out.write("  <segmentation_results>\n")
            fidx = 1
            for name in self.corners:
                # if rejected:
                #     out.write("    <frame index=\"%d\" rejected=\"true\"/>\n" % fidx)
                # else:
                out.write("    <frame index=\"%d\" rejected=\"false\">\n" % fidx)
                out.write("       <point name=\"bl\" x=\"%f\" y=\"%f\"/>\n" % (self.corners[name]['bl'][0], self.corners[name]['bl'][1]))
                out.write("       <point name=\"tl\" x=\"%f\" y=\"%f\"/>\n" % (self.corners[name]['tl'][0], self.corners[name]['tl'][1]))
                out.write("       <point name=\"tr\" x=\"%f\" y=\"%f\"/>\n" % (self.corners[name]['tr'][0], self.corners[name]['tr'][1]))
                out.write("       <point name=\"br\" x=\"%f\" y=\"%f\"/>\n" % (self.corners[name]['br'][0], self.corners[name]['br'][1]))
                out.write("    </frame>\n")
                fidx = fidx + 1
            out.write("  </segmentation_results>\n")
            out.write("</seg_result>\n")
