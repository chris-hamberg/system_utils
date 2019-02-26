import os
#os.system('sudo pacman -Syyu')
os.system('sudo pacman -Syuw')
os.system('sudo pacman -S archlinux-keyring')
os.system('sudo pacman -Syu')

# clean the CacheDir
os.system('sudo pacman -Sc')

# clean orphans
os.system('sudo pacman -Rns $(pacman -Qtdq)')

# clean logs
os.system('sudo journalctl --vacuum-size=50M')

if input('\n:: Do you want to reboot the system? [Y/n] ').lower() == 'n':
    os.system('clear && screenfetch')
else:
    os.system('reboot')
