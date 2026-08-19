#!/bin/bash
set -e
source /root/miniconda/etc/profile.d/conda.sh

echo "Removing old broken conda env..."
conda remove -n trtllm --all -y || true

echo "Creating fresh conda env..."
conda create -n trtllm python=3.10 -y
conda activate trtllm

export TMPDIR=/root/pip-tmp
mkdir -p $TMPDIR

echo "Installing tensorrt_llm (which will pull compatible torch automatically)..."
pip install tensorrt_llm --extra-index-url https://pypi.nvidia.com/ --no-cache-dir

echo "Done!"
