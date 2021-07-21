# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import re
import socket
import subprocess
import urllib.request

from typing import List  # noqa: F401

from libqtile import qtile, bar, layout, widget, hook, extension
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.command import lazy
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal

# Set Variables
# mod4 = Super/Windows Key
mod = "mod1"
terminal = "alacritty"
network = "enp9s0"

# Colors
color_red = "#ff5555"
color_orange = "#ffb86c"
color_yellow = "#f1fa8c"
color_cyan = "#8be9fd"
color_green = "#50fa7b"
color_pink = "#ff79c6"
color_purple = "#bd93f9"
color_comment = "#6272a4"
color_foreground = "#f8f8f2"
color_selection = "#44475a"
color_background = "#282a36"


# Panel Colors
colors = [
    [color_background, color_background],  # panel background
    [color_selection, color_selection],  # background for current screen tab
    [color_foreground, color_foreground],  # font color for group names
    [color_red, color_red],  # border line color for current tab
    # border line color for 'other tabs' and color for 'odd widgets'
    [color_purple, color_purple],
    [color_cyan, color_cyan],  # color for the 'even widgets'
    [color_cyan, color_cyan],  # window name, border foxu
    [color_pink, color_pink],  # backbround for inactive screens
    [color_background, color_background],  # inactive window border color
]

# Themes
layout_theme = {
    "border_width": 2,
    "margin":5,
    "border_focus": colors[6][0],
    "border_normal": colors[8][0],
}


# Default Widget Settings
widget_defaults = dict(
    font="Ubuntu Mono",
    fontsize=12,
    padding=2,
    background=colors[2],
)
def get_public_ip():
    public_ip = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
    return str(public_ip)


keys = [
    # QTile
    Key([mod, "shift"], "r", lazy.restart(),
        desc="Restart Qtile"),
    Key([mod, "shift", "control"], "q", lazy.shutdown(),
        desc="Shutdown Qtile"),

    # Essentials
    Key([mod], "Return", lazy.spawn(terminal),
        desc="Launches My Terminal"),
    Key([mod], "e", lazy.spawn("Thunar"),
        desc="Launches file explorer"),
    Key([], "Print", lazy.spawn("flameshot screen")),
    Key([mod], "Print", lazy.spawn("flmaeshot gui")),

    # GUI
    Key(["mod4"], "Right", lazy.spawn("variety -n")),
    Key(["mod4"], "Left", lazy.spawn("variety -p")),
    Key(["mod4"], "Up", lazy.spawn("variety -f")),
    Key(["mod4"], "Down", lazy.spawn("variety -t")),

    # ROFI Chords
    Key([mod], "d", lazy.spawn("rofi -show run"),
        desc="Run Launcher"),

    Key([mod], "Tab", lazy.spawn("rofi -show"),
        desc="Run Rofi window siwtcher"),

    KeyChord([mod], "p", [
        Key([], "r",
            lazy.spawn("rofi -show run"),
            desc="Run Rofi Launcher"),
        Key([], "Tab",
            lazy.spawn("rofi -show"),
            desc="Run Rofi Window Switcher"),
        Key([], "s",
            lazy.spawn("rofi -show ssh"),
            desc="Run Rofi SSH launcher"),
        Key([], "f",
            lazy.spawn("rofi -show file-browser")),
        Key([], "c",
            lazy.spawn("rofi -show calc")),
        Key([], "p",
            lazy.spawn("rofi-pass -show")),
        Key([], "u",
            lazy.spawn('UDISKIE_DMENU_LAUNCHER="rofi" udiskie-dmenu -matching regex -dmenu -i -no-custom -multi-select'))
    ]),

    # Layouts
    Key([mod], "space", lazy.next_layout(),
        desc="Toggle through layouts"),
    Key([mod, "shift"], "Tab", lazy.layout.rotate(), lazy.layout.flip(),
        desc="Switch which side main pain occurrs"),

    # Windows
    Key([mod, "shift"], "q", lazy.window.kill(),
        desc="Kill active window"),
    Key([mod, "shift"], "f", lazy.window.toggle_floating(),
        desc="toggle floating"),
    Key([mod], "f", lazy.window.toggle_fullscreen(),
        desc="toggle fullscreen"),

    # Switch between windows
    Key([mod], "h", lazy.layout.left(),
        desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(),
        desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(),
        desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(),
        desc="Move focus up"),

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
    Key([mod, "control"], "h", lazy.layout.grow_left(),
        desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(),
        desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(),
        desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(),
        desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(),
        desc="Reset all window sizes"),

    # Monitor Toggling
    Key([mod], "period", lazy.next_screen(),
        desc="Move focus to next monitor"),
    Key([mod], "comma", lazy.prev_screen(),
         desc="Move focus to previous monitor"),

    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"),

    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"),

    # MULTIMEDIA KEYS
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%")),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("light -A 2")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("light -U 2")),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
]

