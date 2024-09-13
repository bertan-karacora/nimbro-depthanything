#!/usr/bin/env bash

set -eo pipefail

readonly path_repo="$(dirname "$(dirname "$(realpath "$BASH_SOURCE")")")"
source "$path_repo/libs/nimbro_config/config.sh"

source "/opt/ros/$DISTRIBUTION_ROS/setup.bash"
source "$HOME/colcon_ws/install/setup.bash"

set -u

main() {
    "$path_repo/libs/nimbro_config/scripts/setup_rmw.sh"

    "$path_repo/scripts/download_weights_pretrained.sh" "$path_repo/resources/weights"
    # "$path_repo/scripts/download_data.sh" "$path_repo/resources/data"

    # python "$path_repo/nimbro_depthanything/scripts/export_model.py" --weights "depth_anything_v2_metric_hypersim_vits" --height 518 --width 686
    # python "$path_repo/nimbro_depthanything/scripts/build_engine.py" --model "depth_anything_v2_metric_hypersim_vits"

    jupyter notebook --no-browser --port 8999 --allow-root
}

main "$@"
