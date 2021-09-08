# Listing Files
alias l='ls -l'
alias ll='ls -alFh'
alias lt='ls --human-readable --size -1 -S --classify'

# View Only Mounted Devices
alias mnt="mount | awk -F' ' '{ printf \"%s\t%s\n\",\$1,\$3;  }' | column -t | egrep ^/dev/ | sort""'"

# Copy with Progess Bar
alias cpv='rsync -ah --info=progress2'

# Untar
alias untar='tar -zxvf'

alias python='python3'
alias pip='pip3'

gsettings set org.gnome.gnome-flashback desktop false

export PATH="$HOME/.local/bin:$PATH"
