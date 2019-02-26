import shutil, sys, os

drive = 'sdb1'
path = '{drive}/Storage/External Hard Drive/Library/DUMP'
dst = os.path.join(os.environ['HOME'], path.format_map(vars()))

def process(name):
    folder = '[Packt] ' + name
    src_folder = os.path.join(os.environ['HOME'], 'Downloads', folder)
    os.mkdir(src_folder)
    for file in os.listdir(os.path.join(os.environ['HOME'], 'Downloads')):
        src = os.path.join(os.environ['HOME'], 'Downloads', file)
        if os.path.isfile(src) and not src.startswith('.'):
            ext = src.split('.')[1]
            alias = name+'.'+ext
            src_alias = os.path.join(os.environ['HOME'], 'Downloads', alias)
            os.rename(src, src_alias)
            shutil.move(src_alias, os.path.join(src_folder, alias))
    shutil.move(src_folder, dst)

if __name__ == '__main__':
    try:
        name = sys.argv[1]
        process(name)
    except Exception as error:
        print(error)
