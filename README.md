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

- In build engine script: Limit memory so other things can also run? config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, 1 << 20) # 1 MiB
- Engine: Add Dimension Constraint using IAssertionLayer?
