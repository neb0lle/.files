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
alt = "mod1"
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
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(),desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(),desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(),desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(),desc="Move window up"),
    Key([mod, "shift"], "n",lazy.layout.client_to_next(),desc="move window to next stack"),

    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, alt], "h",resize_left,desc="Grow window to the left"),
    Key([mod, alt], "l",resize_right,desc="Grow window to the right"),
    Key([mod, alt], "j",resize_down,desc="Grow window down"),
    Key([mod, alt], "k",resize_up, desc="Grow window up"),

    # Rotation of windows
    Key([mod], "r",lazy.layout.rotate(),desc="Rotate windows in Stack mode"),
    Key([mod,"control"], "j",lazy.layout.flip_left(),desc="Flip windows towards left"),
    Key([mod,"control"], "k",lazy.layout.flip_right(),desc="Flip windows towards right"),

    # Toggle between different layouts as defined below
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod],"y",lazy.window.toggle_floating(),desc="Toggle floating on focused window",),
    Key([mod],"m",lazy.window.toggle_minimize(),desc="Toggle Minimize"),
    Key([mod,"control"], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
    Key([mod], "Tab", lazy.next_layout(),desc="Toggle next layout"),
    Key([mod, "shift"], "Tab", lazy.prev_layout(),"Toggle previous layout"),

    # Qtile
    Key([mod, "control"], "r", lazy.restart(), desc="Restart Qtile"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

    # Group Changer
    Key([mod, "control"], "l", lazy.screen.next_group(),desc="Switch to next group"),
    Key([mod, "control"], "h", lazy.screen.prev_group(),desc="Switch to previous group"),
    Key([mod], "u", lazy.next_urgent(),desc="Switch to urgent window"),

]

# Display kebindings in rofi menu
def show_keys():
    key_help = ""
    for k in keys:
        mods = ""

        for m in k.modifiers:
            if m == "mod4":
                mods += "Super + "
            else:
                mods += m.capitalize() + " + "

        if len(k.key) > 1:
            mods += k.key.capitalize()
        else:
            mods += k.key

        key_help += "{:<30} {}".format(mods, k.desc + "\n")

    return key_help

]

colors = [["#000000","#000000"], # BLACK
          ["#ffffff","#ffffff"], # WHITE
          ["#01fdb0","#01fdb0"], # MINT
          ["#131519","#131519"], # DARK GREY
          ["#46474f","#46474f"], # LIGHT GREY
          ["#ffff44","#ffff44"], # YELLOW
          ["#ff4444","#ff4444"], # SALMON
          ["#00a2ff","#00a2ff"], # BLUE
          ["#ff54c4","#ff54c4"]] # MAGENTA

def init_group_names():
    return [("I",{'layout':'bsp'}),
            ("II",{'layout':'bsp'}),
            ("III",{'layout':'bsp'}),
            ("IV",{'layout':'bsp'}),
            ("V",{'layout':'bsp'}),
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
        "border_width":1,
        "margin":4,
        "border_normal":"131519",
        "border_focus":"46474f",
        "grow_amount": 4,
        }
