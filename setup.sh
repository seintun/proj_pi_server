#!/bin/bash
#
# To Run, type ` . startup.sh ` or ` source startup.sh `
# Note the period^

python3 -m venv --system-site-packages venv 
source venv/bin/activate

# Install necessary Pi Camera packages for Raspberry Pi camera support
sudo apt update && sudo apt install -y \
	build-essential \
	cmake \
	g++ \
	libavformat-dev \
	libcairo2-dev \
	libcamera-dev \
	libcap-dev \
	libfreetype6-dev \
	libgif-dev \
	libjpeg-dev \
	libpango1.0-dev \
	libpng-dev \
	libportmidi-dev \
	libsdl1.2-dev \
	libsdl2-dev \
	libsdl2-image-dev \
	libsdl2-mixer-dev \
	libsdl2-ttf-dev \
	libsmbclient-dev \
	libsmpeg-dev \
	libswresample-dev \
	libswscale-dev \
	python3-libcamera \
	python3-picamera2 \
	python3-sip

# pip install -r requirements.txt
pip install -r requirements.txt --no-cache-dir 

