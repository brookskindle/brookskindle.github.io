Title: Installing Arch Linux
Date: 2020-09-23
Category: Programming
Tags: operating systems, arch, minimal, linux

I'm installing [Arch Linux](https://www.archlinux.org/) on my computer.

This shouldn't come as a surprise. If you've known me for long enough, you'll
know that every six months or so I get the urge to wipe my system and do a
clean install. For me, it's that same clean feeling you get after spending a
day cleaning your house, and I love it. At the same time, I also enjoy
experimenting with new things, so oftentimes a reinstallation will end up with
me trying a different Linux distribution than the one I was previously on.

If I had to document my history with Linux, the tl;dr would be something like

* Late 1990s or early 2000s. Our family buys SUSE Linux, the predecessor to
  openSUSE. Being the child that I was, I use it for videogames like Frozen
  Bubble, and later, RuneScape.

* 2010 or thereabouts (high-school). I install linux on a lab machine as part
  of an assignment. I get a good grade and feel like a hacker.

* 2013, college. Most of the students in my computer science classes (myself
  included) are using Windows. A group of several top students are using Linux.
  In awe of their computing prowess, and wanting to fit in, I befriend them and
  they help me install Linux Mint on my laptop.

* 2013-2015, college also. The command line is scary, but I commit myself to
  learning its ways by taking all of my notes in vim. My laptop dies and for a
  brief time and I use a Raspberry Pi (with the Raspbian OS) until I can get a
  replacement computer. The netbook I order arrives and I install Lubuntu on
  it. I also buy a desktop system for video games, but dual boot Windows with
  Linux Mint. Reinstall time! I dabble briefly with Ubuntu on my desktop, but
  finally settle on Crunchbang because the UI looks absolutely amazing.

* 2015-2019. Work lets me install my own operating system and I choose Xubuntu
  because it's easy to set up and allows me to focus on what's important.

* 2019+. I switch jobs and now use a Macbook. The command line experience is
  almost identical thanks to my heavy use of tmux, but the tiling window
  manager setup I had when I was using Linux daily is now gone and I miss it.
  On my personal computer, I install Arch Linux because it seems hard to do.
  Eventually, I get curious again and try Manjaro, i3 community edition.

Which brings me to today. I've used Arch before, but I'm drawn back to it for
several reasons:

* I like the pacman package manager as well as the concept of a rolling release
  distribution
* The idea of having a minimal system that contains only what I want and
  nothing else is appealing to me.

This post documents the steps that I took to install and set up the system.