group_names = [
    ("1", {'layout': 'bsp'}),
    ("2", {'layout': 'bsp'}),
    ("3", {'layout': 'bsp'}),
    ("4", {'layout': 'bsp'}),
    ("5", {'layout': 'bsp'}),
    ("6", {'layout': 'bsp'}),
    ("7", {'layout': 'bsp'}),
    ("8", {'layout': 'bsp'}),
    ("9", {'layout': 'bsp'}),
]

groups = [Group(name, **kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    # switch to another group
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))
    # send current window to group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name)))


layouts = [
    layout.MonadTall(**layout_theme),
    layout.Columns(**layout_theme),
    layout.Max(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Floating(**layout_theme),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    layout.Bsp(**layout_theme, fair=False),
    # layout.Matrix(**layout_theme),
    # layout.MonadTall(**layout_theme),
    # layout.MonadWide(**layout_theme),
    # layout.RatioTile(**layout_theme),
    # layout.Tile(**layout_theme),
    # layout.TreeTab(**layout_theme),
    # layout.VerticalTile(**layout_theme),
    # layout.Zoomy(**layout_theme),
]

extension_defaults = widget_defaults.copy()


def init_top_widgets():
    top_widgets_list = [
        widget.Sep(
            linewidth=0,
            padding=10,
            foreground=colors[2],
            background=colors[0]
        ),
        widget.Image(
            filename = "~/.config/qtile/icons/python-white.png",
            scale = "False",
            background=colors[0],
            mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal)}
        ),
        widget.Sep(
            linewidth=0,
            padding=10,
            foreground=colors[2],
            background=colors[0]
        ),
        widget.GroupBox(
            font="Ubuntu Bold",
            fontsize=12,
            margin_y=3,
            margin_x=0,
            padding_y=5,
            padding_x=6,
            borderwidth=2,
            active=colors[2],
            inactive=colors[7],
            rounded=False,
            highlight_color=colors[1],
            highlight_method="line",
            this_current_screen_border=colors[6],
            this_screen_border=colors[4],
            other_current_screen_border=colors[6],
            other_screen_border=colors[4],
            foreground=colors[2],
            background=colors[0]
        ),
        widget.Spacer(
            background=colors[0],
        ),
        widget.WindowName(
            foreground=colors[6],
            background=colors[0],
            padding=0,
            width=bar.CALCULATED
        ),
        widget.Spacer(
            background=colors[0],
        ),
        # widget.Systray(
        #     background=colors[0],
        #     padding=5
        # ),
        widget.ThermalSensor(
            foreground=[color_cyan, color_cyan],
            background=colors[0],
            threshold=90,
            padding=5
        ),
        widget.Sep(
            linewidth=1,
            padding=20,
            foreground=colors[2],
            background=colors[0],
            size_percent=50
        ),
        widget.CPU(
            foreground=[color_green, color_green],
            background=colors[0],
            format="CPU: {load_percent}%",
            mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(
                terminal + ' -e htop')},
            padding=5
        ),
        widget.Sep(
            linewidth=1,
            padding=20,
            foreground=colors[2],
            background=colors[0],
            size_percent=50
        ),
        widget.Memory(
            foreground=[color_yellow, color_yellow],
            background=colors[0],
            format="RAM: {MemPercent}%",
            mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(
                terminal + ' -e htop')},
            padding=5
        ),
        widget.Sep(
            linewidth=1,
            padding=20,
            foreground=colors[2],
            background=colors[0],
            size_percent=50
        ),
        widget.TextBox(
            text="Vol:",
            foreground=[color_orange, color_orange],
            background=colors[0],
            padding=0
        ),
        widget.Volume(
            foreground=[color_orange, color_orange],
            background=colors[0],
            padding=5
        ),
        widget.Sep(
            linewidth=1,
            padding=20,
            foreground=colors[2],
            background=colors[0],
            size_percent=50
        ),
        widget.Clock(
            foreground=[color_red, color_red],
            background=colors[0],
            format="%A, %B %d - %H:%M "
        ),
    ]
    return top_widgets_list

