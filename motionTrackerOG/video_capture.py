import cv2 
import time

def record(time_sleep):
    """
    records the webcam for a certain time.
    """
    #declaring the codec and the videowriter object so that i can record the reaction.
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
    video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    out.write(video)
    time.sleep(time_sleep)
    video.release()
    out.release()
    cv2.destroyAllWindows()
        
    
    