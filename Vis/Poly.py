# -*- coding: utf-8 -*-
"""
Simple examples demonstrating the use of GLMeshItem.

"""
from Vis import Funcs as F
import random
## Add path to library (just for examples; you do not need this)
import pyqtgraph.examples.initExample

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
import sys, math
from PyQt5 import QtWidgets

def GetPolygon(n=5, gl = None, r = 15, spin = 0, mode = 0, edges = True, bold=.05):
    pl = createPoly(n, r = r, s = spin)
    poly = [[0,0,0]]

    cc = 1
    for pp in pl:
        poly.append([pp[0], pp[1],0])
    #    print(cc,pp);cc+=1

    #print("len(poly)",len(poly))
    return GetShape(poly, gl = gl, r = r, spin = spin, mode = mode, edges = edges, bold = bold)

def GetShape(shape, gl = None, r = 15, spin = 0, mode = 0, edges = True, bold = .05, edgeA = 0.17):

        face = []
        color = []
        n = len(shape)-1
        cn = 1/(n+3)
        c = 1
        for f in range(n):
            if c >= n:
                face.append([0,c,1])
            else:
                face.append([0,c,c+1])

            if mode is 0:
                color.append([.5, 0.3, .9, bold])
            elif mode is 1:
                color.append([.8-c*cn*r, c*cn, .9, bold])
            elif mode is 2:
                color.append([.8-c*cn*r, c*cn, .9-c*cn*0.1*r, bold])
            elif mode is 3:
                color.append([.6-(c*cn*r)/10, c*cn, .9-(c*cn*0.1)/2, bold])
            elif mode is 4:
                color.append([.1*(r/2), c*cn*r*0.05, .15*(c*cn*r*0.1)/2, bold])
            elif mode is 5:
                mode = 0
            #mode+=1
            c+=1

        verts = np.array(shape)
        faces = np.array(face)
        colors = np.array(color)

        ## Mesh item will automatically compute face normals.
        #mx = gl.GLMeshItem(vertexes=verts, faces=faces, faceColors=colors, smooth=False)
        if edges:
            mx = gl.GLMeshItem(vertexes=verts, faces=faces, faceColors=colors, smooth=False ,drawEdges=True, edgeColor=(1, 1, 0, edgeA))
        else:
            mx = gl.GLMeshItem(vertexes=verts, faces=faces, faceColors=colors, smooth=False)
        #mx = gl.GLMeshItem(vertexes=verts)
        mx.translate(0,0, 0)
        mx.setGLOptions('additive')
        return mx, shape


def createPoly(n, r = 15, s=0):
    #polygon = QtGui.QPolygonF()
    w = 360/n                                                       # angle per step
    xy = []
    for i in range(n):                                              # add the points of polygon
        t = w*i + s
        x = r*math.cos(math.radians(t))
        y = r*math.sin(math.radians(t))
        xy.append([x,y])
    return xy

class MyWidget(QtWidgets.QWidget):
    def __init__(self, sides, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.pen = QtGui.QPen(QtGui.QColor(0,0,0))                      # set lineColor
        self.pen.setWidth(3)                                            # set lineWidth
        self.brush = QtGui.QBrush(QtGui.QColor(255,255,255,255))        # set fillColor
        self.polygon = self.createPoly(sides,260,18)                         # polygon with n points, radius, angle of the first point

    def createPoly(self, n, r, s):
        polygon = QtGui.QPolygonF()
        w = 360/n                                                       # angle per step
        for i in range(n):                                              # add the points of polygon
            t = w*i + s
            x = r*math.cos(math.radians(t))
            y = r*math.sin(math.radians(t))
            polygon.append(QtCore.QPointF(self.width()/2 +x, self.height()/2 + y))

        return polygon

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.drawPolygon(self.polygon)

LL = ["FTP", "Importance", "Practicality", "Effort", "Revenue", "Artistic", "f", "z", "x", "a"]

def GetProjectShapes(labels, LabelN = 3, mode = 4):

    global LL
    if labels is None:
        LabelsList = LL
    else:
        LabelsList = labels
        LabelN = len(labels)
    projectsN = 1
    #LabelN = 3
    layers = 13
    R = 20
    #mode = 3
    spin = 0
    #dist = 40
    #spin = 1.6189
    dist = 1.4 # -1
    height = 3
    gridStep = 40
    backBold = 0.07
    under = 12
    trans = True
    newRand = False
    ShowTop = True


    #for i in range(30):
    #    LabelsList.append(""+str(i))
    LabelsList = LabelsList[:LabelN]
    n = len(LabelsList)

    projects = {}

    projectNames = F.OpenProjects()[:projectsN]
    projectsGrid = int(math.sqrt(len(projectNames)))+1
    offx = gridStep*(projectsGrid-projectsGrid%2)/2
    offy = gridStep*(projectsGrid-projectsGrid%2)/2


    #Labels = {}
    #for ll in LabelsList:
    #    Labels[ll] = {}
    #    Labels[ll]["weight"] = 1


    projectShapes = []
    psc=0

    polyGList = []

    for p in projectNames:

        polyList = []

        for l in range(layers):

            row = int(psc/projectsGrid) * gridStep - offx
            col = psc%projectsGrid * gridStep - offy
            polyg, poly = GetPolygon(n,gl, r = R/layers*(l+1), spin = (360/n)*l*spin , mode = mode%5, edges = False, bold = backBold)
            polyList.append(poly)
            if trans:
                polyg.translate(row, col, ((layers-1)-l)*dist- under)
            #w.addItem(polyg)
            polyGList.append(polyg)


        newShape = [[0,0,0]]
        projects[p] = {}
        vc = 1
        v = random.randint(1,10)
        #print(labels)
        for l in range(len(labels)):
        #    print("LLLLLLLL")
            #projects[p][l] = {}
            if newRand:
                v = random.randint(1,10)
            else:
                v = v+  random.randint(-1,1)
                if v<1:v=2;
                if v>len(polyList)-1:v=len(polyList)-1;
            #print(v,vc)
            #print(polyList[v])

            #v = 10
            if labels is not None:
                v = labels[l]
                #print(v)
            #projects[p][l]["value"] = v*Labels[l]["weight"]
            newShape.append([polyList[v][vc][0],polyList[v][vc][1],0])
            vc+=1
        projectShapes.append(newShape)

            #projects[p]
        psc +=1

        psc=0
        for ps in projectShapes:
            mn, mshape = GetShape(ps, gl = gl, r = R, spin = spin, mode = (mode-1)%5, edges = True, bold = 0.5, edgeA = 0.3)





            if trans:
                row = int(psc/projectsGrid) * gridStep - offx
                col = psc%projectsGrid * gridStep - offy
                mn.translate(row, col, height+psc)
            if ShowTop:
                polyGList.append(mn)
                #w.addItem(mn)
            psc+=1

    return projectShapes, polyGList

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication([])
    w = gl.GLViewWidget()
    w.showMaximized()
    w.setWindowTitle('pyqtgraph example: GLMeshItem')
    w.setCameraPosition(distance=100)

    ShowTop = True
    newRand = True
    trans = True
    #R = 20

    dt =0

    num = 3

    for j in range(num):
        for i in range(num):
            labels = None
            projectShapes, polyGList = GetProjectShapes(labels,LabelN = random.randint(3,50), mode = random.randint(0,5)%5)

            for g in polyGList:
                g.translate(dist*i,dist*j,0)
                w.addItem(g)
                pass



    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
