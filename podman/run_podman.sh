#!/bin/bash
# Run the timelapse container
# Usage: ./run_podman.sh <target> <start_date> <end_date> [--bucket BUCKET] [--folder FOLDER]
#
# Example:
#   ./run_podman.sh 101 2021-01-01 2021-01-31
#   ./run_podman.sh 102 2021-01-01 2021-01-31 --bucket prod-bucket --folder camera/snapshots

cd "$(dirname "$0")/.."

# Create work directory if not exists
mkdir -p ./work

# Run with arguments (use with ENTRYPOINT)
# podman run --rm \
#     -v "$(pwd)/.aws:/root/.aws:ro" \
#     -v "$(pwd)/work:/app/work" \
#     make-timelapse "$@"

# Run interactive bash console
podman run -it --rm \
    -v "$(pwd)/.aws:/root/.aws:ro" \
    -v "$(pwd)/make_timelapse.py:/app/make_timelapse.py:ro" \
    -v "$(pwd)/work:/app/work" \
    make-timelapse
