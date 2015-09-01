#!/usr/bin/env sh
gconftool-2 -s -t string /apps/gnome-terminal/profiles/Default/palette "#000000000000:#A6A633333333:#2F2F8D8D4141:#DBDB59592E2E:#323234348383:#E6E649497676:#5C5C64644C4C:#B9B9AAAA9999:#696969696969:#C2C24D4D4343:#6D6D94948D8D:#E8E8BFBF6A6A:#6B6B8484A3A3:#898964649292:#DEDEA0A05050:#ECECE9E9DDDD"
gconftool-2 -s -t string /apps/gnome-terminal/profiles/Default/background_color "#18181C1C2828"
gconftool-2 -s -t string /apps/gnome-terminal/profiles/Default/foreground_color "#C2C2B7B79090"
gconftool-2 -s -t string /apps/gnome-terminal/profiles/Default/bold_color "#DEDEA0A05050"
gconftool-2 -s -t bool /apps/gnome-terminal/profiles/Default/bold_color_same_as_fg "false"
gconftool-2 -s -t bool /apps/gnome-terminal/profiles/Default/use_theme_colors "false"
gconftool-2 -s -t bool /apps/gnome-terminal/profiles/Default/use_theme_background "false"