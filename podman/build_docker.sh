#!/bin/bash
# Build the timelapse container image

cd "$(dirname "$0")/.."

podman build -t make-timelapse -f podman/Dockerfile .
