#!/bin/bash

# A helper script to run the KlipperScreen-fix.sh script in a text terminal
# Nov 10, 2025 - LulzBot

# Switch to text terminal and run the KlipperScreen-fix script there,
# so the user can see what's happening on the touchscreen.

# So after figuring out I can switch terminals with openvt, I found
# it is not installed in our image for the CB1.  So I am going to just
# drop the binary in the /home/buqu/.local/bin folder and make it executable.
# That way Git will not complain it is modified when I set it executable.
# I know this is a bit hacky, but I have been fighting chicken and egg
# problems for days to get this to work.  I do not really want to use
# apt to install it in the same script where I want to use it.
cp /home/biqu/KlipperScreen/scripts/openvt /home/biqu/.local/bin/openvt
chmod +x /home/biqu/.local/bin/openvt

# openvt allocates a new login/terminal and runs a command inside it,
# but openvt needs to be run with sudo, but that launches the script
# as root, which breaks it, so the second sudo runs the script as biqu
sudo /home/biqu/.local/bin/openvt -s -w -- sudo -u "biqu" ~/KlipperScreen/scripts/KlipperScreen-fix.sh
