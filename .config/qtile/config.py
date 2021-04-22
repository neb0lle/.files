from typing import List  # noqa: F401
import os
import re
import subprocess
from libqtile import qtile
from libqtile import qtile, bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.command import lazy
from libqtile.lazy import lazy

mod = "mod4"
terminal = "kitty"

# Resize functions for bsp layout
def resize(qtile, direction):
    layout = qtile.current_layout
    child = layout.current
    parent = child.parent
    while parent:
        if child in parent.children:
            layout_all = False

            if (direction == "left" and parent.split_horizontal) or ( direction == "up" and not parent.split_horizontal
            ):
                parent.split_ratio = max(5, parent.split_ratio - layout.grow_amount)
                layout_all = True
            elif (direction == "right" and parent.split_horizontal) or ( direction == "down" and not parent.split_horizontal
            ):
                parent.split_ratio = min(95, parent.split_ratio + layout.grow_amount)
                layout_all = True

            if layout_all:
                layout.group.layout_all()
                break
        child = parent
        parent = child.parent
@lazy.function
def resize_left(qtile):
    resize(qtile, "left")
@lazy.function
def resize_right(qtile):
    resize(qtile, "right")
@lazy.function
def resize_up(qtile):
    resize(qtile, "up")
@lazy.function
def resize_down(qtile):
    resize(qtile, "down")

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "n",lazy.layout.next(),desc="Switch focus to other pane of stack"),

    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),
        desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),
        desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),
        desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(),
        desc="Move window up"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "mod1"], "h",resize_left,desc="Grow window to the left"),
    Key([mod, "mod1"], "l",resize_right,desc="Grow window to the right"),
    Key([mod, "mod1"], "j",resize_down,desc="Grow window down"),
    Key([mod, "mod1"], "k",resize_up, desc="Grow window up"),

    # Rotation of windows
    Key([mod], "r",lazy.layout.rotate()),
    Key([mod,"control"], "j",lazy.layout.flip_left()),
    Key([mod,"control"], "k",lazy.layout.flip_right()),

    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout()),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod],"y",lazy.window.bring_to_front(),desc="Bring window to front"),
    Key([mod,"control"],"y",lazy.window.toggle_floating(),desc="Toggle floating on focused window",),
    Key([mod,"control"], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
    Key([mod],"m",lazy.layout.maximize(),desc="Toggle window between minimum and maximum sizes"),

    # Qtile
    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    # Group Changer
    Key([mod, "control"], "l", lazy.screen.next_group()),
    Key([mod, "control"], "h", lazy.screen.prev_group()),
    Key([mod], "u", lazy.next_urgent()),

    # Rofi-Calc
    Key([mod],"equal",lazy.spawn('''rofi -width 27 -show calc -modi calc -no-show-match -no-sort -no-history -lines 0 -theme ~/.config/rofi/themes/sed.rasi -calc-command "echo -n '{result}' | xclip -selection clipboard"'''),desc="Rofi calc"),

]
colors = [["#000000","#000000"], # BLACK
          ["#ffffff","#ffffff"], # WHITE
          ["#01fdb0","#01fdb0"], # MINT
          ["#131519","#131519"], # DARK GREY
          ["#46474f","#46474f"], # LIGHT GREY
          ["#ffff44","#ffff44"], # YELLOW
          ["#ff4444","#ff4444"], # SALMON
          ["#00a2ff","#00a2ff"]] # BLUE

def init_group_names():
    return [("I",{'layout':'bsp'}),
            ("II",{'layout':'bsp'}),
            ("III",{'layout':'bsp'}),
            ("IV",{'layout':'bsp'}),
            (" V ",{'layout':'bsp'}),
            ("VI",{'layout':'bsp'}),
            ("VII",{'layout':'bsp'}),
            ("VIII",{'layout':'bsp'}),
            ("IX",{'layout':'bsp'})]

def init_groups():
    return [Group(name,**kwargs) for name, kwargs in group_names]
if __name__ in ["config","__main__"]:
    group_names=init_group_names()
    groups=init_groups()
for i, (name,kwargs) in enumerate(group_names,1):
    keys.append(Key([mod],str(i),lazy.group[name].toscreen()))
    keys.append(Key([mod,"shift"],str(i),lazy.window.togroup(name,switch_group=True)))

layout_theme = {
        "border_width":2,
        "margin":4,
        "border_normal":"131519",
        "border_focus":"46474f",
        "font": "JetBrainsMono Nerd Font",
        "grow_amount": 2,
        }
layouts = [
    # layout.Columns(),
    layout.Bsp(**layout_theme,fair=False),
    layout.Stack(num_stacks=2,**layout_theme),
    layout.Max(**layout_theme),
   # layout.Floating(**layout_theme),
   # layout.Matrix(),
   # layout.MonadTall(),
   # layout.MonadWide(),
   # layout.RatioTile(),
   # layout.Tile(),
   # layout.TreeTab(),
   # layout.VerticalTile(),
   # layout.Zoomy(),
]

