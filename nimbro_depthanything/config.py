MODELS = {
    "depth_anything_v2_metric_hypersim_vits": {
        "kwargs": {
            "encoder": "vits",
            "features": 64,
            "out_channels": [48, 96, 192, 384],
        },
    },
    "depth_anything_v2_metric_hypersim_vitb": {
        "kwargs": {
            "encoder": "vitb",
            "features": 128,
            "out_channels": [96, 192, 384, 768],
        },
    },
    "depth_anything_v2_metric_hypersim_vitl": {
        "kwargs": {
            "encoder": "vitl",
            "features": 256,
            "out_channels": [256, 512, 1024, 1024],
        },
    },
    "depth_anything_v2_metric_hypersim_vitg": {
        "kwargs": {
            "encoder": "vitg",
            "features": 384,
            "out_channels": [1536, 1536, 1536, 1536],
        },
    },
}
_PATH_DIR_WEIGHTS = "/root/colcon_ws/src/nimbro_depthanything/resources/weights/"
_PATH_DIR_ONNX = "/root/colcon_ws/src/nimbro_depthanything/resources/models_onnx/"
_PATH_DIR_ENGINES = "/root/colcon_ws/src/nimbro_depthanything/resources/engines/"
