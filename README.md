# nimbro_depthanything

## Links

- [Depth Anything V2](https://depth-anything-v2.github.io)

## Setup

```bash
git clone https://git.ais.uni-bonn.de/athome/nimbro_depthanything.git
cd nimbro_depthanything
git submodule update --init --remote --recursive
```

## Usage

```bash
cd nimbro_depthanything

Docker/build.sh --use_clean
Docker/run.sh
```

## TODO

- Compiler is mounted if runtime=nvidia is used. Get /usr/lib/aarch64-linux-gnu/nvidia/libnvdla_compiler.so at build time somehow.
- Make model and engine working with dynamic shapes
- Make ros 2 jazzy container work
- Write ros node
- Collect data from relevant sensors