## Prerequisites
Download and verify the latest [Arch Linux
ISO](https://www.archlinux.org/download/) and make a bootable USB drive with
the image. I did this with the `dd` command. Then: restart your machine, boot
from your new install media, and after a short while you will be greeted with a
single prompt.
```console
#
```

And that's pretty much it. Unlike other operating systems, there is no
graphical installer to guide you. There is no console based one, either.
Instead, there is the ArchWiki's [installation
guide](https://wiki.archlinux.org/index.php/Installation_guide), which covers
in detail the commands to run in order to install the system yourself. This
spartan approach to installation can be intimidating to beginners and experts
alike (myself included), but the end result is a system completely customized
to the wants and needs of the owner.

## Installation steps

### Connect to the internet
Hard-wired connections shouldn't have to worry about this step, but if you're
connecting via wifi like me, you can use the interactive `iwctl` command to
connect
```
# iwctl
[iwctl] station wlan0 scan
[iwctl] station wlan0 get-networks
                  Available networks
------------------------------------------------------
    Network name                    Security  Signal
-----------------------------------------------------
    One Cute Cottage                psk       ****
    XFINITY                         8021x     ***
    Prejudice                       psk       ***
    Pride                           psk       **
    Andromeda_2.4GHz                psk       **
    Bassoon                         psk       *
    Bhaati - 2.4GHz                 psk       ***
[iwctl] station wlan0 connect "One Cute Cottage"
Enter passphrase:
```
and then verify the connection with `ping archlinux.org`.

### Installation guide
At this point, if you need to refer back to the guide, you can optionally run
`Installation_guide` which opens up the Arch Wiki's [Installation
guide](https://wiki.archlinux.org/index.php/Installation_guide) in `w3m`, a
command line web browser. It's not the best user experience but it gets the job
done, especially if you don't have another device with which to access the
guide. Use `alt` + (`left` or `right`) to switch to a new virtual console and
continue the installation from there.

### NTP server
Just like how wall clocks slowly become out of sync with the current time, so
too, does your computer. To fix this, your computer can use the Network Time
Protocol to synchronize itself with a list of known accurate time servers to
prevent itself from drifting.
```console
# timedatectl set-ntp true
```
Verify with `timedatectl status`

### Drive setup
One of the most important steps, and also the one that will vary the most among
installations. To keep things simple, I'll walk you through the approach that I
took: A single encrypted filesystem with a separate `/boot` partition.

With `cfdisk`, create two partitions.

* A 300M EFI partition that will be used for `/boot`
* The rest of the space will contain the Linux filesystem. I have enough RAM on
  my machine that I don't want or need swap.

```
# cfdisk /dev/nvme0n1
```

If you're unsure of your drive name, you can use `lsblk` to find out.
You can additionally use it to verify the your partition changes were
successfully written to disk.
```
# lsblk
NAME          MAJ:MIN RM   SIZE RO TYPE  MOUNTPOINT
nvme0n1       259:0    0 476.9G  0 disk
├─nvme0n1p1   259:1    0   300M  0 part
└─nvme0n1p2   259:2    0 476.6G  0 part
```

From here, ensure the boot partition is formatted as `fat32`.
```
# mkfs.vfat -F 32 /dev/nvme0n1p1
```

Encrypt the root partition and format the opened drive as `ext4`.
```
# cryptsetup -y -v luksFormat /dev/nvme0n1p2
Enter password:
Verify password:
# cryptsetup open /dev/nvme0n1p2 cryptroot
# mkfs.ext4 /dev/mapper/cryptroot
```

### Chroot
The goal of this section is to configure your system just enough so that
restarting the computer will allow it to boot without the help of the install
disk. We can do that by performing a `chroot`, a command that tricks a subshell
into thinking the filesystem root directory is that of our formatted drives,
rather than the usb-drive we booted from, and then configuring the operating
system from there.

However, before chrooting, we must first mount the filesystem
```
# mount /dev/mapper/cryptroot /mnt
# mkdir /mnt/boot
# mount /dev/nvme0n1p1 /mnt/boot
```

generate the filesystems table
```
# genfstab -U /mnt >> /mnt/etc/fstab
```

and install a few packages into our system. At a minimum, this should be
```
# pacstrap /mnt base linux linux-firmware
```
This will give us the very basic set of commands post-chroot. Finally, we can
enter the system
```
# arch-chroot /mnt
```

At this point, you will see the prompt change from a `#` to a `$`, indicating
we've left the install media and are now running a shell from within the
filesystem we just set up.

Set the root password
```console
$ passwd
```

and install any additional packages you need that weren't included in the
previous `pacstrap` step. For me, I need an editor while configuring the
system, and a wifi daemon so that, post-reboot, I can connect and continue the
setup.
```console
$ sudo pacman -Sy
$ sudo pacman -S vim iwd
```

What next?

Set the timezone and locale
```console
$ ln -sf /usr/share/zoneinfo/America/Los_Angeles /etc/localtime
$ hwclock --systohc
$ vim /etc/locale.gen  # uncomment the en_US.UTF-8 line
$ locale-gen
$ echo LANG=en_US.UTF-8 > /etc/locale.conf
```

Set the hostname
```
$ echo midnight > /etc/hostname
$ vim /etc/localhost
127.0.0.1 localhost
::1 localhost
127.0.0.1 midnight.localdomain midnight
```

```console
$ pacman -S base-devel man-db man-pages
```

Edit `/etc/mkinitcpio.conf`, add `sd-encrypt` to the HOOKS section, and swap
`udev` with `systemd`. More information on hooks is on the
[mkinitcpio](https://wiki.archlinux.org/index.php/Mkinitcpio#Common_hooks)
ArchWiki page
```text
HOOKS=(base systemd autodetect modconf block filesystems keyboard sd-encrypt fsck)
```
Regenerate it with `mkinitcpio -p linux`

Configure the bootloader to

* turn on [microcode](https://wiki.archlinux.org/index.php/microcode) updates
* mount our encrypted root directory on boot

```console
$ sudo pacman -S intel-ucode
```
```
$ bootctl install
$ vim /boot/loader/entries/arch.conf
title	Archlinux
linux	/vmlinuz-linux
initrd	/intel-ucode.img
initrd	/initramfs-linux.img
options	rw rd.luks.name=fdd06c74-7d25-4542-841f-7ca3ec8b4f50=cryptroot root=/dev/mapper/cryptroot
```
Where UUID is the UUID of the encrypted linux filesystem (`/dev/nvme0n1p2`),
found with `blkid` or `lsblk -f`.

```console
$ bootctl update
$ bootctl list  # verify archlinux entry is there
```

## Post-installation setup
At this point, `reboot` the system and log in as `root` with the password you
set before.

### Wireless
Like before, we can use `iwctl` (provided by the `iwd` package) to connect to
wifi. Unlike before, however, we do not automatically get an ip address, so we
must dhcp. `iwd` has its own functionality for this, so we must simply edit the
configuration file and enable it. In the past I've used `dhcpcd`, but the
program requires root to start, whereas the `iwd` daemon can be enabled to
automatically start on boot.
```
$ vim /etc/iwd/main.conf
[General]
EnableNetworkConfiguration=true
$ systemctl enable iwd
```

### Create your user
The goal is to create your own user account and prevent `root` from logging in
via password.
```console
$ pacman -S sudo
$ useradd --create-home brooks
$ passwd brooks
$ usermod -a -G wheel brooks
$ vim /etc/sudoers  # and uncomment the wheel line
$ su -l brooks
$$ sudo su  # Ensure sudo works
$ passwd --lock root  # Once sudo is verified, prevent root from logging in
```
On the next reboot, you can sign in as your user instead of `root`

### zsh + development environment
For general development environment setup, these are the programs I use often.
```console
$ sudo pacman -S zsh zsh-autosuggestions zsh-syntax-highlighting
$ chsh -s /bin/zsh brooks
```

```console
$ sudo pacman -Sy
$ sudo pacman -S git tmux stow
$ sudo pacman -S neovim the_silver_searcher fd bat fzf \
                 acpi neofetch nodejs python npm openssh
```

```console
$ mkdir ~/build && cd ~/build
$ git clone https:/aur.archlinux.org/yay.git
$ cd yay
$ makepkg -si
$ yay -S xcwd-git
```

I have an Apple magic keyboard and want to swap the `fn` and `ctrl` key.
```console
$ yay -S hid-apple-patched-git-dkms
$ sudo mkinitcpio -P all
```

### Graphical server
So far, we've been configuring our system without the use of a graphical
server. I prefer the [i3 tiling window manager](https://i3wm.org/), and this
time around I'm using it without a display manager.
```console
$ sudo pacman -S i3-gaps i3blocks \
                 xorg-xinit xorg-xmodmap xorg-server \
                 arandr termite rofi chromium
```
A graphical environment can be started at any time using `startx`.

### Audio
```console
$ sudo pacman -S pulseaudio pavucontrol
```
In my i3config, I use `pactl` to map volume control to a few keys. Can be
started with `start-pulseaudio-x11`

### Video
Luckily I didn't have to set anything up in order to support video streaming
from my webcam

### Backlight
```console
$ sudo pacman -S xbacklight xf86-video-intel
$ reboot
```
Backlight controls from `xbacklight` doesn't work unless video drivers are
installed. I have an Intel-based machine, hence `xf86-video-intel`.

### Screensaver
```console
$ sudo pacman -S xautolock i3lock-color
```

### Font installation
```console
$ sudo pacman -S ttf-hack ttf-font-awesome noto-fonts-emoji
```
[Hack](https://sourcefoundry.org/hack/) as my general font, and [Font
Awesome](https://fontawesome.com/) for icon support on my status bar. The [Noto
Emoji Fonts](https://www.google.com/get/noto/help/emoji/) is a font designed by
Google. Once installed, all our applications (Chromium, Termite, i3blocks,
rofi, etc...) can support emoji rendering.

For example, This is the fox face emoji: 🦊, but without an emoji font
installed, my terminal and browser would render it as a white box.

Another interesting thing that I learned about emojis while configuring support
for it is that a lot of the more complex emojis are actually multiple code
points. For example, 👍🏻 is simply the combination of two emojis right next to
each other: 👍 and 🏻.

### Gtk / Theming
The default gtk theme, Raleigh, isn't the best in my opinion, and the `Arc`
theme is a good default dark theme.
```console
$ sudo pacman -S lxappearance arc-gtk-theme
$ yay -S xcursor-breeze
```
Use `lxappearance` to change the theme and mouse pointer

### File manager
On the command line
```console
$ sudo pacman -S ranger w3m
```
`w3m` can be used to preview images from the command line

---

And that's it for now. [My dotfiles are on
Github](https://github.com/brookskindle/dotfiles), if you want to take a look
at the configuration yourself.
