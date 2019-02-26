#
# ~/.bashrc
#

# If not running interactively, don't do anything
[[ $- != *i* ]] && return

alias ls='ls --color=auto'

SHAPE=$(echo -e "\u232c")
SOLIDHEX=$(echo -e "\u2b1f")
POINT=$(echo -e "\u25b6")

myOP=$"\[\033[3;37m\] ~ "
myUS=$"\[\033[3;96m\] \u"
myOPP=$"\[\033[3;37m\] ~"
myCLO=$"\[\033[0m\] $SHAPE"
myL=$"\[\033[0m\] $SHAPE "
myHO=$"\[\033[3;96m\]\h"
myPA=$"\[\033[3;37m\] \w"
myD=$"\[\033[2;96m\] $POINT "
mySYST=$"\[\033[0m\]"

PS1=$"$myUS$myL$myHO$myPA$myD$mySYST"

# set EDITOR environment variable
export EDITOR=vim
export VISUAL=vim

export PATH=/opt/anaconda/bin:$PATH

xset -b

# alias clear
alias clear='clear && screenfetch'
# print ascii art when terminal is opened
screenfetch

# alias update system
alias update='python $HOME/.system/update.py'

# alias mount ext hd
alias drive='python $HOME/.system/drive.py'

# alias to create a new repo on Github.com from CLI
alias gitrepo='python $HOME/.system/gitrepo.py'

# alias Skype
alias skype='chromium --app=https://web.skype.com'

# alias gmail
alias gmail='chromium --app=https://gmail.com'

# alias twitter
alias twitter='chromium --app=https://twitter.com'

# alias facebook
alias facebook='chromium --app=https://facebook.com'

# alias messenger
alias messenger='chromium --app=https://facebook.com/messages/'

# alias instagram
alias instagram='chromium --app=https://instagram.com'

# alias youtube
alias youtube='chromium --app=https://youtube.com'

# alias github
alias github='chromium --app=https://github.com'

# alias library
alias library='thunar /home/chris/Library'

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
__conda_setup="$('/opt/anaconda/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
if [ $? -eq 0 ]; then
    eval "$__conda_setup"
else
    if [ -f "/opt/anaconda/etc/profile.d/conda.sh" ]; then
        . "/opt/anaconda/etc/profile.d/conda.sh"
    else
        export PATH="/opt/anaconda/bin:$PATH"
    fi
fi
unset __conda_setup
# <<< conda initialize <<<

