#!/usr/bin/env bash

set -euo pipefail

readonly path_repo="$(dirname "$(dirname "$(realpath "$BASH_SOURCE")")")"
source "$path_repo/libs/nimbro_config/config.sh"

is_found_overlay_nimbro_config=""
is_found_overlay_nimbro_utils=""

show_help() {
    echo "Usage:"
    echo "  ./run.sh"
    echo
    echo "Run Docker container."
    echo
}

parse_args() {
    if [ "$#" -ne 0 ]; then
        show_help
        exit 1
    fi
}

check_overlays() {
    if [ -d "$PATH_NIMBRO_CONFIG" ]; then
        is_found_overlay_nimbro_config=0
    fi
    if [ -d "$PATH_NIMBRO_UTILS" ]; then
        is_found_overlay_nimbro_utils=0
    fi
}

run_docker() {
    local arch="$(arch)"
    local name_repo="$(basename "$path_repo")"

    docker run \
        --name "$NAME_CONTAINER_NIMBRO_DEPTHANYTHING" \
        --runtime nvidia \
        --shm-size 8G \
        --gpus all \
        --ipc host \
        --interactive \
        --tty \
        --net host \
        --rm \
        --env DISPLAY \
        --volume /etc/localtime:/etc/localtime:ro \
        --volume /tmp/.X11-unix/:/tmp/.X11-unix/:ro \
        --volume "$HOME/.Xauthority:/root/.Xauthority:ro" \
        --volume "$HOME/.ros/:/root/.ros/" \
        --volume "$path_repo:/root/colcon_ws/src/$name_repo" \
        ${is_found_overlay_nimbro_config:+--volume "$PATH_NIMBRO_CONFIG:/root/colcon_ws/src/$name_repo/libs/nimbro_config"} \
        ${is_found_overlay_nimbro_utils:+--volume "$PATH_NIMBRO_UTILS:/root/colcon_ws/src/nimbro_utils"} \
        "$NAME_CONTAINER_NIMBRO_DEPTHANYTHING:$arch" "$@"
    # --detach \
    # --restart unless-stopped \
}

main() {
    check_overlays
    run_docker "$@"
}

main "$@"
