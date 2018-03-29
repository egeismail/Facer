import cv2
import numpy as np
import os
import json as JsonParser
import hashlib as hlb
import random
FCR_VERSION = "0.1b"
def md5(text):
    d_b = hlb.md5()
    d_b.update(text.encode("utf-8"))
    return d_b.hexdigest()
class Face:
    def __init__(self,FaceIMG=None,Rect=tuple(),Label=int()):
        self.FaceIMG = FaceIMG
        self.Rect = Rect
        self.Label = Label
    FaceIMG = None
    Rect = tuple()
    Label = int()
class Facer:
    FCR_Algorithms = np.array([md5("Eigen_FR"),
                               md5("Fisher_FR"),
                               md5("LBPHF_FR")])
    def __init__(self,options):
        self.options = dict(options)
        self.facer_LF = False
        self.CWDType = True
        if "fcr_dir" in options:
            print("ok")
            if os.path.exists(options["fcr_dir"]):
                self.CWDType = True
            else:
                os.makedirs(options["fcr_dir"])
                self.CWDType = True
        elif "fcr_Name" in options:
            self.facer_Name = options["fcr_Name"]
            if os.path.exists(os.path.join(os.getcwd(),self.facer_Name)):
                self.CWDType = False
            else:
                os.makedirs(os.path.join(os.getcwd(),self.facer_Name))
                self.CWDType = False
        if self.CWDType:
            cwd = options["fcr_dir"]
        else:
            cwd = os.path.join(os.getcwd(),self.facer_Name)            
        if os.path.isfile(os.path.join(cwd,"foptions.json")):
            mjd = JsonParser.loads(os.path.join(cwd,"foptions.json"))
            Filter = (
                        "fcr_name" in mjd and
                        "fcr_version" in mjd and
                        "fcr_file" in mjd and
                        "fcr_algorithm" in mjd
                    )
            if Filter:
                mfd = os.path.join(cwd,mjd["fcr_file"])
                Filter2 = (
                            mjd["fcr_version"] == FCR_VERSION and
                            (np.array(mjd["fcr_algorithm"]) == FCR_Algorithms).any()
                        )
                if Filter2:
                    self.facer_Version = FCR_VERSION
                    self.facer_Name = mjd["fcr_name"]
                    self.facer_File = mfd
                    self.facer_Recognizer = self.GetAlgorithm(mjd["fcr_algorithm"])
                    if self.facer_Recognizer is not None:
                        self.facer_LF = True
                    else:
                        return None
                else:
                    return None
            else:
                return None
        else:
            self.facer_Recognizer = self.GetAlgorithm(self.FCR_Algorithms[2])
            self.facer_Recognizer.write("Untitled.xml")
            with open(os.path.join(cwd,"foptions.json"),"w") as fp:
                fp.write(JsonParser.dumps({
                    "fcr_name":"Untitled",
                    "fcr_version":FCR_VERSION,
                    "fcr_file":"Untitled.xml",
                    "fcr_algorithm":self.FCR_Algorithms[2]
                }))
    def DetectSingleFace(self,img,Label):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);
        if (len(faces) == 0):
            return None
        elif(len(faces) > 1):
            return None
        return Face(gray[y:y+w, x:x+h], faces[0], Label)
    def TrainSingleFace(self,img,Label):
        Face = self.DetectSingleFace(img,Label)
        if Face is not None:
            try:
                self.facer_Recognizer.train(Face.FaceIMG,Face.Label)
            except:
                return False
            return True
        return False
    def TrainMultipleFaces(self,img):
        random.randint(0)
    def GetAlgorithm(self,algoid):
        if(algoid == self.FCR_Algorithms[0]):
            return cv2.face.EigenFaceRecognizer_create()
        elif(algoid == self.FCR_Algorithms[1]):
            return cv2.face.FisherFaceRecognizer_create()
        elif(algoid == self.FCR_Algorithms[2]):
            return cv2.face.LBPHFaceRecognizer_create()
        else:
            return None
def main():
    FTL = Facer({"fcr_Name":"sepy"})
if __name__ == '__main__':
    main()