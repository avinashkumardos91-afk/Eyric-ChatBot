#!/bin/bash
# =============================================================================
# NVIDIA TensorRT-LLM Setup Script
# =============================================================================
# This script installs TensorRT-LLM and its dependencies in WSL Ubuntu.
# Run with: bash nvidia_setup.sh
#
# Prerequisites:
#   - WSL2 with Ubuntu 26.04
#   - NVIDIA GPU with CUDA support (compute capability >= 7.0)
#   - NVIDIA drivers installed on Windows host
# =============================================================================

set -e  # Exit on error

echo "============================================="
echo "  NVIDIA TensorRT-LLM Installation Script"
echo "============================================="
echo ""

# -----------------------------------------------------------------------------
# Step 1: System Dependencies
# -----------------------------------------------------------------------------
echo "[Step 1/6] Installing system dependencies..."
sudo apt-get update -y
sudo apt-get install -y python3-pip python3-venv libopenmpi-dev libzmq3-dev
echo "[Step 1/6] ✅ System dependencies installed."
echo ""

# -----------------------------------------------------------------------------
# Step 2: Install PyTorch with CUDA 13.0
# -----------------------------------------------------------------------------
echo "[Step 2/6] Installing PyTorch with CUDA 13.0 support..."
pip3 install torch==2.11.0 torchvision --index-url https://download.pytorch.org/whl/cu130 --break-system-packages
echo "[Step 2/6] ✅ PyTorch with CUDA 13.0 installed."
echo ""

# -----------------------------------------------------------------------------
# Step 3: Uninstall conflicting CUTLASS packages
# -----------------------------------------------------------------------------
echo "[Step 3/6] Removing conflicting CUTLASS packages..."
pip3 uninstall -y nvidia-cutlass-dsl nvidia-cutlass-dsl-libs-base nvidia-cutlass-dsl-libs-cu13 2>/dev/null || true
echo "[Step 3/6] ✅ CUTLASS packages removed (or not present)."
echo ""

# -----------------------------------------------------------------------------
# Step 4: Install pip/setuptools/wheel and TensorRT-LLM
# -----------------------------------------------------------------------------
echo "[Step 4/6] Installing pip, setuptools, wheel..."
pip3 install --ignore-installed pip setuptools wheel --break-system-packages

echo "[Step 4/6] Creating torch version constraint..."
CURRENT_TORCH_VERSION=$(python3 -c "import torch; print(torch.__version__)")
echo "torch==${CURRENT_TORCH_VERSION}" > /tmp/torch-constraint.txt
echo "  Torch constraint: torch==${CURRENT_TORCH_VERSION}"

echo "[Step 4/6] Installing TensorRT-LLM with torch constraint..."
pip3 install tensorrt_llm -c /tmp/torch-constraint.txt --break-system-packages
echo "[Step 4/6] ✅ TensorRT-LLM installed."
echo ""

# -----------------------------------------------------------------------------
# Step 5: Verify installation
# -----------------------------------------------------------------------------
echo "[Step 5/6] Verifying installation..."
python3 -c "
import tensorrt_llm
print(f'  TensorRT-LLM version: {tensorrt_llm.__version__}')
import torch
print(f'  PyTorch version: {torch.__version__}')
print(f'  CUDA available: {torch.cuda.is_available()}')
if torch.cuda.is_available():
    print(f'  GPU: {torch.cuda.get_device_name(0)}')
    print(f'  CUDA version: {torch.version.cuda}')
"
echo "[Step 5/6] ✅ Verification complete."
echo ""

# -----------------------------------------------------------------------------
# Step 6: OpenMPI SLURM fix
# -----------------------------------------------------------------------------
echo "[Step 6/6] Setting OpenMPI environment variables..."
export PMIX_MCA_gds=hash
export OMPI_MCA_btl=^openib
echo "  PMIX_MCA_gds=hash"
echo "  OMPI_MCA_btl=^openib"
echo "[Step 6/6] ✅ OpenMPI configured."
echo ""

echo "============================================="
echo "  Installation Complete!"
echo "============================================="
echo ""
echo "To run the quickstart example:"
echo "  python3 app/quickstart_example.py"
echo ""
echo "To start the TensorRT-LLM server:"
echo "  trtllm-serve 'TinyLlama/TinyLlama-1.1B-Chat-v1.0'"
echo ""
echo "To query the server (from another terminal):"
echo "  curl -X POST http://localhost:8000/v1/chat/completions \\"
echo "    -H 'Content-Type: application/json' \\"
echo "    -d '{\"model\": \"TinyLlama/TinyLlama-1.1B-Chat-v1.0\","
echo "         \"messages\": [{\"role\": \"user\", \"content\": \"Hello!\"}],"
echo "         \"max_tokens\": 32}'"
echo ""
