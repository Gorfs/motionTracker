#importing the shit i need to make this work
import cv2, time, pandas
from video_capture import record
from datetime import datetime
from audio_player import play
import smtplib, ssl
import vlc

x = 0

#shit for when we make a log of movement.
static_back = None
motion_list = [ None, None ]
time = []
df = pandas.DataFrame(columns = ["Start", "End"])
  
#the capture from the webcam
video = cv2.VideoCapture(0)

#the player for the mp3 file for the audio that will scare luce
p = vlc.MediaPlayer('\96cddc50-e423-4c3d-9c47-50944f0570e2.mp3')
#the trigger for making sure the audio clip does not reapeat while it is playing.
trigger = 0

#loop to basically make this run indefinetly
while True:
    #frame is the video (still not exactly known how it works)
    check, frame = video.read()
    #if motion = 1 then there is mum in ma room
    #if motion = 0 then there is no mum in ma room
    motion = 0 #simple boolean value
  
    # gray get reassigned to a gray value with a blue to deal with noise in the image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if static_back is None:
        static_back = gray
        continue
  
    #make the difference frame which shows what has changes in a frame with white pixels.
    diff_frame = cv2.absdiff(static_back, gray)

    #the thresh frame uses the diff frame to find which pixels are different and if they are higher than 30 then they change them to fully white, if not then they are black.
    thresh_frame = cv2.threshold(diff_frame, 30, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations = 2) #don't know what dilate does tbh
  
    cnts,_ = cv2.findContours(thresh_frame.copy(), 
                       cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  
    #! for drawing the rectangle-----------------------------------------------------------------------------------------------------
    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        motion = 1
        if p.is_playing() == False:
            p.play()
        else:
            print('currently playing clip, cannot play again.')
        (x, y, w, h) = cv2.boundingRect(contour)
        # making green rectangle arround the moving object
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
    #TODO here is the start of what i don't understand.
    #! stopped drawing the rectangle------------------------------------------------------------------------------------------------------
  
    # marking down the motion state in the motion list list thing
    motion_list.append(motion)
  
    motion_list = motion_list[-2:]
  
  #! explanation for the csv file, it shows the start time of the movment and end time, It"s the DF thing not the motion list..
  #! so it's not motion list that goes into the csv file.
    
    
    # Appending Start time of motion
    #? why tf is there a verification of the ending things of the motion list.
    if motion_list[-1] == 1 and motion_list[-2] == 0:
        time.append(datetime.now())
        #making python play the mp3 file:
        #TODO trigger the playing of the file
        
            
        
            
            
        
    # Appending End time of motion
    if motion_list[-1] == 0 and motion_list[-2] == 1:
        time.append(datetime.now())
        
    #TODO here is the end of ths stuff i don't understand.
    
    
    # Displaying image in gray_scale
    cv2.imshow("Gray Frame", gray)
  
    # Displaying the difference in currentframe to
    cv2.imshow("Difference Frame", diff_frame)
  
    # Displaying the black and white image for the thresh frame
    cv2.imshow("Threshold Frame", thresh_frame)
  
    # Displaying color frame with contour of motion of object
    cv2.imshow("Color Frame", frame)
  
    key = cv2.waitKey(1)
    # if q entered whole process will stop
    if key == ord('q'):
        # if something is movingthen it append the end time of movement
        if motion == 1:
            time.append(datetime.now())
        break
  
#-------------script kiddyed----------------------
# Appending time of motion in DataFrame
for i in range(0, len(time), 2):
    #! i did not write this so it's using the format methode which i don't like :(
    df = df.append({"Start":time[i], "End":time[i + 1]}, ignore_index = True)
#----------------------------------------------------------------------------------------------------------
  
# Creating the times file
df.to_csv("Time_of_movements.csv")
  
video.release()
  
# destroy everything
#all must be balanced in the universe *snap*.
cv2.destroyAllWindows()