#!/bin/bash
function install_service() {
    local SERVICE_DIR="$(dirname ${1})"
    local SERVICE_FILE="$(basename ${1})"
    local SYSTEMD_DIR=~/.config/systemd/user
    mkdir -p ${SYSTEMD_DIR}
    cp {${SERVICE_DIR},${SYSTEMD_DIR}}/${SERVICE_FILE}
    chmod 644 ${SYSTEMD_DIR}/${SERVICE_FILE}
    systemctl --user enable ${SERVICE_FILE}
    sudo systemctl daemon-reload
    systemctl --user start ${SERVICE_FILE}
}

if [ "$1" == "" ] || [ $# -gt 1 ]; then
    echo Usage: . install_service.sh [SERVICE_PATH]
else
    install_service ${1}
fi
