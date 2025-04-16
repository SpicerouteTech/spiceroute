#!/bin/bash

# System Monitoring Script
# Monitors system resources, disk usage, and processes

LOG_DIR="./logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/system_monitor_$(date +%Y%m%d).log"

monitor_system() {
    while true; do
        echo "=== System Status Report - $(date) ===" >> "$LOG_FILE"
        echo "=== CPU and Memory Usage ===" >> "$LOG_FILE"
        top -l 1 | head -n 10 >> "$LOG_FILE"
        echo "=== Disk Usage ===" >> "$LOG_FILE"
        df -h >> "$LOG_FILE"
        echo "=== Memory Usage ===" >> "$LOG_FILE"
        vm_stat >> "$LOG_FILE"
        echo "=== Network Connections ===" >> "$LOG_FILE"
        netstat -an | grep ESTABLISHED >> "$LOG_FILE"
        echo "=====================================" >> "$LOG_FILE"
        sleep 60
    done
}

# Start monitoring in the background
monitor_system &
MONITOR_PID=$!

# Cleanup function
cleanup() {
    echo "Stopping system monitor..."
    kill $MONITOR_PID
    exit 0
}

# Trap SIGINT and SIGTERM
trap cleanup SIGINT SIGTERM

# Keep the script running
wait 