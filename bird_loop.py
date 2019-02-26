#!/home/chris/anaconda3/bin/python3
import pygame, time, os

def init():
    parent = '/home/chris/Music'
    track = os.listdir(parent)[0]
    path = os.path.join(parent, track)
    duration = (15*60) + 35 + 1
    return path, duration

def play(path, duration):
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    while True:
        pygame.mixer.music.play()
        time.sleep(duration)
    pygame.mixer.music.stop()

def main():
    path, duration = init()
    play(path, duration)

if __name__ == '__main__':
    main()
