############################## CONFIG
# nvim editor
export VISUAL=/usr/bin/nvim

# autoload
autoload -U compinit
compinit

############################## UI
export TERM=xterm-256color
export COLORTERM=truecolor
alias ls='ls --color=auto'
alias dir='dir --color=auto'
alias tree='tree --color=auto'
PROMPT='%F{39}%~%f%F{213} ❯%f '

############################# BITNOMIAL
alias shake='stack exec shake --'
BTNL_DATABASE='postgresql://app:password123@localhost:5432/main'

