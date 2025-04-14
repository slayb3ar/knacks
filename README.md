# Knacks

Random configs etc

## Config

To symlink content,

1. Symlink all config/ contents `find /knacks/config -maxdepth 1 -not -path /test/folder -exec ln -s {} ~/.config/ \;`
2. Update tmux config `tmux source-file ~/.config/tmux.conf`

## Terminal

1. Import `tokyo_night.terminal`
