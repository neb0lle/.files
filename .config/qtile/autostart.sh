#!/bin/sh
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &
nitrogen --restore &
picom --experimental-backends &
nm-applet &
# blueman-applet &
greenclip daemon &
dunst &
xbindkeys &
flameshot &
# noisetorch -i &
