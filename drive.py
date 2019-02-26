'''
author  : Chris Hamberg
program : xfce4 Arch Linux NTFS Compatable External Drive Mount
github  : https://github.com/morphine-html/
facebook: https://www.facebook.com/chris.hamberg.1

usage:

    first time running... ~$ drive.py
    forever after that... ~$ drive 

about:

    A script for mounting and unmounting external storage on Arch Linux xfce4
    systems.

    Establishes NTFS read/write compatability for NTFS drives.

    Script installs itself to a hidden folder, and creates a command line Bash
    alias
        ~$ drive

    If you do not have have ntfs-3g installed this script will install it for you.
    ntfs-3g is a component of the NTFS compatability solution. It also enables
    a sudo modprobe ntfs command in real time during mount.

    The script can be used to mount or unmount one external storage device at
    a time. The reason for this limitation is simplicity.
'''
import psutil, sys, os, re

def notify():
    os.system('clear')
    print('''
### Welcome to drive.py ###
 
 Python will make a hidden folder in your user directory: /home/user/.system
 (if that folder does not already exist.) This script will be deleted and moved 
 to that directory. If no Bash alias 'drive' exists then this script will create 
 one. To run this script in the future, simply run the command ~$ drive

 This script will make your xfce4 Arch Linux system compatable with the NTFS 
 file system, so that you can read/write to an external drive, and usb. The 
 primary function of this script is to mount any drive, and make Linux NTFS 
 compatable for any NFTS drive. Although any type of drive can be mounted and 
 unmounted with this script.

 To uninstall, simply delete the script from /home/user/.system, and delete
 the Bash alias in /home/user/.bashrc. The Bash alias is 'drive'.

 If you do not have ntfs-3g installed, this script will handle that for you.
 [WARNING] Follow the simple instructions during that installation carefully. 
 Disrupting the ntfs-3g install can cause serious problems in your system.
 As long as the directions are followed everything should go smoothly.
 Alternatively, you can manually install ntfs-3g with the command
 sudo pacman -S ntfs-3g. This command is exactly what the script does. 
 If ntfs-3g is already installed then the script will skip the installation 
 step. Installation of ntfs-3g requires a mandatory system reboot. This
 script will force you to reboot after the install. Do not interupt it.
    ''')
    input('press [anykey] to continue\n')

def retrieve_drives():
    '''
    Parse and return all system drives as a dict, from the fdisk -l result.
    '''
    # Initialize local variables.
    drives, key, regex = dict(), 0, re.compile(r'^/dev/(.*?) ')
    for drive in list(os.popen('sudo fdisk -l')):   # Parse system drives
        if regex.search(drive):    # then (for example) found '/dev/sda'
            drives[key] = drive.strip()
            key += 1                # generate a new dict key
    return drives                   # returns a dictionary {key: drive}

def internal_drives():
    '''
    Detects the device ('/dev/sda') on the root partition.
    It is assumed that all internal drives, and all hard drives are on the same
    logical volume.
    Returns a string of the form '/dev/sda'
    '''
    partitions = psutil.disk_partitions()
    root_partition = partitions[0]
    drive_letter = root_partition.device
    return drive_letter[:-1]                # truncates the device number

def display(drives):
    '''
    Takes drives dict (result from fdisk -l) as input.
    Display attached drives in terminal.
    '''
    print('Select the drive to mount (by number) ...')
    system_partition = internal_drives()    # ex. system_partition = '/dev/sda'
    regex = re.compile(r'^(/dev/\w{3})')    # ex. '/dev/sda', '/dev/sdb', etc..
    for key, drive in drives.items():       # Scan drives from fdisk -l result.
        if regex.search(drive)[0] == system_partition:
            continue                        # drive is not external.
        print(' [{key}]:\t{drive}'.format_map(vars()))

def select(drives):
    '''
    Takes the drives dict as input.
    Prompt user to select a drive from that dict. With validation.
    Returns the dictonary key of the user selected drive.
    '''
    while True:                         # Wait for valid input.
        try:
            drive_number = int(input('> '))
            drives[drive_number]        # Test for validity.
        except (ValueError, KeyError):
            print('Error: select a number from the list.')
            continue                    # The input was invalid.
        else:
            break                       # The input was valid.
    return drive_number                 # returns the dictionary key as int

def create(drive):
    '''
    Creates a mount point in the /home/user directory. 
    The mount point is the name of drive.
    Returns mount_point as a str. Ex. '/home/user/sdb1'
    '''
    name = drive.split('/')[-1]                     # ex. 'sdb1'
    basepath = os.environ['HOME']
    mount_point = os.path.join(basepath, name)      # '/home/user/sdb1'
    if not os.path.exists(mount_point):
        os.mkdir(mount_point)                       # create the mount point
    return mount_point

def mount(drive, mount_point):
    '''
    Takes two strings as input. Ex. '/dev/sdb1' and '/home/user/sdb1'
    Mounts the drive.
    '''
    uid, gid = os.getuid(), os.getgid()
    cmd = 'sudo mount -o uid={uid},gid={gid},rw {drive} {mount_point}'
    os.system(cmd.format_map(vars()))
    print('drive {drive} has been mounted to {mount_point}'.format_map(vars()))

def unmount(drive, mount_point):
    '''
    Takes two strings as input. Ex. '/dev/sdb1' and '/home/user/sdb1'
    Unmounts the drive that this script mounted.
    '''
    try: # in the edge case where a system was rebooted and a drive was mounted.
        cmd = 'sudo umount {drive}'
        os.system(cmd.format_map(vars()))
        os.rmdir(mount_point)   # deletes the mount point.
    except FileNotFoundError:   # drive wasn't mounted.
        pass
    except Exception:           # in case of logical error.
        pass

