#!/bin/bash

set -e
set -x

cmd="mamba" # or conda

create mamba/conda environment
mamba create -n mo445 python==3.10

mamba install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia -y
mamba install matplotlib tqdm numpy tifffile monai torchmetrics jupyter medpy -y

pip install torch-summary
pip install torch-snippets
