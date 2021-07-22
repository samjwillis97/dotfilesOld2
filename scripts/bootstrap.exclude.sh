#!/bin/bash

# https://github.com/ajmalsiddiqui/dotfiles/blob/master/bootstrap.exclude.sh

##### Inits ######

PROMPT="[ BOOTSTRAP ]"
source .exports

# Symlink all dotfiles
## Ignore errors because files may already exist

# Install Requirement
## Change per OS

# Create Some Folders as required

# Create crontabs as required

##### FUNCTIONS #####

# Echo with Prompt
function echo_with_prompt() {
	PROMPT="${PROMPT:-'[ SamsDotFiles  ]'}"
	echo "$PROMPT $@"
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
	echo "$os"
}

# Create Folders
function init_dirs() {
	echo_with_prompt "Making a Projects Folder in $PATH_TO_PROJECTS if it doesn't already exist"
}

##### MAIN #####

get_os

init_dirs