widget_defaults = dict(
    font='JetBrainsMono Nerd Font Medium',
    fontsize=14,
 )
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    font = "JetBrainsMono Nerd Font Bold",
                    margin_y=3,
                    fontsize=16,
                    highlight_color=colors[5],
                    block_highlight_text_color=colors[6],
                    inactive=colors[4],
                    active=colors[1],
                    this_current_screen_border=colors[3],
                    disable_drag=True,
                    this_screen_border=colors[3],
                    other_current_screen_border=colors[3],
                    other_screen_border=colors[3],
                    background=colors[3],
                    urgent_text=colors[5],
                    urgent_border=colors[3],
                    ),
                widget.WindowName(
                    padding = 24,
                    background=colors[3],
                    ),
                widget.Systray(
                    background=colors[3],
                    padding=10,
                    ),
                widget.Sep(
                    background=colors[3],
                    foreground=colors[3],
                    linewidth=8,
                    ),
                 widget.TextBox(
                       text = '\ue0b2',
                       font="Ubuntu Mono",
                       background = colors[3],
                       foreground = colors[4],
                       padding =-1,
                       fontsize = 24,
                       ),
                widget.CurrentLayoutIcon(
                       custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                       foreground = colors[0],
                       background = colors[4],
                       padding = 5,
                       scale = 0.7
                       ),
                 widget.TextBox(
                       text = '\ue0b2',
                       font="Ubuntu Mono",
                       background = colors[4],
                       foreground = colors[2],
                       padding =-1,
                       fontsize = 24,
                       ),
                widget.TextBox(
                       text = "  ",
                       foreground = colors[0],
                       background = colors[2],
                       padding = 0,
                       fontsize = 14
                       ),
              widget.CPU(
                       foreground = colors[0],
                       background = colors[2],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e bashtop')},
                       padding = 8
                       ),
                 widget.TextBox(
                       text = '\ue0b2',
                       font="Ubuntu Mono",
                       background = colors[2],
                       foreground = colors[5],
                       padding =-1,
                       fontsize = 24,
                       ),
                widget.TextBox(
                       text = "  ",
                       foreground = colors[0],
                       background = colors[5],
                       padding = 0,
                       fontsize = 14
                       ),
              widget.Memory(
                        measure_mem='M',
                       foreground = colors[0],
                       background = colors[5],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e htop')},
                       padding = 8
                       ),
                # widget.TextBox(
                #        text = '\ue0b2',
                #        font="Ubuntu Mono",
                #        background = colors[5],
                #        foreground = colors[2],
                #        padding =-1,
                #        fontsize = 24,
                #        ),
                 # widget.Net(
                 #       interface = "enp6s0",
                 #       format = '{down} ↓↑ {up}',
                 #       foreground = colors[0],
                 #       background = colors[2],
                 #       padding = 8
                 #       ),
                 # widget.TextBox(
                 #       text = '\ue0b2',
                 #       font="Ubuntu Mono",
                 #       background = colors[2],
                 #       foreground = colors[5],
                 #       padding =-1,
                 #       fontsize = 24,
                 #       ),
                 # widget.TextBox(
                 #        text = "  ",
                 #       foreground = colors[0],
                 #       background = colors[5], padding = 0),
                 # widget.Volume(
                 #         foreground=colors[0],
                 #         background=colors[5],
                 #         padding=10,
                 #        ),
                widget.TextBox(
                       text = '\ue0b2',
                       font="Ubuntu Mono",
                       background = colors[5],
                       foreground = colors[2],
                       padding =-1,
                       fontsize = 24,
                       ),
                widget.Clock(
                    foreground=colors[0],
                    background=colors[2],
                    format="%A %B %d - %H:%M",
                    ),
                 widget.TextBox(
                        text = '\ue0b2',
                        font="Ubuntu Mono",
                        background = colors[2],
                        foreground = colors[6],
                        padding =-1,
                        fontsize = 24,
                        ),
                widget.QuickExit(
                        default_text="⏻ ",
                        countdown_format="{}",
                        countdown_start=4,
                          foreground=colors[0],
                          background=colors[6],
                          padding=10,
                         ),
            ],
            24,
            margin=[0,0,2,0],
        ),
        bottom = bar.Gap(2),
        left = bar.Gap(2),
        right = bar.Gap(2),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

# Configuration Variables
dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = False
bring_front_click = True
cursor_warp = False
auto_fullscreen = True
auto_minimize = False
focus_on_window_activation = "focus"

floating_layout = layout.Floating(
    **layout_theme,
    float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    subprocess.call([home+'/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "Qtile"
