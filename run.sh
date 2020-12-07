#!/bin/bash
echo "Starting SuitBot..."
cd /home/pi/suitbot/ || exit
/usr/bin/screen -dmS suitbot /home/pi/suitbot/venv/bin/python3 /home/pi/suitbot/run.py
