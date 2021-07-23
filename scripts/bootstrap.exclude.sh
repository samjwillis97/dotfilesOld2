#!/bin/bash

# https://github.com/ajmalsiddiqui/dotfiles/blob/master/bootstrap.exclude.sh

##### Inits ######

PROMPT="[ BOOTSTRAP ]"
source .exports

# Create crontabs as required

##### FUNCTIONS #####

# Echo with Prompt
function echo_with_prompt() {
	PROMPT="${PROMPT:-'[ SamsDotFiles  ]'}"
	echo "$PROMPT $@"
}

# Execute function with a prompt
function execute_func_with_prompt() {
	# Args
	# $1 - Function to call
	# $2 - Description of Function
	# Returns
	# 1, if user cancels
	# 2, if the function failed
	# 0, if all went well

	echo_with_prompt "About to $2"
	echo_with_prompt "Proceed? (y/N)"
	read resp
	
	if [ "$resp" = 'y' -o "$resp" = 'Y' ] ; then
		"$1" || return 2
		echo_with_prompt "$2 complete"
	else
		echo_with_prompt "$2 cancelled by user"
		return 1
	fi

}

function link_files {
	# Ask Folder?
	# Get Files from Said Folder
	# local reg_file=''
	for file in $(ls -d ../*/) ; do
		echo "$file"
		# comp=$(echo "$reg_file"  | sed '/([A-Z])\w/')
		# echo "$reg_file"
	done
	# for file in $(ls -A | grep -vE '\.exclude*|\.git$|\.gitignore|\.gitmodules|.*.md') ; do
		# ln -sv "$PWD/$file" "$HOME" || true
		# echo "$file"
	# done
}

# Install Tools for Arch Based System
function install_tools_arch() {
	pacman -Syyu

	# Basic Utilities
	pacman -S --noconfirm --needed vim

	# Programming Languages + Frameworks
	pacman -S --noconfirm --needed python
	pacman -S --noconfirm --needed python-pip

	pacman -S --noconfirm --needed nodejs
	pacman -S --noconfirm --needed npm

	pacman -S --noconfirm --needed go

	# Tools
	pacman -S --noconfirm --needed zsh
	pacman -S --noconfirm --needed curl
	pacman -S --noconfirm --needed base-devel

	# Misc
	pacman -S --noconfirm --needed git-delta
	pacman -S --noconfirm --needed the_silver_searcher
	pacman -S --noconfirm --needed bat

	git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
	git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

}

function install_wm_arch() {
	# ALacritty
	pacman -S --noconfirm --needed alacritty
	# QTile
	pacman -S --noconfirm --needed qtile
	# Yay
	git clone https://aur.archlinux.org/yay.git /tmp/yay
	cd /tmp/yay
	makepkg -si
}

# Get OS
function get_os() {
	local os=''
		if [ $( echo "$OSTYPE" | grep 'linux-gnu' ) ] ; then
			# File contains all required details
			source /etc/os-release
			# Set os to ID_LIKE if exists, else set to ID
			os="${ID_LIKE:-$ID}"
		else
			os="Unknown OS"
		fi
	export DETECTED_OS="$os"
}

# Create Folders
function init_dirs() {
	echo_with_prompt "Making a Projects Folder in $PATH_TO_PROJECTS if it doesn't already exist"
	mkdir -p "$PATH_TO_PROJECTS"
	echo_with_prompt "Making a Playground Folder in $PATH_TO_PLAYGROUND if it doesn't already exist"
	mkdir -p "$PATH_TO_PLAYGROUND"
}

# Install Tools
function install_tools() {
	get_os
	local os=$DETECTED_OS

	if [ "$os" = 'arch' ] ; then
		echo_with_prompt "Detected Arch Linux"
		echo_with_prompt "Installing utilities using Pacman"
		install_tools_arch
		execute_func_with_prompt install_wm_arch "Installing Qtile"
	else
		echo_with_prompt "Unknown OS"
		echo_with_prompt "$os"
		echo_with_prompt "Skipping Installation of Tools"
	fi
}

##### MAIN #####

# execute_func_with_prompt init_dirs "Initializing directories"
execute_func_with_prompt link_files "Symlink config files"
# execute_func_with_prompt install_tools "Installing tools"
