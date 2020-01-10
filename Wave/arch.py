#nodes
#manager
import time
import random
from threading import Thread
import cv2
import numpy as np

def delaySum( lis):
    sum = 0
    for a in lis:
        sum+=a
    return sum

states = ["green", "flashing", "amber", "red", "ready"]
trafficStates = [(0,0,1),(0,2,0),(0,1,0),(1,0,0),(1,1,0)]
RAG = [((0,0,70),(0,0,255)) , ((0,100,100),(0,255,255), (0,255,255)) , ((0,70,0),(0,255,0))]
#defaultSeq = [7,3.25,1.25,4,1]
defaultSeq = [9,3.25,1.25,3,1]
#print(delaySum(defaultSeq),"XXXXXXXXXXXXXXXX")
t2Seq = list()
t2Seq.append(defaultSeq[-2]-defaultSeq[-1]-(defaultSeq[1]+defaultSeq[2]))
t2Seq.append(defaultSeq[1])
t2Seq.append(defaultSeq[2])
t2Seq.append(defaultSeq[-1]+defaultSeq[0]+defaultSeq[1]+defaultSeq[2])
t2Seq.append(defaultSeq[-1])
#print(delaySum(t2Seq),"XXXXXXXXXXXXXXXX")
#defaultSeq = [==7==,3.25,1.25,   ==4==,            1 ][7,3.25,1.25,4,1 ][7,3.25,1.25,4,1 ]
#defaultSeq =                      1][.5,3.25,1.25, 7              ,1][.5,3.25,1.25,7,1]

colors = states
colors = [
(0, 240, 59)[::-1],
##(0, 0, 0)[::-1],
#(183, 234, 59)[::-1],
(255, 175, 0)[::-1],
#(0, 0, 0)[::-1],
(255, 175, 0)[::-1],
#(0, 0, 0)[::-1],
(210, 0, 15)[::-1],
##(0, 0, 0)[::-1],
(255, 103, 0)[::-1]
]

