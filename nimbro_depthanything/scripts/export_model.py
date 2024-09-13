import argparse
from pathlib import Path

import torch

import nimbro_depthanything.config as config
from nimbro_depthanything.models import DepthAnythingV2


def list_weights_available():
    path_dir_weights = Path(config._PATH_DIR_WEIGHTS)
    paths_weights = sorted(path_dir_weights.glob("*.pth"))
    names_weights_available = [str(path_weights.parent.relative_to(path_dir_weights) / path_weights.stem) for path_weights in paths_weights]

    return names_weights_available


def parse_args():
    names_weights_available = list_weights_available()

    parser = argparse.ArgumentParser(description="Export model.")
    parser.add_argument("--weights", dest="name_weights", help="Name of the saved weights", choices=names_weights_available, required=True)
    parser.add_argument("--opset", dest="version_opset", help="Opset version", type=int)
    parser.add_argument("--width", dest="width_input", help="Width of input image after resizing if it is the shorter side", type=int, default=518)
    parser.add_argument("--height", dest="height_input", help="Height of input image after resizing if it is the shorter side", type=int, default=518)

    args = parser.parse_args()

    shape_input = (1, 3, args.height_input, args.width_input)

    return shape_input, args.name_weights, args.version_opset


def export_model(name_weights, shape_input=(1, 3, 518, 518), version_opset=None):
    print(f"Exporting model ...")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    path_weights = Path(config._PATH_DIR_WEIGHTS) / f"{name_weights}.pth"
    weights = torch.load(f"{path_weights}", map_location="cpu")

    model = DepthAnythingV2(**config.MODELS[name_weights]["kwargs"])
    model.load_state_dict(weights)
    model = model.to(device)
    model = model.eval()

    input_dummy = torch.rand(shape_input, device=device, dtype=torch.float32)

    path_onnx = Path(config._PATH_DIR_ONNX) / f"{name_weights}.onnx"
    path_onnx.parent.mkdir(parents=True, exist_ok=True)
    torch.onnx.export(
        model,
        input_dummy,
        path_onnx,
        opset_version=version_opset,
        export_params=True,
        input_names=["input"],
        output_names=["output"],
        # dynamic_axes={
        #     "input": {2: "height", 3: "width"},
        #     "output": {1: "height", 2: "width"},
        # },
    )
    # torch.onnx.dynamo_export(
    #     model,
    #     input_dummy,
    #     # export_options=torch.onnx.ExportOptions(dynamic_shapes=True),
    # ).save(str(path_onnx))

    print(f"Model exported to {path_onnx}")


def main():
    shape_input, name_weights, version_opset = parse_args()
    export_model(name_weights, shape_input, version_opset)


if __name__ == "__main__":
    main()
