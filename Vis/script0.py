# -*- coding: utf-8 -*-
"""
Simple examples demonstrating the use of GLMeshItem.

"""
import Funcs as F
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
        print(cc,pp);cc+=1

    print("len(poly)",len(poly))
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



## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication([])
    w = gl.GLViewWidget()
    w.showMaximized()
    w.setWindowTitle('pyqtgraph example: GLMeshItem')
    w.setCameraPosition(distance=100)





    g = gl.GLGridItem()
    g.scale(2,2,1)
    #w.addItem(g)



    ## Example 1:
    ## Array of vertex positions and array of vertex indexes defining faces
    ## Colors are specified per-face

    verts = np.array([
        [0, 0, 0],
        [2, 0, 0],
        [1, 2, 0],
        [1, 1, 1],
    ])
    faces = np.array([
        [0, 1, 2],
        [0, 1, 3],
        [0, 2, 3],
        [1, 2, 3]
    ])
    colors = np.array([
        [1, 0, 0, 0.3],
        [0, 1, 0, 0.3],
        [0, 0, 1, 0.3],
        [1, 1, 0, 0.3]
    ])

    ## Mesh item will automatically compute face normals.
    m1 = gl.GLMeshItem(vertexes=verts, faces=faces, faceColors=colors, smooth=False)
    m1.translate(5, 5, 0)
    m1.setGLOptions('additive')
#    w.addItem(m1)


    ## Example 2:
    ## Array of vertex positions, three per face
    verts = np.empty((36, 3, 3), dtype=np.float32)
    theta = np.linspace(0, 2*np.pi, 37)[:-1]
    verts[:,0] = np.vstack([2*np.cos(theta), 2*np.sin(theta), [0]*36]).T
    verts[:,1] = np.vstack([4*np.cos(theta+0.2), 4*np.sin(theta+0.2), [-1]*36]).T
    verts[:,2] = np.vstack([4*np.cos(theta-0.2), 4*np.sin(theta-0.2), [1]*36]).T

    ## Colors are specified per-vertex
    colors = np.random.random(size=(verts.shape[0], 3, 4))
    m2 = gl.GLMeshItem(vertexes=verts, vertexColors=colors, smooth=False, shader='balloon',
                       drawEdges=True, edgeColor=(1, 1, 0, 1))
    m2.translate(-5, 5, 0)
#    w.addItem(m2)



    ## Example 3:
    ## sphere

    md = gl.MeshData.sphere(rows=10, cols=20)
    #colors = np.random.random(size=(md.faceCount(), 4))
    #colors[:,3] = 0.3
    #colors[100:] = 0.0
    colors = np.ones((md.faceCount(), 4), dtype=float)
    colors[::2,0] = 0
    colors[:,1] = np.linspace(0, 1, colors.shape[0])
    md.setFaceColors(colors)
    m3 = gl.GLMeshItem(meshdata=md, smooth=False)#, shader='balloon')

    m3.translate(5, -5, 0)
#    w.addItem(m3)


    # Example 4:
    # wireframe

    md = gl.MeshData.sphere(rows=4, cols=8)
    m4 = gl.GLMeshItem(meshdata=md, smooth=False, drawFaces=False, drawEdges=True, edgeColor=(1,1,1,1))
    m4.translate(0,10,0)
#    w.addItem(m4)

    # Example 5:
    # cylinder
    md = gl.MeshData.cylinder(rows=10, cols=20, radius=[1., 2.0], length=5.)
    md2 = gl.MeshData.cylinder(rows=10, cols=20, radius=[2., 0.5], length=10.)
    colors = np.ones((md.faceCount(), 4), dtype=float)
    colors[::2,0] = 0
    colors[:,1] = np.linspace(0, 1, colors.shape[0])
    md.setFaceColors(colors)
    m5 = gl.GLMeshItem(meshdata=md, smooth=True, drawEdges=True, edgeColor=(1,0,0,1), shader='balloon')
    colors = np.ones((md.faceCount(), 4), dtype=float)
    colors[::2,0] = 0
    colors[:,1] = np.linspace(0, 1, colors.shape[0])
    md2.setFaceColors(colors)
    m6 = gl.GLMeshItem(meshdata=md2, smooth=True, drawEdges=False, shader='balloon')
    m6.translate(0,0,7.5)

    m6.rotate(0., 0, 1, 1)
    #m5.translate(-3,3,0)