def drive_name(drives, drive_number):
    '''
    Takes the drives dict, and key drive_number as input.
    Parse the drive name from the selected drive dict[int].
    Returns the string '/dev/sdb1'.
    '''
    return drives[drive_number].split()[0]      # ex. return '/dev/sdb1'

def permission_failed():
    '''
    Handles the installation of ntfs-3g.
    This function is only called when ntfs-3g is not installed in the system.
    '''
    print('Missing critical package(s): ntfs-3g')
    input('Package(s) will be installed.\n[anykey] to continue ...\n')
    print('Do NOT turn off your computer and do NOT exit this prompt!!!')
    os.system('sudo pacman -S ntfs-3g')
    print('\n[WARNING] System must reboot in order to prevent '
          'catasrophic system failure.')
    print('External NTFS will be r/w mountable from now on, after reboot.')
    print('Press [anykey] to continue '
          '(system will be rebooted automatically)')
    input()
    os.system('reboot')
 
def grant_permissions():
    '''
    Verify ntfs-3g installation or install ntfs-3g.
    Activate ntfs compatability.
    '''
    try:
        # see if ntfs-3g is installed
        assert list(os.popen('which ntfs-3g'))
    except AssertionError:
        permission_failed()         # install ntfs-3g
    else:
        # ntfs-3g is installed.
        cmd = 'sudo modprobe ntfs'
        os.system(cmd)              # enable ntfs

def check_drive(drives, drive_number):
    '''
    Takes drives dict and drive_number int as input.
    Searchs for 'NTFS' in the drive information.
    Returns Boolean (either drive is NTFS or it is not.)
    '''
    return 'ntfs' in drives[drive_number].lower()

def persist(drive, mount_point):
    '''
    Takes two paths as strings, as input. Ex. '/dev/sdb1' and '/home/user/sdb1'
    Persist the mount point identity. Required for unmounting.
    Outputs the input data to a simple csv as a hidden file in the user dir.
    '''
    name = '.DO_NOT_DELETE_THIS_FILE_CONTAINS_DATA_FOR_SAFE_UNMOUNT'
    with open(name, 'w') as fhand:
        fhand.write('{drive},{mount_point}'.format_map(vars()))

def recover(name):
    '''
    name is the filename used for the purpose of path persistence.
    Restore the mount point identity into RAM.
    return (for example) '/dev/sdb1' and '/home/user/sdb1'
    '''
    with open(name, 'r') as fhand:
        data = fhand.read()
    drive, mount_point = data.split(',')
    return drive, mount_point

def install():

    fname = os.path.basename(__file__)
    path1 = os.path.join(os.environ['HOME'], '.system')
    path2 = os.path.join(path1, fname)
    
    if os.path.exists(path2):
        pass
    else:
        notify()
        if not os.path.exists(path1):
            print('Making a hidden folder {path1}'.format_map(vars()))
            os.mkdir(path1)
        with open('drive.py', 'r') as fhand1, open(
                  path2, 'w') as fhand2:
            print('Copying {fname} to {path2}'.format_map(vars()))
            fhand2.write(fhand1.read())
        fname_abspath = os.path.dirname(os.path.realpath(__file__))
        os.remove(os.path.join(fname_abspath, fname))
        print('Local copy of {fname} has been deleted'.format_map(vars()))
        print('Checking if bash alias exists')
        with open('.bashrc', 'r') as fhand:
            if 'drive' in fhand.read():
                print('Bash alias "drive" is already in .bashrc')
                return True
        print('Creating bash alias "drive"')
        alias  = '\n# mount external drive'
        alias += "\nalias drive='python $HOME/.system/{fname}'".format_map(
                vars())
        with open('.bashrc', 'a') as fhand:
            fhand.write(alias)
        print('''\n
Installation of drive.py complete.

From now on, use the command...
    ~$ drive
...to mount and unmount external drives with this script.
(you must open a new terminal or type ~$ source .bashrc)

If ntfs-3g is not installed, this script will install it
the next time it is ran. Following the install of ntfs-3g
and a system reboot, you will freely be able to mount and
unmount any external storage with the script!

The script will now exit...''')
        input('\npress [anykey] to continue...\n')
        sys.exit(0)

def main():
    '''
    Mounts an unmounted drive.
    Unmounts a mounted drive.
    '''
    name = '.DO_NOT_DELETE_THIS_FILE_CONTAINS_DATA_FOR_SAFE_UNMOUNT'

    # Unmount procedure
    if os.path.exists(name):                    # Mounted drive has not been unmounted.
        drive, mount_point = recover(name)      # From previous execution.
        unmount(drive, mount_point)
        print('drive {drive} has been unmounted.'.format_map(vars()))
        os.remove(name)                         # Drives are no longer mounted.

    # Mount procedure
    else:
        drives = retrieve_drives()      # Get system drives information
        display(drives)
        drive_number = select(drives)             # user selectes drive to mount
        drive = drive_name(drives, drive_number)  # parse drive name from info
        ntfs  = check_drive(drives, drive_number) # search for 'NTFS' in info
        if ntfs:
            grant_permissions()     # enable NTFS compatability
        mount_point = create(drive) # create a mount point
        mount(drive, mount_point)   # mount the drive
        persist(drive, mount_point) # persist '/dev/sdb1' & '/home/user/sdb1'
        print('to umount the drive simply run ~$ python drive.py')
    sys.exit(0)

if __name__ == '__main__':
    if sys.version[0] == '2':       # Python 2 interpreter detected.
        print('This script runs in Python 3.')
        sys.exit(0)
    elif not psutil.LINUX:          # OS is not Linux
        print('This script solves a problem for GNU/Linux distributions.')
        sys.exit(0)
    else:
        install()
        main()
