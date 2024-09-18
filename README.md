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

- Make model and engine working with dynamic shapes
- Make ros 2 jazzy container work