layouts = [
    layout.Bsp(**layout_theme,fair=False),
    layout.Stack(num_stacks=1,margin=4,border_width=0),
    layout.Stack(num_stacks=2,**layout_theme),
   # layout.Max(),
   # layout.Columns(),
   # layout.Floating(),
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
                widget.Sep(
                    background=colors[3],
                    foreground=colors[3],
                    linewidth=4,
                ),
                widget.GroupBox(
                    font = "Nimbus Sans, Bold",
                    padding=4,
                    margin_y=5,
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
                widget.Sep(
                    background=colors[3],
                    foreground=colors[3],
                    linewidth=15,
                ),
                widget.WindowName(
                    padding = 24,
                    background=colors[3],
                    ),
                widget.Sep(
                    background=colors[3],
                    foreground=colors[3],
                    linewidth=8,
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
                       text = '|',
                       background = colors[3],
                       foreground = colors[4],
                       padding =-3,
                       fontsize = 20,
                       ),
                widget.CurrentLayoutIcon(
                       custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                       foreground = colors[0],
                       background = colors[3],
                       padding = 3,
                       scale = 0.6
                       ),
                 widget.TextBox(
                       text = '|',
                       background = colors[3],
                       foreground = colors[4],
                       padding =-3,
                       fontsize = 20,
                       ),
                widget.Battery(
                    background = colors[3],
                    foreground = colors[2],
                    low_foreground = colors[6],
                    low_percentage = 0.1,
                    full_char = "",
                    charge_char = "",
                    discharge_char = "",
                    empty_char = "",
                    noify_below = 10,
                    format = '{char} {percent:1.0%}',
                    update_interval =1,
                ),
                 widget.TextBox(
                       text = '|',
                       background = colors[3],
                       foreground = colors[4],
                       padding =-3,
                       fontsize = 20,
                       ),
                widget.TextBox(
                    text = "  ",
                       foreground = colors[1],
                       background = colors[3],
                       padding = -3,
                       fontsize = 16
                       ),
                widget.Backlight(
                    backlight_name="amdgpu_bl0",
                    background = colors[3],
                    foreground= colors[1],
                ),
                 widget.TextBox(
                       text = '|',
                       background = colors[3],
                       foreground = colors[4],
                       padding =-3,
                       fontsize = 20,
                       ),
                widget.TextBox(
                       text = "  ",
                       foreground = colors[8],
                       background = colors[3],
                       padding = -3,
                       fontsize = 16
                       ),
                widget.Volume(
                    background = colors[3],
                    foreground = colors[8],
                    padding = 8,
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('pavucontrol')},
                ),
                 widget.TextBox(
                        text = '|',
                        background = colors[3],
                        foreground = colors[4],
                        padding =-3,
                        fontsize = 20,
                        ),
                widget.TextBox(
                       text = "  ",
                       foreground = colors[2],
                       background = colors[3],
                       padding = 0,
                       fontsize = 14
                       ),
                widget.CPU(
                       foreground = colors[2],
                       background = colors[3],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e bashtop')},
                       padding = 8
                       ),
                 widget.TextBox(
                        text = '|',
                        background = colors[3],
                        foreground = colors[4],
                        padding =-3,
                        fontsize = 20,
                        ),
                widget.TextBox(
                       text = "  ",
                       foreground = colors[5],
                       background = colors[3],
                       padding = 0,
                       fontsize = 14
                       ),
              widget.Memory(
                        measure_mem='M',
                       foreground = colors[5],
                       background = colors[3],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e htop')},
                       padding = 8
                       ),
                 widget.TextBox(
                        text = '|',
                        background = colors[3],
                        foreground = colors[4],
                        padding =-3,
                        fontsize = 20,
                        ),
                widget.TextBox(
                       text = "  ",
                       foreground = colors[7],
                       background = colors[3],
                       padding = 0,
                       fontsize = 14
                       ),
                widget.Clock(
                    foreground=colors[7],
                    background=colors[3],
                    format="%A %B %d - %H:%M",
                    ),
                 widget.TextBox(
                        text = '|',
                        background = colors[3],
                        foreground = colors[4],
                        padding =-3,
                        fontsize = 20,
                        ),
                widget.QuickExit(
                        default_text="⏻ ",
                        countdown_format="{}",
                        countdown_start=4,
                        foreground=colors[6],
                        background=colors[3],
                        padding=10,
                         ),
            ],
            30,
            # opacity=0.6,
            margin=[6,6,2,6],
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
    Match(title='Qalculate'),
])

# Configuration Variables
dgroups_key_binder = None
dgroups_app_rules = []  # type: List
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
auto_fullscreen = True
auto_minimize = False
focus_on_window_activation = "focus"


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
