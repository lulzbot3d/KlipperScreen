#!/bin/bash

# A helper script to run the KlipperScreen-fix.sh script in a text terminal
# Nov 7, 2025 - LulzBot

# Switch to text terminal and run the KlipperScreen-fix script there.
# openvt allocates a new login/terminal and runs a command inside it,
# but openvt needs to be run with sudo, but that launches the script
# as root, which breaks it, so the second sudo runs the script as biqu

sudo openvt -s -w -- sudo -u "biqu" ~/KlipperScreen/scripts/KlipperScreen-fix.sh
