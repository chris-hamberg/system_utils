#!/home/chris/anaconda3/bin/python
import os, time

volume, wait, count = 5, 3, 260

for i in range(count):

    os.system('clear')
    
    print('[i]={i}\t[vol]={volume}\t[wait]={wait}'.format_map(vars()))
    
    if volume < 67 or i >= 240:
        if i >= 240:
            # over sleeping. wake up
            volume, wait = 100, 0.5
        os.system('pactl set-sink-volume 0 {volume}%'.format_map(vars()))
    
    os.system('play /home/chris/.system/beep-09.wav')
    
    time.sleep(wait)
    
    if not i%2: volume += 1

os.system('pactl set-sink-volume 0 67%')
