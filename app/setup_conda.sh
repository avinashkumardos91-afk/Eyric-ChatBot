#!/bin/bash
set -e

source $HOME/miniconda/etc/profile.d/conda.sh

echo "Creating pip-tmp dir on disk..."
mkdir -p /root/pip-tmp
export TMPDIR=/root/pip-tmp

echo "Activating conda environment with Python 3.10..."
conda activate trtllm

echo "Installing PyTorch..."
pip install torch==2.11.0 torchvision --index-url https://download.pytorch.org/whl/cu130 --no-cache-dir

echo "Generating torch constraint..."
CURRENT_TORCH_VERSION=$(python -c "import torch; print(torch.__version__)")
echo "torch==$CURRENT_TORCH_VERSION" > /tmp/torch-constraint.txt

echo "Installing TensorRT-LLM..."
pip install tensorrt_llm -c /tmp/torch-constraint.txt --extra-index-url https://pypi.nvidia.com/ --no-cache-dir

echo "Conda environment setup complete!"
