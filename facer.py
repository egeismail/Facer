import cv2
import numpy as np
import os
import json as JsonParser
import hashlib as hlb
FCR_VERSION = "0.1a"
def md5(text):
    d_b = hlb.md5()
    d_b.update(text)
    return d_b.hexdigest()
class Facer:
    FCR_Algorithms = np.array([md5("Eigen_FR"),
                               md5("Fisher_FR"),
                               md5("LBPHF_FR")])
    def __init__(self,options):
        self.options = dict(options)
        self.facer_LF = False
        self.CWDType = True
        if options.has_key("facer_dir"):
            if os.path.exists(os.path.join(os.getcwd(),options["facer_dir"])):
                self.CWDType = True
            else:
                os.makedirs(os.path.join(os.getcwd(),options["facer_dir"]))
                self.CWDType = True
        elif options.has_key("facer_name"):
            self.facer_Name = options["facer_name"]
            if os.path.exists(os.path.join(os.getcwd(),self.facer_Name)):
                self.CWDType = False
            else:
                os.makedirs(os.path.join(os.getcwd(),self.facer_name))
                self.CWDType = False
        if self.CWDType:
            pass
        else:
            cwd = os.path.join(os.getcwd(),self.facer_Name)            
        if os.path.isfile(os.path.join(cwd,"foptions.json")):
            mjd = JsonParser.loads(os.path.join(cwd,"foptions.json"))
            Filter = (
                        mjd.has_key("fcr_name") and
                        mjd.has_key("fcr_version") and
                        mjd.has_key("fcr_file") and
                        mjd.has_key("fcr_algorithm")
                    )
            if Filter:
                mfd = os.path.join(cwd,mjd["fcr_file"])
                Filter2 = (
                            mjd["fcr_version"] == FCR_VERSION and
                            os.path.isfile(mfd) and
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
                        print("Facer Version Error or Facer File Error")
    def GetAlgorithm(self,algoid):
        if(algoid == self.FCR_Algorithms[0]):
            return cv2.face.EigenFaceRecognizer_create()
        elif(algoid == self.FCR_Algorithms[1]):
            return cv2.face.FisherFaceRecognizer_create()
        elif(algoid == self.FCR_Algorithms[2]):
            return cv2.face.LBPHFaceRecognizer_create()
        else:
            return None