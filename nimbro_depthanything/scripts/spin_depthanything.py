import nimbro_utils.node as utils_node

from nimbro_depthanything.node_depthanything import NodeDepthAnything


def main():
    utils_node.start_and_spin_node(NodeDepthAnything)


if __name__ == "__main__":
    main()
