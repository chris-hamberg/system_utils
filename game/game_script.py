import os, sys

def arg_parse():
    command = construct()
    try:
        arg = sys.argv[1]
    except IndexError: 
        arg = ''
    finally:
        return command[arg.lower()]

def construct():
    bash_cmd = 'bash $HOME/proj/game/'
    return {'-w' : [bash_cmd+'d2aw'],
            ''   : [bash_cmd+'d2a'],
            'mul': [bash_cmd+'d2aw', bash_cmd+'d2bw'],
            '1'  : [bash_cmd+'d2a'],
            '2'  : [bash_cmd+'d2b']}

def mount():
    try:
        if os.listdir('.iso/'):
            os.system('sudo umount ~/.iso/')
        os.system('sudo mount -o loop ~/game/Expansion.iso ~/.iso/')
    except Exception:
        print('error: iso mount')
        system.exit(0)
 
def run(commands):
    for cmd in commands:
        os.popen(cmd)

def main():
    commands = arg_parse()
    mount()
    run(commands)

if __name__ == '__main__':
    main()
