from path import Path
import sys, os

def rec(fname):
    os.system('sox -t pulseaudio default {fname}'.format_map(vars()))
    print('playback command: ~$ play .wavs/{fname}'.format_map(vars()))

def initalize():
    path = os.path.join(os.getcwd(), '.wavs')
    os.path.exists(path) or os.mkdir(path)
    return path

def normalize(fname):
    ext = Path(fname).ext
    if not ext:
        fname += '.wav'
    return fname

def sanity_check():
    try:
        assert list(os.popen('which sox'))
    except AssertionError:
        os.system('sudo pacman -S sox')

def main():

    sanity_check()

    try:
        fname = os.path.join(initialize(), normalize(sys.argv[1]))
        assert not os.path.exists(fname)
    except AssertionError:
        print('{fname} already exists.'.format_map(vars()))
    except IndexError:
        print('You must specify an output filename.')
    else:
        rec(fname)

if __name__ == '__main__':
    main()