def init_bot_widgets():
    bot_widgets_list = [
        widget.Sep(
            linewidth=0,
            padding=10,
            foreground=colors[2],
            background=colors[0]
        ),
        widget.TextBox(
            text="⟳",
            padding=4,
            foreground=[color_yellow, color_yellow],
            background=colors[0],
            fontsize=14
        ),
        widget.CheckUpdates(
            update_interval=1800,
            padding=2,
            distro="Arch_checkupdates",
            display_format=" {updates} Updates",
            foreground=[color_yellow, color_yellow],
            colour_no_updates=[color_yellow, color_yellow],
            colour_have_updates=[color_orange, color_orange],
            mouse_callbacks={'Button1': lambda: qtile.cmd_spawn(
                terminal + ' -e "sudo pacman -Syu"')},
            background=colors[0],
            no_update_string = " Up to Date"
        ),
        widget.Sep(
            linewidth=1,
            padding=20,
            foreground=colors[2],
            background=colors[0],
            size_percent=50
        ),
        widget.OpenWeather(
            background=colors[0],
            foreground=[color_pink, color_pink],
            cityid="2171766",
        ),
        widget.Spacer(
            background=colors[0],
        ),
        widget.Net(
            interface=network,
            format='{down} ↓ ',
            foreground=[color_cyan, color_cyan],
            background=colors[0],
            padding=2,
        ),
        widget.GenPollText(
            foreground=[color_purple, color_purple],
            background=colors[0],
            padding=10,
            func=get_public_ip,
            update_interval=6000,
        ),
        widget.Net(
            interface=network,
            format=' ↑ {up}',
            foreground=[color_green, color_green],
            background=colors[0],
            padding=2,
        ),
        widget.Spacer(
            background=colors[0],
        ),
        widget.DF(
            background=colors[0],
            foreground=[color_orange, color_orange],
            visible_on_warn=False,
            format="Disk: {r:.0f}GB/{s}GB"
        ),
        widget.Sep(
            linewidth=1,
            padding=20,
            foreground=colors[2],
            background=colors[0],
            size_percent=50
        ),
        widget.CurrentLayoutIcon(
            custom_icon_paths=[os.path.expanduser(
                "~/.config/qtile/icons")],
            foreground=colors[0],
            background=colors[0],
            padding=2,
            scale=0.65
        ),
        widget.CurrentLayout(
            foreground=colors[2],
            background=colors[0],
            padding=5
        ),
        widget.Sep(
            linewidth=0,
            padding=10,
            foreground=colors[2],
            background=colors[0]
        ),
    ]
    return bot_widgets_list

# Setting up Screens


def init_top_widgets_screen1():
    widgets_screen1 = init_top_widgets()
    return widgets_screen1

def init_bot_widgets_screen1():
    widgets_screen1 = init_bot_widgets()
    return widgets_screen1

def init_top_widgets_screen2():
    widgets_screen2 = init_top_widgets()
    return widgets_screen2

def init_bot_widgets_screen2():
    widgets_screen2 = init_bot_widgets()
    return widgets_screen2

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_top_widgets_screen1(), opacity=1.00, size=20),
                   bottom=bar.Bar(widgets=init_bot_widgets_screen1(), opacity=1.00, size=20)),
            Screen(top=bar.Bar(widgets=init_top_widgets_screen2(), opacity=1.00, size=20),
                   bottom=bar.Bar(widgets=init_bot_widgets_screen2(), opacity=1.00, size=20))]


if __name__ in ["config", "__mwidgets_screen1ain__"]:
    screens = init_screens()
    top_widgets_list = init_top_widgets()
    bot_widgets_list = init_bot_widgets()
    top_widgets_screen1 = init_top_widgets_screen1()
    bot_widgets_screen1 = init_bot_widgets_screen1()
    top_widgets_screen2 = init_top_widgets_screen2()
    bot_widgets_screen2 = init_bot_widgets_screen2()

# Essential functions
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)


def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)


def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)


def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)


def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='Thunar'), # thunar
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
