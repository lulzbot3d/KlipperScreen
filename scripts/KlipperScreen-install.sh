#!/bin/bash

# KlipperScreen dependency installer script -- LulzBot -- November 2025

# So here's the story.  At some point in the past, a dependency was added to KlipperScreen
# that doesn't get installed properly. Moonraker's update manager calls KlipperScreen-install.sh,
# which should install dependencies, but it doesn't work when called from the update manager,
# maybe because it's interactive and ends up waiting for user input that never comes.
# This script is a workaround to just install the dependencies properly when called by the
# update manager.  I just copied the relevant parts of the original KlipperScreen-install.sh.
# I had to replace the existing KlipperScreen-install.sh script because the update manager
# is hardcoded to call that script, and I can't change the moonraker.conf file to call a
# different script, because it's not located in the lulzbot-config repository.

SCRIPTPATH="$( cd "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
KSPATH=$(sed 's/\/scripts//g' <<< $SCRIPTPATH)
KSENV="${KLIPPERSCREEN_VENV:-${HOME}/.KlipperScreen-env}"

source ${KSENV}/bin/activate
pip --disable-pip-version-check install -r ${KSPATH}/scripts/KlipperScreen-requirements.txt

if [ $? -gt 0 ]; then
    echo "Unable to install dependencies, aborting install."
    deactivate
    exit 1
fi
deactivate
echo "Dependencies installed successfully."
exit 0
