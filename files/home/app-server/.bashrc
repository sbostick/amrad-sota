# Default bashrc configuration

set -o vi
alias c='clear'

function prompt::init_colors {
  ANSI_RED="\033[0;31m"
  ANSI_BLUE="\033[0;34m"
  ANSI_BBLUE="\033[1;34m"
  ANSI_BROWN="\033[0;33m"
  ANSI_CYAN="\033[0;36m"
  ANSI_MAGENTA="\033[0;35m"
  ANSI_NONE="\033[0m"

  XTERM256_GREEN="\033[38;5;10m"
  XTERM256_WHITE="\033[38;5;15m"
  XTERM256_BLUE1="\033[38;5;25m"
  XTERM256_BLUE2="\033[38;5;27m"
  XTERM256_BLUE3="\033[38;5;33m"
  XTERM256_MAGENTA="\033[38;5;129m"
  XTERM256_PINK="\033[38;5;213m"
  XTERM256_RED="\033[38;5;160m"
  XTERM256_YELLOW="\033[38;5;227m"
  XTERM256_BROWN="\033[38;5;243m"
  XTERM256_CYAN="\033[38;5;44m"
}

function prompt::set_ps1 {
  local LINE_1="${ANSI_CYAN}[\t]${ANSI_NONE} ${ANSI_BROWN}\u@\H${ANSI_NONE}"
  local LINE_2="\w> "
  export PS1="${LINE_1}\n${LINE_2}"
}

function config::history {
  HISTCONTROL=ignoreboth
  HISTSIZE=1000
  HISTFILESIZE=2000
  shopt -s histappend
}

function config::aliases {
  alias ll='ls -alF'
  alias la='ls -A'
  alias l='ls -CF'
}

# __MAIN__
config::history
config::aliases
prompt::init_colors
prompt::set_ps1

# Check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# Enable command completion
if ! shopt -oq posix; then
  if [ -f /usr/share/bash-completion/bash_completion ]; then
    . /usr/share/bash-completion/bash_completion
  elif [ -f /etc/bash_completion ]; then
    . /etc/bash_completion
  fi
fi
