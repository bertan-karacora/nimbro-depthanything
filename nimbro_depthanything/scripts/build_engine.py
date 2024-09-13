import argparse
from pathlib import Path

import tensorrt as trt

import nimbro_depthanything.config as config

_LOGGER_TRT = trt.Logger(trt.Logger.INFO)


def list_models_available():
    path_dir_models_onnx = Path(config._PATH_DIR_ONNX)
    paths_models_onnx = sorted(path_dir_models_onnx.glob("*.onnx"))
    names_models_onnx_available = [str(path_model.parent.relative_to(path_dir_models_onnx) / path_model.stem) for path_model in paths_models_onnx]

    return names_models_onnx_available


def parse_args():
    names_models_onnx_available = list_models_available()

    parser = argparse.ArgumentParser(description="Build tensorrt engine.")
    parser.add_argument("--model", dest="name_model", help="Name of the saved ONNX model", choices=names_models_onnx_available, required=True)
    parser.add_argument("--width", dest="width_input", help="Width of input image", type=int, default=518)
    parser.add_argument("--height", dest="height_input", help="Height of input image", type=int, default=518)

    args = parser.parse_args()

    shape_input = (1, 3, args.height_input, args.width_input)

    return args.name_model, shape_input


def build_engine(name_model, shape_input=(1, 3, 518, 518)):
    print(f"Building tensorrt engine ...")

    path_onnx = Path(config._PATH_DIR_ONNX) / f"{name_model}.onnx"

    builder = trt.Builder(_LOGGER_TRT)

    definition_network = builder.create_network(1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH))

    parser = trt.OnnxParser(definition_network, _LOGGER_TRT)

    success = parser.parse_from_file(str(path_onnx))
    for i in range(parser.num_errors):
        print(parser.get_error(i))
    if not success:
        print(f"Error: Could not parse ONNX model")
        return

    config_builder = builder.create_builder_config()
    if builder.platform_has_fast_fp16:
        config_builder.set_flag(trt.BuilderFlag.FP16)

    # profile_optimization = builder.create_optimization_profile()
    # profile_optimization.set_shape("input", (1, 3, 518, 518), shape_input, (1, 3, 518 * 4, 518 * 4))
    # config_builder.add_optimization_profile(profile_optimization)

    engine_serialized = builder.build_serialized_network(definition_network, config_builder)

    path_engine = Path(config._PATH_DIR_ENGINES) / f"{name_model}.engine"
    path_engine.parent.mkdir(parents=True, exist_ok=True)
    with open(path_engine, "wb") as file_engine:
        file_engine.write(engine_serialized)

    print(f"Engine saved to {path_engine}")


def main():
    name_model, shape_input = parse_args()
    build_engine(name_model, shape_input)


if __name__ == "__main__":
    main()
