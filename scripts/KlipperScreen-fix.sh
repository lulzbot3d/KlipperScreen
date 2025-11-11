#!/bin/bash

# A script for fixing KlipperScreen update config and dependencies.
# Nov 7, 2025 - LulzBot

# Path to the flag file that indicates this has been done already
FLAG="$HOME/printer_data/config/.klipperscreen_updated"

# Exit if already run
if [ -f "$FLAG" ]; then
    echo "KlipperScreen fix already applied. Exiting."
    echo "To force this script to run again, delete the file: $FLAG"
    echo "and run this script again."
    exit 0
fi

# The first part of this script updates the Moonraker config file with the
# new method for handling dependency updates for KlipperScreen.

echo "Updating Moonraker config for KlipperScreen updates."

# Moonraker config path for typical Klipper installations
CONF="$HOME/printer_data/config/moonraker.conf"

# Backup first
cp "$CONF" "$CONF.bak_$(date +%Y%m%d_%H%M%S)"

sed -i '/^\[update_manager KlipperScreen\]/,/^\[/{
    s|^env:.*|virtualenv: ~/.KlipperScreen-env|;
    s|^install_script:.*|system_dependencies: scripts/system-dependencies.json|;
}' "$CONF"

echo "Done."
echo "A backup was saved as: $CONF.bak_<timestamp>"
echo


# The second part of this script installs any missing dependencies for KlipperScreen.

# So here's the story.  At some point in the past, a dependencies were added to KlipperScreen
# that don't get installed properly with our current Moonraker.conf update manager settings.
# Hopefully the update manager config was fixed above so that won't happen in the future.
# But for now, we need to manually install the missing dependencies.
# So the below was copied and changed a bit from the klippersceen install script to
# activate the virtual environment and install the dependencies properly.

cd ~/KlipperScreen
SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
KSPATH=$(sed 's/\/scripts//g' <<< $SCRIPTPATH)
KSENV="${KLIPPERSCREEN_VENV:-${HOME}/.KlipperScreen-env}"

source ${KSENV}/bin/activate

# Going to force install these just in case the users KlipperScreen-requirements.txt is out of date.
# They'll be already there when the update that needs them comes through.
pip --disable-pip-version-check install sdbus sdbus_networkmanager psutil

# Check if the installs were successful
if [ $? -gt 0 ]; then
    echo "Unable to install dependencies, aborting install."
    deactivate
    exit 1
fi

# Then install any other dependencies that may be missing.
pip --disable-pip-version-check install -r ${KSPATH}/scripts/KlipperScreen-requirements.txt

# Check if the installs were successful
if [ $? -gt 0 ]; then
    echo "Unable to install dependencies, aborting install."
    deactivate
    exit 1
fi

deactivate
echo "Dependencies installed successfully."
# Create the flag file to prevent future runs
touch "$FLAG"
exit 0
