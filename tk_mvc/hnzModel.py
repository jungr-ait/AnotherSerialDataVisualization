from tkinter.filedialog import askopenfilename
#import cv2
from pubsub import pub
#import PIL.ImageTk, PIL.Image
import numpy as np

class Model:
    def __init__(self):

       
        return


    def loadImg(self):
        print("Model - loadImg")
        path= askopenfilename(initialdir="./",
                       filetypes=[("Image File", "*.jpg"),("All Files","*.*")],
                        title = "Choose a file."
                        )
        
        if len(path)>0:
            #self.originalImg = cv2.imread(path)
            self.currentImg = self.originalImg.copy()
            ##image = PIL.Image.fromarray(self.originalImg)#.resize(300,300)
            #update view image
            #pub.sendMessage("model_updated", data=self.toTkImg(self.currentImg))

        print (path)
        return
        
    def getCurrentImg(self):
        print("Model - getCurrentImg")
        return 
    def getOriginalImg(self):
        return self.originalImg

    def lineDetection(self,p,th,minlen,maxgap):

        #self.currentImg=img
        pub.sendMessage("model_updated", data=None)
        print("Model- lineDetection")

    #convert cv2 image to tk image
    def toTkImg(self,img):
        return