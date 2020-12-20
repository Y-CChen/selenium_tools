#!/bin/bash
function install_service() {
    local SERVICE_DIR="$(dirname ${1})"
    local SERVICE_FILE="$(basename ${1})"
    sudo cp {${SERVICE_DIR},/lib/systemd/system}/${SERVICE_FILE}
    sudo chmod 644 /lib/systemd/system/${SERVICE_FILE}
    sudo systemctl daemon-reload
}

if [ "$1" == "" ] || [ $# -gt 1 ]; then
    echo Usage: . install_service.sh [SERVICE_PATH]
else
    install_service ${1}
fi