#    w.addItem(m5)
#    w.addItem(m6)

#    widgett = MyWidget(sides = 5)
#    widgett.show()









    projectsN = 35
    LabelN = 7




    LabelsList = ["FTP", "Importance", "Practicality", "Effort", "Revenue", "Artistic", "f", "z", "x", "a"]
    for i in range(30):
        LabelsList.append(""+str(i))
    LabelsList = LabelsList[:LabelN]
    layers = 11
    R = 20
    n = len(LabelsList)
    mode = 3
    spin = 0
    spin = 1.6189
    dist = 1.4 # -1
    height = 3

    projects = {}

    projectNames = F.OpenProjects()[:projectsN]
    projectsGrid = int(math.sqrt(len(projectNames)))+1
    gridStep = 40
    offx = gridStep*(projectsGrid-projectsGrid%2)/2
    offy = gridStep*(projectsGrid-projectsGrid%2)/2


    Labels = {}
    for ll in LabelsList:
        Labels[ll] = {}
        Labels[ll]["weight"] = 1


    projectShapes = []
    psc=0

    for p in projectNames:

        polyList = []

        for l in range(layers):

            row = int(psc/projectsGrid) * gridStep - offx
            col = psc%projectsGrid * gridStep - offy
            polyg, poly = GetPolygon(n,gl, r = R/layers*(l+1), spin = (360/n)*l*spin , mode = (psc+1)%5, edges = False, bold = 0.3)
            polyList.append(poly)
            polyg.translate(row, col, ((layers-1)-l)*dist)
            w.addItem(polyg)


        newShape = [[0,0,0]]
        projects[p] = {}
        vc = 1
        v = random.randint(1,10)
        for l in Labels.keys():
            projects[p][l] = {}
            newRand = False
            if newRand:
                v = random.randint(1,10)
            else:
                v = v+  random.randint(-1,1)
                if v<1:v=2;
                if v>len(polyList)-1:v=len(polyList)-1;
            print(v,vc)
            print(polyList[v])
            #v = 10
            projects[p][l]["value"] = v*Labels[l]["weight"]
            newShape.append([polyList[v][vc][0],polyList[v][vc][1],0])
            vc+=1
        projectShapes.append(newShape)
            #projects[p]
        psc +=1

    psc=0
    for ps in projectShapes:
        mn, mshape = GetShape(ps, gl = gl, r = R, spin = spin, mode = psc%5, edges = True, bold = 0.5, edgeA = 0.3)




        row = int(psc/projectsGrid) * gridStep - offx
        col = psc%projectsGrid * gridStep - offy

        mn.translate(row, col, height+psc)
        #w.addItem(mn)
        psc+=1

    '''
    values = [10,1,7,1,10,1]
    vc=1
    newShape = [[0,0,0]]
    for ns in range(n):
        v = values[ns]
        newShape.append([polyList[v][vc][0],polyList[v][vc][1],0])

        vc+=1
    mn, mshape = GetShape(newShape, gl = gl, r = R, spin = spin, mode = mode, edges = True, bold = 1)
    mn.translate(0, 0, 10)
    #w.addItem(mn)
    '''









    verts = []
    faces = []
    colors = []

    for p in poly:
        verts.append([0,0,0])
        verts.append([p[0],p[1],0])
        verts.append([0,0,0])
    c = 0
    for f in range(int(len(verts)/3)):
        faces.append([0+c*3,1+c*3,2+c*3])
        colors.append([.8, .0, .9, 0.3])
        c+=1


    verts = np.array(verts)
    faces  = np.array(faces)
    colors = np.array(colors)

    mx2 = gl.GLMeshItem(vertexes=verts, faces=faces, faceColors=colors, smooth=False,drawEdges=True, edgeColor=(1, 1, 0, 1))
    #mx = gl.GLMeshItem(vertexes=verts)
    mx2.translate(0,0, 10)
    mx2.setGLOptions('additive')
    #w.addItem(mx2)





    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
