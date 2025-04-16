#!/bin/bash

# QEMU Status Check Script
# Checks QEMU installation and running status

check_qemu() {
    echo "=== QEMU Status Check - $(date) ==="
    
    # Check QEMU installation
    echo "=== QEMU Installation Status ==="
    if command -v qemu-system-x86_64 &> /dev/null; then
        echo "QEMU is installed:"
        qemu-system-x86_64 --version
    else
        echo "QEMU is not installed"
    fi

    # Check running QEMU processes
    echo -e "\n=== Running QEMU Processes ==="
    ps aux | grep -i qemu | grep -v grep

    # Check system resources
    echo -e "\n=== System Resources ==="
    top -l 1 | head -n 10

    # Check disk usage
    echo -e "\n=== Disk Usage ==="
    df -h /usr/local
}

# Run the check
check_qemu 