import vlc
import time

def play():
    '''
    plays the file that is cool af
    '''
    start = time.time()
    end = start + 30
    while time.time() < end:
        p = vlc.MediaPlayer('\96cddc50-e423-4c3d-9c47-50944f0570e2.mp3')
        p.play()