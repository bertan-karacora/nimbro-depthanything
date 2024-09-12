import argparse
from pathlib import Path

import torch

import nimbro_depthanything.config as config
from nimbro_depthanything.models import DepthAnythingV2


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


def export_model(name_weights, shape_image=(3, 518, 518)):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    path_weights = Path(config._PATH_DIR_WEIGHTS) / f"{name_weights}.pth"
    weights = torch.load(f"{path_weights}", map_location="cpu")

    model = DepthAnythingV2(**config.MODELS[name_weights])
    model.load_state_dict(weights)
    model = model.to(device).eval()

    # Provide an example input to the model. This is necessary for exporting to ONNX.
    input_dummy = torch.ones(shape_image, device=device)[None, ...]
    model(input_dummy)

    path_onnx = Path(config._PATH_DIR_ONNX) / f"{name_weights}.onnx"
    path_onnx.parent.mkdir(parents=True, exist_ok=True)
    # TODO: Check opset version
    torch.onnx.export(model, input_dummy, path_onnx, input_names=["input"], output_names=["output"])

    print(f"Model exported to {path_onnx}")


def main():
    shape_image, name_weights = parse_args()
    export_model(name_weights, shape_image)


if __name__ == "__main__":
    main()