class Eye(object):
    def __init__(self, args):
        self.StartTime = time.time()
        self.Manager = args["Manager"]

        self.Seq = args["Seq"]
        #self.Seq = [1,1,1,1,1]
        self.Distace = args["Distance"]
        self.DelayUnit = args["DelayUnit"]
        self.RandomError = random.choice([1]) * random.random()*(1/pow(10,random.randint(1,3)))
        self.RandomError = 0
        self.Correction = self.CorrectTime()

        self.Color = None
        self.state = -1
        self.Run = False
        #self.ID = args["ID"]
        self.StartRun()

    def genImg(self, h = 300 , w = 100, cs = 8):

        img = np.zeros((h,w,3), np.uint8)
        a,b,c = (w//2,h//6),(w//2,h//2),(w//2,h*5//6)

        #img = cv2.circle(img, a, cs, RAG[0][tlight.R], -1)
        #img = cv2.circle(img, b, cs, RAG[1][tlight.A], -1)
        img = cv2.circle(img, c, cs, self.Color, -1)
        return img

    def Start(self):
        self.Run = True

    def StartRun(self):
        t = Thread(target = self.StartEye)
        t.start()

    def StartEye(self):
        global states
        global colors

        while(not self.Run):
            time.sleep(0.001)
            #print(self.Distace)


        self.state = 0
        stateCounter = 0
        ln = len(self.Seq)

        time.sleep(self.RandomError)

        time.sleep(self.Distace * self.DelayUnit)

        while(self.Run):
            t = time.time()
            self.state = stateCounter % ln
            self.HandleState()

            stateCounter+=1 # overflow
            slp = self.Seq[self.state]-self.Correction
            self.Correction = 0
            fin = time.time()

            slp = slp - (fin-t)
            #print(self.Distace, self.Color, "- holding ",slp)
            time.sleep(slp - (time.time()-fin))

        self.state = None

    def HandleState(self):
        global colors
        self.Color = colors[self.state] # change color based on state


    def CorrectTime(self):
        #Todo: ask self.Manager to sync
        self.Correction = self.RandomError
        return self.Correction


class TrafficLight(object):
    def __init__(self,args):
        self.R = False
        self.A = False
        self.G = False
        self.Seq = args["Seq"]
        self.Run = True
        self.startState = args["startState"]
        self.Start()

    def Start(self):
        t = Thread(target = self.StartTraffic)
        t.start()

    def StartTraffic(self):
        global states
        global trafficStates
        global colors

        delayS = delaySum(self.Seq)
        self.state = self.startState #4
        stateCounter = self.state
        ln = len(self.Seq)

        while(self.Run):
            t = time.time()
            self.state = stateCounter % ln
            self.HandleState()

            stateCounter+=1 # overflow
            slp = self.Seq[self.state]
            #print("SSSSSSSSSS",slp,self.Seq)
            fin = time.time()
            slp = slp - (fin-t)
            #print("SSSSSSSSSS",slp)
            #print("Traffic Light", states[self.state],[self.R, self.A, self.G], "- holding ",slp)
            time.sleep((slp - (time.time()-fin))%delayS)

        self.state = None

    def HandleState(self):
        global colors
        self.R, self.A, self.G = trafficStates[self.state] # change color based on state
        if self.A is 2:
            t = Thread(target = self.flash)
            t.start()

    def flash(self):
        delay = self.Seq[self.state]/4
        time.sleep(delay)
        self.A = 0
        time.sleep(delay)
        self.A = 1
        time.sleep(delay)
        self.A = 0

class Dyn(object):
    pass

class Viewer(object):
    def __init__(self, args):
        self.tlight = args["tlight"]
        self.Manager = args["Manager"]
        self.Run = True
        self.args = args
        t = Thread(target = self.start)
        #t.start()

    def genHorImg(sezlf, h = 100 , w = 300, cs = 8):

        img = np.zeros((h,w,3), np.uint8)
        a,b,c = (w//2,h//6),(w//2,h//2),(w//2,h*5//6)

        #img = cv2.circle(img, a, cs, RAG[0][tlight.R], -1)
        #img = cv2.circle(img, b, cs, RAG[1][tlight.A], -1)
        img = cv2.circle(img, c, cs, self.Color, -1)
        return img

    def genTLightImg(self, tlight, h = 300 , w = 100, cs = 25):

        img = np.zeros((h,w,3), np.uint8)
        a,b,c = (w//2,h//6),(w//2,h//2),(w//2,h*5//6)

        img = cv2.circle(img, a, cs, RAG[0][tlight.R], -1)
        img = cv2.circle(img, b, cs, RAG[1][tlight.A], -1)
        img = cv2.circle(img, c, cs, RAG[2][tlight.G], -1)
        return img
    def start(self):
        t = Thread(target = self.startViewerSimple)
        t.start()
        ts = Thread(target = self.startViewer4Way)
        ts.start()
    def startViewer(self):
        #return self.startViewerSimple()
        return self.startViewer4Way()
    def putOnImg(self, bigImg, smallImg, loc):
        h2,w2,s = smallImg.shape
        h,w = loc
        h2+=h
        w2+=w
        bigImg[h:h2,w:w2] = smallImg
        return bigImg
    def startViewer4Way(self):

        rec = None
        newSeq = list()
        global RAG
        global states
        h = 300; lw = 100; ew = 30
        h = 60; lw = 20

        EyeNums = len(self.Manager.Eyes)
        A,B = Dyn(), Dyn()

        A.fromY, A.toY = 105, 1200
        A.fromX, A.toX = 1473, 1030

        A.fromY, A.toY = 90, 1200
        A.fromX, A.toX = 1480, 1030

        A.jumpsX = int((A.toX-A.fromX)//EyeNums*1.2)
        A.jumpsY = int((A.toY-A.fromY)//EyeNums*1.2)

        A.minSize = 3
        A.maxSize = 14
        A.sizeJump = (A.maxSize-A.minSize)/EyeNums

        B.fromY, B.toY = 45, -170
        B.fromX, B.toX = 1330, 1830

        B.jumpsX = ((B.toX-B.fromX)/EyeNums*0.8)
        B.jumpsY = ((B.toY-B.fromY)/EyeNums*0.8)

        B.minSize = 3
        B.maxSize = 1
        B.sizeJump = (B.maxSize-B.minSize)/EyeNums

        Lines = list()
        Lines.append(A)
        Lines.append(B)


        cs = 5
        while(self.Run):
            limg = self.genTLightImg(self.tlight, h = h, w = lw, cs = 5)
            W = ew*EyeNums+lw
            bigImg = cv2.imread('D:\\Projects\\Wave\\road2.jpg')
            #print(bigImg)
            #cv2.imshow(self.args["name"], bigImg)
            #c = cv2.waitKey(0)
            #bigImg = np.zeros((h,W,3), np.uint8)
            whiteImg = np.zeros((h+2,lw+2,3), np.uint8)
            whiteImg[:,:] = (255,255,255)
            bigImg = self.putOnImg(bigImg,whiteImg,(19,1399))
            bigImg = self.putOnImg(bigImg,limg,(20,1400))

            #bigImg[:,:lw] = limg
            c = 2

            for e in self.Manager.Eyes[::-1]:
                for L in Lines:
                    cloc = (int(L.fromX+L.jumpsX*c*(c*.1)),int(L.fromY+L.jumpsY*c*(c*.1)))
                    #cloc = (int(fromX+jumpsX*c),int(fromY+jumpsY*c))
                    cs = int(L.minSize+L.sizeJump*c)
                    #jumpsX*=1.01
                    #jumpsY*=1.01
                    #print(cloc)
                    bigImg = cv2.circle(bigImg, cloc, int(cs*1.3)+1, (0,0,0), -1)
                    bigImg = cv2.circle(bigImg, cloc, int(cs), e.Color, -1)
                #bigImg[:,lw+c*ew:lw+c*ew+ew] = e.genImg(w = ew)
                c+=1

            cv2.imshow(self.args["name"]+"X", bigImg)
            c = cv2.waitKey(1)




            if c is 32:
                lastRec = rec
                rec = time.time()
                if lastRec is not None:
                    newSeq.append(rec-lastRec)

                if len(newSeq) is len(states):
                    self.Manager.UpdateSeq(newSeq)
                    for i in range(20):
                        print("starting wave")
                    self.Manager.StartAllEyes()
                print(c)
                print("QQQQQQQQQ")
            elif c is 99:
                self.Run = False
                self.Manager.StopAllEyes()
                self.tlight.Run = False
                self.args["run"] = False
            elif c is 13:
                for i in range(20):
                    print("starting wave")
                self.Manager.StartAllEyes()
            elif c is not -1:
                print(c)


    def startViewerSimple(self):
        rec = None
        newSeq = list()
        global RAG
        global states
        h = 300; lw = 100; ew = 30
        while(self.Run):
            limg = self.genTLightImg(self.tlight, h = h, w = lw)
            EyeNums = len(self.Manager.Eyes)
            W = ew*EyeNums+lw
            bigImg = np.zeros((h,W,3), np.uint8)
            bigImg[:,:lw] = limg
            c = 0
            for e in self.Manager.Eyes[::-1]:
                bigImg[:,lw+c*ew:lw+c*ew+ew] = e.genImg(w = ew,cs = 5)
                c+=1


            cv2.imshow(self.args["name"],  cv2.flip(bigImg, 1))
            c = cv2.waitKey(1)
            if c is 32:
                lastRec = rec
                rec = time.time()
                if lastRec is not None:
                    newSeq.append(rec-lastRec)

                if len(newSeq) is len(states):
                    self.Manager.UpdateSeq(newSeq)
                    for i in range(20):
                        print("starting wave")
                    self.Manager.StartAllEyes()
                print(c)
                print("QQQQQQQQQ")
            elif c is 99:
                self.Run = False
                self.Manager.StopAllEyes()
                self.tlight.Run = False
                self.args["run"] = False
            elif c is 13:
                for i in range(20):
                    print("starting wave")
                self.Manager.StartAllEyes()
            elif c is not -1:
                print(c)

                #QuitProgram()
            #This initialises an RGB-image that is just black. Now, for example, if you wanted to set the left half of the image to blue and the right half to green , you could do so easily:



class WaveManager(object):
    def __init__(self, args):
        self.Eyes = list()
        self.tlight = args["tlight"]
        self.DelayUnit = args["DelayUnit"]
        self.Seq = args["Seq"]

        for i in range(args["EyeNums"]):
            args = {
                "Manager": self,
                "Distance": i,
                "DelayUnit": args["DelayUnit"],
                "Seq": args["Seq"]#,
                #"tlight": args["tlight"]
            }
            self.Eyes.append(Eye(args))

    def UpdateSeq(self, seq):
        self.Seq = seq
        for e in self.Eyes:
            e.Seq = seq



    def StopAllEyes(self):
        for e in self.Eyes:
            e.Run = False

    def StartAllEyes(self):
        e = Thread(target = self.StartAllEyesT)
        e.start()

    def StartAllEyesT(self):
        startDelay = self.DelayUnit * len(self.Eyes)
        delayS = delaySum(self.Seq)

#        if self.tlight.state is 0:
#            while(self.tlight.state is 0):
#                pass
        while(self.tlight.state is not 0):
            pass

        time.sleep((delayS-startDelay)%delayS)


        for e in self.Eyes:
            e.Start()

args = {}
args["EyeNums"] = 30
args["DelayUnit"] = 0.1
args["EyeNums"] = 50
args["DelayUnit"] = 0.1
args["Seq"] = defaultSeq
args["run"] = True
args["startState"] = 3

tlight = TrafficLight(args)
args["tlight"] = tlight
args["name"] = "xxx1"
wave = args["Manager"] = WaveManager(args)
v = Viewer(args)
v.start()

args2 = {}
args2["EyeNums"] = 70
args2["DelayUnit"] = 0.5
args2["Seq"] = t2Seq
args2["run"] = True
args2["name"] = "xxx1"
args2["startState"] = 4
t2light = TrafficLight(args2)
args2["tlight"] = t2light
args2["name"] = "xxx2"
wave2c = args2["Manager"] = WaveManager(args2)

v2 = Viewer(args2)
#while(tlight.state is not 4):
    #pass
#v2.start()

while(args["run"]):
    time.sleep(10)
    print("..............")

print("finished all")


#h,w = 100,200
#blank_image = np.zeros((h,w,3), np.uint8)
#blank_image[:,0:width//2] = (255,0,0)      # (B, G, R)
#blank_image[:,width//2:width] = (0,255,0)

#blank_image[:,0:10] = (255,255,255)      # (B, G, R)
#blank_image[height//4:3*height//4,width//2-5:width//2+5] = blank_image[:,0:10][height//4:3*height//4,:]


#img = cv2.circle(img, a, 25, (0,0,255), -1)
#img = cv2.circle(img, b, 25, (0,255,255), -1)
#img = cv2.circle(img, c, 25, (0,255,0), -1)
