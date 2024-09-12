#!/usr/bin/env bash

set -eo pipefail

readonly path_repo="$(dirname "$(dirname "$(realpath "$BASH_SOURCE")")")"
source "$path_repo/libs/nimbro_config/config.sh"

source "/opt/ros/$DISTRIBUTION_ROS/setup.bash"
source "$HOME/colcon_ws/install/setup.bash"

set -u

main() {
    "$path_repo/libs/nimbro_config/scripts/setup_rmw.sh"

    jupyter notebook --no-browser --port 8999 --allow-root

    # Stay alive
    exec "$@"
}

main "$@"
