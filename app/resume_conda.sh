#!/bin/bash
set -e
source /root/miniconda/etc/profile.d/conda.sh
conda activate trtllm
export TMPDIR=/root/pip-tmp
CURRENT_TORCH_VERSION=$(python -c "import torch; print(torch.__version__)")
echo "torch==$CURRENT_TORCH_VERSION" > /tmp/torch-constraint.txt
pip install tensorrt_llm -c /tmp/torch-constraint.txt --extra-index-url https://pypi.nvidia.com/ --no-cache-dir
