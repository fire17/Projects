import numpy as np
import cv2
import random
# Load an color image in grayscale
import os, glob


import time

def ColorImage(w,h,color):
    img = np.zeros((h,w,3), np.uint8)
    img[:,:,] = color
    return img

def Mask(img, mask, color = [35,35,35]):
    # Read the images
    background = img

    h,w,z = img.shape

    foreground = ColorImage(w, h, color)
    alpha = mask

    # Convert uint8 to float
    foreground = foreground.astype(float)
    background = background.astype(float)

    # Normalize the alpha mask to keep intensity between 0 and 1
    #print()
    #print(img.shape)
    #print(foreground.shape)
    #print("AAAAAA",alpha.shape)
    #cv2.imshow("aaaaaa",img)
    #print("_______")
    #cv2.waitKey(0)
    alpha = alpha.astype(float)/255

    # Multiply the foreground with the alpha matte
    foreground = cv2.multiply(alpha, foreground)

    # Multiply the background with ( 1 - alpha )
    print(alpha.shape, background.shape)
    background = cv2.multiply(1.0 - alpha, background)
    #cv2.imshow("for",foreground/255)
    #cv2.imshow("bak",background/255)
    #cv2.waitKey(0)

    # Add the masked foreground and background.
    outImage = cv2.add(foreground, background)

    return outImage


class ProgressBar:

    min = 0
    max = 300
    current = 0
    bar = []
    autoSet = True

    beforeColor = [255,255,255]
    afterColor = [0,0,0]

    height = 50
    width = 300

    img = None

    #overlay = None
    top = None
    mask = None



    def __init__(self, mask, current = -1, color = [255,255,255], topground = [35,35,35]
    , autoSet = True):
        # Read the images
        #self.top = cv2.imread(top)
        self.mask = cv2.imread(mask)
        height,width,z = self.mask.shape
        self.height = height
        self.width = width
        #self.top = ColorImage(width, height, topground)
        self.topc = topground
        print("mask ==== height:",height,"width:",width )
        #cv2.waitKey(0)

        self.max = width
        if current is not -1:
            self.current = current
        #self.bar = []
        for i in range(self.max):
            self.bar.append([])
            self.bar[i] = topground
        self.beforeColor = color
        self.afterColor = topground
        #print(self.bar)

    def SetBarColor(self):
        #print("_____________")
        before = self.beforeColor
        for i in range(self.current):
        #    print(i, before, "IIIIIIIIIIIIII")
            self.bar[i] = before
        #    print("-------",self.bar[i],before)

        after = self.afterColor
        for i in range(self.max-self.current):
            self.bar[i+self.current] = after


    def plus(self, n = 1):
        #print(self.beforeColor,"zzzzzzzzzzzzzzzz")
        if not(n>1):
            n = 1
        for i in range(n):
            self.current += 1

        if self.current >= self.max:
            self.current = 99

        if self.autoSet:
            self.SetBarColor()

        return self.current

    def minus(self, n = 1):
            if not(n>1):
                n = 1
            for i in range(n):
                self.current += -1
            if self.current<self.min:
                self.current=0

            if self.autoSet:
                self.SetBarColor()

            return self.current


    def printCMD(self):
            clear = lambda: os.system("cls")
            clear()
            str = "["
            bar = self.GetBar()
        #    print(bar,"xxx")
            for b in bar[:]:
                #print(b)
                r,g,b = b
                if r > 100 or g > 100 or b > 100:
                    str+="*"
                else:
                    str+=" "
            str+="]"
            print(str)


    def GetBar(self):
        return self.bar

    def SetBar(self, bar):
        self.bar = bar

    def GetImage(self):
        return self.GenPic(self.bar)

    def displayImage(self, winName = "bar"):

        self.display(self.GetImage(), winName = winName)

    def display(self, img, winName = "XXX"):

        cv2.imshow(winName,img)
        cv2.waitKey(1)


    def GenPic(self, bar, widthS = 1):
        width = widthS*self.max

        print(width,self.height )
        if self.img is None:
            img = np.zeros((self.height,width,3), np.uint8)
            self.img = img
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
            print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        else:
            img = self.img
            print("YYYYYYYYYYYYYYYYYYYYYYYYYY")
            print("YYYYYYYYYYYYYYYYYYYYYYYYYY")
            print("YYYYYYYYYYYYYYYYYYYYYYYYYY")

        img[:,:,] = self.afterColor
        #This initialises an RGB-image that is just black. Now, for example, if you wanted to set the left half of the image to blue and the right half to green , you could do so easily:
        #blank_image[:,0:width//2] = (255,0,0)      # (B, G, R)
        #blank_image[:,width//2:width] = (0,255,0)
    #    print("lens", len(img), len(self.bar ))

    #    print(self.bar[:self.current])
    #    print(self.bar[self.current:])
        #for i in range(self.max):
            #print(i)
        img[:,:self.current] = self.bar[:self.current]

