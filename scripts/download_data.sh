#!/usr/bin/env bash

set -euo pipefail

readonly path_repo="$(dirname "$(dirname "$(realpath "$BASH_SOURCE")")")"
source "$path_repo/libs/nimbro_config/config.sh"

readonly urls=(
    # https://huggingface.co/depth-anything/Depth-Anything-V2-Small/resolve/main/depth_anything_v2_vits.pth
    # https://huggingface.co/depth-anything/Depth-Anything-V2-Base/resolve/main/depth_anything_v2_vitb.pth
    # https://huggingface.co/depth-anything/Depth-Anything-V2-Large/resolve/main/depth_anything_v2_vitl.pth
    https://huggingface.co/depth-anything/Depth-Anything-V2-Metric-Hypersim-Small/resolve/main/depth_anything_v2_metric_hypersim_vits.pth
    https://huggingface.co/depth-anything/Depth-Anything-V2-Metric-Hypersim-Base/resolve/main/depth_anything_v2_metric_hypersim_vitb.pth
    https://huggingface.co/depth-anything/Depth-Anything-V2-Metric-Hypersim-Large/resolve/main/depth_anything_v2_metric_hypersim_vitl.pth
    # https://huggingface.co/depth-anything/Depth-Anything-V2-Metric-VKITTI-Small/resolve/main/depth_anything_v2_metric_vkitti_vits.pth
    # https://huggingface.co/depth-anything/Depth-Anything-V2-Metric-VKITTI-Base/resolve/main/depth_anything_v2_metric_vkitti_vitb.pth
    # https://huggingface.co/depth-anything/Depth-Anything-V2-Metric-VKITTI-Large/resolve/main/depth_anything_v2_metric_vkitti_vitl.pth
)
path_dir_data=""

show_help() {
    echo "Usage:"
    echo "  ./download_data.sh <path_dir_data>"
    echo
    echo "Download training data to <path_dir_data>."
    echo
}

parse_args() {
    if [ "$#" -ne 1 ]; then
        show_help
        exit 1
    fi
    path_dir_data="$1"
}

download_data() {
    if [ ! -d "$path_dir_data" ]; then
        mkdir -p "$path_dir_data"
    fi

    for url in "${urls[@]}"; do
        local name_file="$(basename "$url")"
        local path="$path_dir_data/$name_file"

        if [ ! -f "$path" ]; then
            echo "Downloading $name_file to $path_dir_data ..."
            wget "$url" --directory-prefix "$path_dir_data" --quiet --show-progress
        else
            echo "$name_file already exists in $path_dir_data"
        fi
    done
}

main() {
    parse_args "$@"
    download_data
}

main "$@"
