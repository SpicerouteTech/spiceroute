#!/bin/bash

# Installation Monitoring Script
# Monitors installation processes and logs

LOG_DIR="./logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/install_monitor_$(date +%Y%m%d).log"

monitor_installation() {
    while true; do
        echo "=== Installation Status Report - $(date) ===" >> "$LOG_FILE"
        echo "=== Docker Status ===" >> "$LOG_FILE"
        docker info >> "$LOG_FILE" 2>&1
        echo "=== Kubernetes Status ===" >> "$LOG_FILE"
        kubectl get nodes >> "$LOG_FILE" 2>&1
        echo "=== Running Containers ===" >> "$LOG_FILE"
        docker ps >> "$LOG_FILE" 2>&1
        echo "=== System Resources ===" >> "$LOG_FILE"
        top -l 1 | head -n 10 >> "$LOG_FILE"
        echo "=====================================" >> "$LOG_FILE"
        sleep 60
    done
}

# Start monitoring in the background
monitor_installation &
MONITOR_PID=$!

# Cleanup function
cleanup() {
    echo "Stopping installation monitor..."
    kill $MONITOR_PID
    exit 0
}

# Trap SIGINT and SIGTERM
trap cleanup SIGINT SIGTERM

# Keep the script running
wait 