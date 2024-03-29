import numpy as np
import cv2
import os
from image import Image
from multiprocessing import Process
from datetime import datetime
DirName='/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])
class Video:
    def __init__(self):
        self.image= Image()
        self.now = datetime.now()
    def show_webcam(self,mirror=False):
        cap = cv2.VideoCapture(0)
        i=0
        while(True):
            # Capture frame-by-frame
            ret, frame = cap.read()
            # Our operations on the frame come here
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # Display the resulting frame
            cv2.imshow('frame',gray)
            if (datetime.now()-self.now).total_seconds() >= 4:
                pos=DirName+'/hackathon/video/public/images/'+str(i)+'.png'
                print(pos)
                cv2.imwrite(pos,frame)
                p = Process(target=self.image.helper, args=(pos,i))
                p.start()
                self.now=datetime.now()
                i=i+1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
if __name__ == '__main__':
    video=Video()
    video.show_webcam(mirror=True)