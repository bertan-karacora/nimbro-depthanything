MODELS = {
    "depth_anything_v2_metric_hypersim_vits": {"encoder": "vits", "features": 64, "out_channels": [48, 96, 192, 384]},
    "depth_anything_v2_metric_hypersim_vitb": {"encoder": "vitb", "features": 128, "out_channels": [96, 192, 384, 768]},
    "depth_anything_v2_metric_hypersim_vitl": {"encoder": "vitl", "features": 256, "out_channels": [256, 512, 1024, 1024]},
    "depth_anything_v2_metric_hypersim_vitg": {"encoder": "vitg", "features": 384, "out_channels": [1536, 1536, 1536, 1536]},
}
_PATH_DIR_WEIGHTS = "/root/colcon_ws/src/nimbro_depthanything/weights/"
_PATH_DIR_ONNX = "/root/colcon_ws/src/nimbro_depthanything/onnx/"
