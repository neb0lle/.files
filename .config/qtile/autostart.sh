#!/bin/sh
/usr/lib/mate-polkit/polkit-mate-authentication-agent-1 &
nvidia-settings --assign CurrentMetaMode="nvidia-auto-select +0+0 { ForceFullCompositionPipeline = On }" &
xwallpaper --maximize ~/Pictures/Wallpapers/wallpaper.png &
picom --experimental-backends &
sxhkd &
nm-applet &
greenclip daemon &
dunst &
flameshot &
udiskie &

xinput set-prop 18 346 1 &
xinput set-prop 11 342 1 &
