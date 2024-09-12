import argparse
from pathlib import Path

import tensorrt as trt

import nimbro_depthanything.config as config


def list_weights_available():
    paths_weights = sorted(Path(config._PATH_DIR_WEIGHTS).glob("*.pth"))
    names_weights_available = [f"{path_weights.parent.relative_to(paths_weights) / path_weights.stem}" for path_weights in paths_weights]

    return names_weights_available


def parse_args():
    names_weights_available = list_weights_available()

    parser = argparse.ArgumentParser(description="Export model.")
    parser.add_argument("--width", type=int, help="Width of input image", default=518)
    parser.add_argument("--height", type=int, help="Height of input image", default=518)
    parser.add_argument("--name_weights", help="Name of the saved weights", choices=names_weights_available, required=True)

    args = parser.parse_args()

    shape_image = (3, args.height, args.width)

    return shape_image, args.name_weights


logger = trt.Logger(trt.Logger.INFO)
builder = trt.Builder(logger)

network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))
parser = trt.OnnxParser(network, logger)

path_onnx = Path(".") / "onnx" / "depth_anything_v2_metric_hypersim_vits.onnx"
success = parser.parse_from_file(str(path_onnx))
for idx in range(parser.num_errors):
    print(parser.get_error(idx))

if not success:
    pass  # Error handling code here

config_builder = builder.create_builder_config()

if builder.platform_has_fast_fp16:
    config_builder.set_flag(trt.BuilderFlag.FP16)

# TODO: Limit memory so other things can also run?
# config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, 1 << 20) # 1 MiB

engine_serialized = builder.build_serialized_network(network, config_builder)
path_engine = Path(".") / "engines" / "depth_anything_v2_metric_hypersim_vits.engine"
with open(path_engine, "wb") as file_engine:
    file_engine.write(engine_serialized)
