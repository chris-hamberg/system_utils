import os, sys

def adjust(arg):
    if 'd' in arg.lower():
        os.system('xgamma -rgamma 0.85 -ggamma 0.8 -bgamma 0.75')
        os.system('xbacklight = 30')
        os.system('xrandr --output LVDS1 --brightness 0.4')
    else:
        os.system('xgamma -rgamma 1 -ggamma 1 -bgamma 1')
        os.system('xbacklight = 0')
        os.system('xrandr --output LVDS1 --brightness 1')

if __name__ == '__main__':
    try:
        arg = sys.argv[1]
        assert ('d' in arg.lower() 
                or 'u' in arg.lower()
                or 'h' in arg.lower()
                )
    except (IndexError, AssertionError):
        print('Select "up" or "down". "h" for help.')
    else:
        if 'h' in arg.lower():
            print('xrandr --output LVDS1 --brightness <value from 0.0 to 1>')
        else:
            adjust(arg)
