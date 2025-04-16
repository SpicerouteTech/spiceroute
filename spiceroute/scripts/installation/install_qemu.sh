#!/bin/bash

# QEMU Installation Script
# Installs and verifies QEMU installation

LOG_DIR="./logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/qemu_install_$(date +%Y%m%d).log"

install_qemu() {
    echo "Starting QEMU installation..." | tee -a "$LOG_FILE"
    
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "Homebrew not found. Installing Homebrew..." | tee -a "$LOG_FILE"
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi

    # Install QEMU
    echo "Installing QEMU..." | tee -a "$LOG_FILE"
    brew install qemu >> "$LOG_FILE" 2>&1

    # Verify installation
    if command -v qemu-system-x86_64 &> /dev/null; then
        echo "QEMU installation successful!" | tee -a "$LOG_FILE"
        qemu-system-x86_64 --version | tee -a "$LOG_FILE"
    else
        echo "QEMU installation failed!" | tee -a "$LOG_FILE"
        exit 1
    fi
}

# Run installation
install_qemu

# Start monitoring script
./scripts/monitoring/install_monitor.sh & 