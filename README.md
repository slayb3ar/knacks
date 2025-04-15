# Knacks

Random configs etc

## Config

To symlink content,

1. Symlink all config/ contents `find /knacks/config -maxdepth 1 -not -path /test/folder -exec ln -s {} ~/.config/ \;`
2. Update tmux config `tmux source-file ~/.config/tmux.conf`

## Terminal

1. Import `tokyo_night.terminal`
2. Copy zshrc `cp /knacks/terminal/.zshrc ~/.zshrc && source ~/.zshrc`

## Setup

# setup repo

`Git clone repo`

# install

`brew install tmux`
`brew install vim`

# fonts

`download font && copy /system/fonts/

# symlink

`ln -s PWD/config/* ~/.config/`

#

`brew install lazygit`
