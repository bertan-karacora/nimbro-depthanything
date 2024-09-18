FROM amd64/ros:humble-perception AS base-amd64



# ========================================
FROM arm64v8/ros:humble-perception AS base-arm64



# ========================================
FROM "base-$TARGETARCH" AS base

ARG DEBIAN_FRONTEND=noninteractive
ENV DEBCONF_NOWARNINGS="yes"

SHELL ["/bin/bash", "-c"]

# Install apt-utils
RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends \
    apt-utils \
    && \
    apt-get autoremove -y -qq && \
    apt-get clean -qq && \
    rm -rf /var/lib/apt/lists/*

# Install essentials
RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends \
    build-essential \
    ca-certificates \
    curl \
    git \
    lsb-release \
    nano \
    software-properties-common \
    tmux \
    unzip \
    wget \
    && \
    apt-get autoremove -y -qq && \
    apt-get clean -qq && \
    rm -rf /var/lib/apt/lists/*



# ========================================
FROM base AS system-amd64

ENV NVIDIA_VISIBLE_DEVICES=all \
    NVIDIA_DRIVER_CAPABILITIES=all

# Install cuda
RUN wget --quiet "https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.1-1_all.deb" --directory-prefix /tmp/ && \
    dpkg -i /tmp/cuda-keyring_1.1-1_all.deb && \
    rm -rf /tmp/*
RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends \
    cuda-toolkit-12-4 \
    && \
    apt-get autoremove -y -qq && \
    apt-get clean -qq && \
    rm -rf /var/lib/apt/lists/*
ENV PATH="/usr/local/cuda/bin:$PATH"
RUN ldconfig

# Install cudnn
RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends \
    cudnn9-cuda-12  \
    && \
    apt-get autoremove -y -qq && \
    apt-get clean -qq && \
    rm -rf /var/lib/apt/lists/*

# Install tensorrt
RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends \
    tensorrt \
    && \
    apt-get autoremove -y -qq && \
    apt-get clean -qq && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies
RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends \
    gettext-base \
    ros-humble-rmw-cyclonedds-cpp \
    && \
    apt-get autoremove -y -qq && \
    apt-get clean -qq && \
    rm -rf /var/lib/apt/lists/*



# ========================================
FROM base AS system-arm64

ENV NVIDIA_VISIBLE_DEVICES=all \
    NVIDIA_DRIVER_CAPABILITIES=all

# Install cuda
# Note: Installer for Ubuntu 24.04 not available for arm64
# Using Ubuntu 22.04 repos instead
RUN wget --quiet "https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/arm64/cuda-keyring_1.1-1_all.deb" --directory-prefix /tmp/ && \
    dpkg -i /tmp/cuda-keyring_1.1-1_all.deb && \
    rm -rf /tmp/*
RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends \
    cuda-toolkit-12-4 \
    && \
    apt-get autoremove -y -qq && \
    apt-get clean -qq && \
    rm -rf /var/lib/apt/lists/*
ENV PATH="/usr/local/cuda/bin:$PATH"
RUN ldconfig

# Install cudnn
RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends \
    cudnn9-cuda-12  \
    && \
    apt-get autoremove -y -qq && \
    apt-get clean -qq && \
    rm -rf /var/lib/apt/lists/*

# Install tensorrt
# Assume Jetson device
# Full installer only available for amd64
RUN wget --quiet https://developer.nvidia.com/downloads/compute/machine-learning/tensorrt/10.0.1/tars/TensorRT-10.0.1.6.l4t.aarch64-gnu.cuda-12.4.tar.gz --output-document /tmp/TensorRT.tar
RUN tar -xvf /tmp/TensorRT.tar --directory /usr/src && \
    mv /usr/src/TensorRT-* /usr/src/tensorrt && \
    cp -r /usr/src/tensorrt/lib/* "/usr/lib/$(uname -m)-linux-gnu/" && \
    cp -r /usr/src/tensorrt/include/* "/usr/include/$(uname -m)-linux-gnu/" && \
    rm -rf /tmp/*

# Install dependencies
RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends \
    gettext-base \
    ros-humble-rmw-cyclonedds-cpp \
    && \
    apt-get autoremove -y -qq && \
    apt-get clean -qq && \
    rm -rf /var/lib/apt/lists/*



# ========================================
FROM "system-$TARGETARCH" AS python-base

# Install python
RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends \
    python-is-python3 \
    python3 \
    python3-pip \
    python3-venv \
    && \
    apt-get autoremove -y -qq && \
    apt-get clean -qq && \
    rm -rf /var/lib/apt/lists/*

# Install python version explicitly
# Use python 3.10 since pytorch wheel is only avaiable for this version (and actually ubuntu 22.04)
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends \
    python3.10 \
    python3.10-venv \
    && \
    apt-get autoremove -y -qq && \
    apt-get clean -qq && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    PYTHONWARNINGS=ignore:::setuptools.command.install,ignore:::setuptools.command.easy_install,ignore:::setuptools.command.develop,ignore:::setuptools.dist,ignore:::pkg_resources \
    PIP_ROOT_USER_ACTION=ignore \
    PIP_DISABLE_PIP_VERSION_CHECK=on

# Setup venv
RUN python3.10 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONPATH="/opt/venv/lib/python3.10/site-packages:$PYTHONPATH"
RUN pip install --no-cache-dir \
    pip==24.2 \
    setuptools==74.0.0 \
    wheel==0.44.0



# ========================================
FROM python-base AS python-amd64

# Install dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --requirement /tmp/requirements.txt && \
    rm -rf /tmp/*



# ========================================
FROM python-base AS python-arm64-torch_tensorrt-build

# Install dependencies
COPY requirements.txt /tmp/requirements.txt
RUN grep -ivE "accelerate==|tensorrt==|torch==|torch-tensorrt==|torchaudio==|torchprofile==|torchvision==" /tmp/requirements.txt > /tmp/requirements_arm.txt
RUN pip install --no-cache-dir --requirement /tmp/requirements_arm.txt && \
    rm -rf /tmp/*

# Install dependencies for pytorch wheel
RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends \
    libopenblas-dev \
    libopenmpi-dev \
    libomp-dev \
    && \
    apt-get autoremove -y -qq && \
    apt-get clean -qq && \
    rm -rf /var/lib/apt/lists/*

# Assume Jetson device
# Check updates here: https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048
RUN wget --quiet https://nvidia.box.com/shared/static/zvultzsmd4iuheykxy17s4l2n91ylpl8.whl --output-document /tmp/torch-2.3.0-cp310-cp310-linux_aarch64.whl && \
    wget --quiet https://nvidia.box.com/shared/static/u0ziu01c0kyji4zz3gxam79181nebylf.whl --output-document /tmp/torchvision-0.18.0a0+6043bc2-cp310-cp310-linux_aarch64.whl && \
    wget --quiet https://nvidia.box.com/shared/static/9si945yrzesspmg9up4ys380lqxjylc3.whl --output-document /tmp/torchaudio-2.3.0+952ea74-cp310-cp310-linux_aarch64.whl

RUN pip install --no-cache-dir \
    /tmp/torch-2.3.0-cp310-cp310-linux_aarch64.whl \
    /tmp/torchvision-0.18.0a0+6043bc2-cp310-cp310-linux_aarch64.whl \
    /tmp/torchaudio-2.3.0+952ea74-cp310-cp310-linux_aarch64.whl \
    && \
    rm -rf /tmp/*

# Install tensorrt
RUN pip install --no-cache-dir \
    /usr/src/tensorrt/python/tensorrt-*-cp310-*.whl

# Install bazel
RUN BAZELISK_RELEASE=$(wget -qO- https://api.github.com/repos/bazelbuild/bazelisk/releases/latest | grep -Po '"tag_name": "\K.*?(?=")') && \
    BAZELISK_URL="https://github.com/bazelbuild/bazelisk/releases/download/$BAZELISK_RELEASE/bazelisk-linux-arm64" && \
    echo "BAZELISK_RELEASE=$BAZELISK_RELEASE" && echo "BAZELISK_URL=$BAZELISK_URL" && \
    wget --quiet --show-progress --progress=bar:force:noscroll --no-check-certificate $BAZELISK_URL -O /usr/local/bin/bazel && \
    chmod +x /usr/local/bin/bazel

RUN git clone --branch=v2.3.0 https://github.com/pytorch/TensorRT /opt/torch_tensorrt
COPY resources/WORKSPACE.jp60 /opt/torch_tensorrt/toolchains/jp_workspaces/WORKSPACE.jp60
COPY resources/WORKSPACE.jp60 /opt/torch_tensorrt/WORKSPACE
COPY resources/torch_tensorrt.diff /opt/torch_tensorrt 
RUN cd /opt/torch_tensorrt && \
    python setup.py bdist_wheel --jetpack-version 6.0 --use-cxx11-abi && \
    cp dist/torch_tensorrt*.whl /opt/



# ========================================
FROM python-base AS python-arm64

# Install dependencies
COPY requirements.txt /tmp/requirements.txt
RUN grep -ivE "accelerate==|tensorrt==|torch==|torch-tensorrt==|torchaudio==|torchprofile==|torchvision==" /tmp/requirements.txt > /tmp/requirements_arm.txt
RUN pip install --no-cache-dir --requirement /tmp/requirements_arm.txt && \
    rm -rf /tmp/*

# Install dependencies for pytorch wheel
RUN apt-get update -qq && \
    apt-get install -y -qq --no-install-recommends \
    libopenblas-dev \
    libopenmpi-dev \
    libomp-dev \
    && \
    apt-get autoremove -y -qq && \
    apt-get clean -qq && \
    rm -rf /var/lib/apt/lists/*

# Assume Jetson device
# Check updates here: https://forums.developer.nvidia.com/t/pytorch-for-jetson/72048
RUN wget --quiet https://nvidia.box.com/shared/static/zvultzsmd4iuheykxy17s4l2n91ylpl8.whl --output-document /tmp/torch-2.3.0-cp310-cp310-linux_aarch64.whl && \
    wget --quiet https://nvidia.box.com/shared/static/u0ziu01c0kyji4zz3gxam79181nebylf.whl --output-document /tmp/torchvision-0.18.0a0+6043bc2-cp310-cp310-linux_aarch64.whl && \
    wget --quiet https://nvidia.box.com/shared/static/9si945yrzesspmg9up4ys380lqxjylc3.whl --output-document /tmp/torchaudio-2.3.0+952ea74-cp310-cp310-linux_aarch64.whl

RUN pip install --no-cache-dir \
    /tmp/torch-2.3.0-cp310-cp310-linux_aarch64.whl \
    /tmp/torchvision-0.18.0a0+6043bc2-cp310-cp310-linux_aarch64.whl \
    /tmp/torchaudio-2.3.0+952ea74-cp310-cp310-linux_aarch64.whl \
    && \
    rm -rf /tmp/*

# Install tensorrt
RUN pip install --no-cache-dir \
    /usr/src/tensorrt/python/tensorrt-*-cp310-*.whl

# Install torch-tensorrt
COPY --from=python-arm64-torch_tensorrt-build /opt/torch_tensorrt*.whl /opt/
RUN pip install --no-cache-dir \
    /opt/torch_tensorrt*.whl \
    nvidia-modelopt[all]~=0.17.0 --extra-index-url https://pypi.nvidia.com



# ========================================
FROM "python-$TARGETARCH" AS depthanything

# Add code
ARG USERNAME_GITLAB \
    TOKEN_GITLAB
RUN git clone "https://$USERNAME_GITLAB:$TOKEN_GITLAB@git.ais.uni-bonn.de/athome/nimbro_utils.git" /root/colcon_ws/src/nimbro_utils
COPY . /root/colcon_ws/src/nimbro_depthanything

# Build
WORKDIR /root/colcon_ws
RUN source /opt/ros/humble/setup.bash && \
    colcon build --symlink-install
WORKDIR /root/colcon_ws/src/nimbro_depthanything

ENTRYPOINT []
CMD ["scripts/start_all.sh"]
