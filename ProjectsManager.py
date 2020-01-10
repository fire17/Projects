import pyqtgraph
from Vis import Funcs as F
from Vis import Poly as P
import random

## Add path to library (just for examples; you do not need this)
import pyqtgraph.examples.initExample

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
import sys, math
from PyQt5 import QtWidgets
#from Vis import *

def DisplayProjects(proj):
    return DisplayProjectsConsole(proj)

def DisplayProjectsConsole(proj):
    """Print Projcets to Console
    """
    print()
    for p in proj.keys():
        print(p,":")
        for label in proj[p]:

            val = proj[p][label]["value"]
            s = label+"("+str(val)+"): "
            if val is not None:
                for a in range(val):
                    s+="+"
            print (s)
        print()

projects = {}

projectNames = F.OpenProjects()[:3]
LabelsList = ["FTP", "Importance", "Practicality", "Effort", "Revenue", "Romantic"]
Labels = {}
for ll in LabelsList:
    Labels[ll] = {}
    Labels[ll]["weight"] = 1


for p in projectNames:
    projects[p] = {}
    for l in Labels.keys():
        projects[p][l] = {}
        x = random.randint(1,10)
        projects[p][l]["value"] = x*Labels[l]["weight"]
        projects[p]

DisplayProjects(projects)

#print("||||||||||||||||||||||||||||||||||||||||||||||||||")
#for p in projects:
#    print(projects[p])
#    print(len(projects[p]))
#print("||||||||||||||||||||||||||||||||||||||||||||||||||")
#print(projects)

import sys
app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.showMaximized()
w.setWindowTitle('pyqtgraph example: GLMeshItem')
w.setCameraPosition(distance=100)

ShowTop = True
newRand = True
trans = True
R = 20
spin = 0
dist = 40
dt =0

num = 3

i = 0
j = 0
for p in projectNames:
    #projects[p] = {}
    labelss = []
    for l in Labels.keys():
        labelss.append(projects[p][l]["value"])

    projectShapes, polyGList = P.GetProjectShapes(labelss,LabelN = random.randint(3,50), mode = random.randint(0,5)%5)

    for g in polyGList:
        g.translate(dist*i,dist*j,0)
        w.addItem(g)
        pass

    print(p, "XXXXXXXXXXXXXXXXXXXXXXXXx",len(labelss), labelss)
    i +=1

'''
for j in range(1):
    for i in range(num):
        labels = None
        projectShapes, polyGList = P.GetProjectShapes(labels,LabelN = random.randint(3,50), mode = random.randint(0,5)%5)

        for g in polyGList:
            g.translate(dist*i,dist*j,0)
            w.addItem(g)
            pass
'''


if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
    QtGui.QApplication.instance().exec_()