#        cv2.imshow("iii",img)
#        cv2.waitKey(1)
        #return img
        return Mask(img = img, mask = self.mask)/255


        #if self.overlay is not None:
        #    for i in range(1 ):
        #        img = cv2.addWeighted(img,.5,self.overlay,.5,0)

        #img[:,self.current:] = self.bar[self.current:]
        #img[:,self.current:,i,] = self.bar[self.current:]


        return img





#added_image = cv2.addWeighted(background,0.4,overlay,0.6,0)
#cv2.imshow("gx",added_image)


#new = overlay_transparent(cv2.imread('full.png'),overlay,0,0)
#cv2.imshow("new",new)

#cv2.waitKey(1)
#cv2.imwrite('combined.png', added_image)

w,h = 500,100
c = (255,0,0)
img = ColorImage(w,h,c)
#cv2.imshow("img",img)

print(">>>>>>>>>>>>>>>>>>>>>>>>")
#cv2.waitKey(0)

background = cv2.imread('masks/1.png')
#overlay = cv2.imread('add.png')
print("xxxxxxxxxxxxx",background.shape)

max = background.shape[1]
n = 4
#bar1 = ProgressBar(mask = 'mask.png', max = max, color = [137,135,255], background = [25,25,25], height = background.shape[0])

#b = bar1.GetBar()
print("@@@@@@")
#print(b[0])
print("@@@@@@")
print()


for i in range(int(max/n)-1):
    print("_______")
#    bar1.plus(n=n)
#        bar.printCMD()
#    img = bar1.GetImage()
#    bar1.display(img, "a")

#    cv2.waitKey(0)


print("XXXXXXXXXXXX")

for rr in range(6):

    colors = [[137,135,255], [24,174,252], [78,67,231], [205,110,91], [226,229,106]]
    c2 = []
    for c in colors:
        x,y,z = c
        r = rr%4
        r = 0
        c = [(x+r*random.randint(0,60))%255,(y+r*random.randint(0,20))%255,(z+r*random.randint(0,40))%255]
        c2.append(c)
    colors = c2
    BarList = []
    colorC = 0
    hsum, wsum = 0,0
    h,w = 0,0
    fileCount=0
    maskList = []
    for infile in sorted(glob.glob('masks/*.png')):
        fileCount+=1
        #print(max)
        #print(max)
        #print(max)
        m = cv2.imread(infile)
        maskList.append(m)
        print("file:",m.shape)
        hsum += m.shape[0]
        h,w,z = m.shape

        #cv2.waitKey(0)
        bar = ProgressBar(color = colors[colorC], mask = infile)
        bar.current = random.randint(0,int(bar.max/2))
        bar.current = 0
        BarList.append(bar)
        colorC+=1

    bigImg = ColorImage(w, hsum, [0,255,0])
    bigMask = ColorImage(w, hsum, [255,255,255])
    for i in range(fileCount):
        bigImg[i*h:(i+1)*h,:] = colors[i]
        bigMask[i*h:(i+1)*h,:] = maskList[i][:,:]


    #cv2.imshow("big",bigImg)
    #cv2.imshow("mask",bigMask)
    #cv2.waitKey(0)

    final = Mask(bigImg, bigMask)
    #cv2.imshow("FINAL_X", final/255)
    #cv2.waitKey(0)


    startAt = 100

    done = False
    strng = 1
    finalCopy = final.copy()
    while(not done):
        final = finalCopy.copy()
        for f in range(fileCount):
            startAt = BarList[f].current
            #startAt+=100

            BarList[f].current +=random.randint(-4,12)*strng
            if BarList[f].current >= BarList[f].max:
                done = True
            if BarList[f].current <0:
                current = 0;

            final[f*h:(f+1)*h,startAt:] = [35,35,35]
        cv2.imshow("FINAL_X", final/255)
        cv2.waitKey(1)

    cv2.imshow("FINAL_X", final/255)
    #cv2.waitKey(0)
