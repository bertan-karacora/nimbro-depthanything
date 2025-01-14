#!/usr/bin/env bash

set -euo pipefail

readonly path_repo="$(dirname "$(dirname "$(realpath "$BASH_SOURCE")")")"
source "$path_repo/libs/nimbro_config/config.sh"

use_clean=""
use_debug=""

show_help() {
    echo "Usage:"
    echo "  ./build.sh [--use_clean] [--use_debug]"
    echo
    echo "Build the Docker image."
    echo
}

parse_args() {
    local arg=""
    while [[ $# -gt 0 ]]; do
        arg="$1"
        shift
        case $arg in
        -h | --help)
            show_help
            exit 0
            ;;
        --use_clean)
            use_clean=0
            ;;
        --use_debug)
            use_debug=0
            ;;
        *)
            echo "Unknown option $arg"
            exit 1
            ;;
        esac
    done
}

build() {
    local arch="$(arch)"

    docker build \
        --build-arg=USERNAME_GITLAB \
        --build-arg=TOKEN_GITLAB \
        --tag="$NAME_CONTAINER_NIMBRO_DEPTHANYTHING:$arch" \
        --file="$path_repo/docker/Dockerfile" \
        ${use_clean:+--no-cache} \
        ${use_debug:+--progress=plain} \
        \
        "$path_repo" # --platform linux/arm64 \
}

main() {
    parse_args "$@"
    build
}

main "$@"
