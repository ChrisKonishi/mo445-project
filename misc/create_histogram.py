import cv2
import matplotlib.pyplot as plt
import numpy as np
import os, os.path as osp

MASK_DIR = "./truelabels"

# Increase font size
plt.rcParams.update({'font.size': 16})


def main():
    mask_files = os.listdir(MASK_DIR)
    mask_files = [osp.join(MASK_DIR, f) for f in mask_files]
    vals = []

    for m in mask_files:
        mask = cv2.imread(m, cv2.IMREAD_GRAYSCALE)
        nonzero_percentage = np.count_nonzero(mask) / mask.size
        if nonzero_percentage < 1e-4:
            continue
        vals.append(nonzero_percentage)

    plt.figure(figsize=(11, 5))
    plt.hist(vals, bins=20)
    plt.xlabel("Porcentagem de píxeis não nulos")
    plt.ylabel("Número de imagens")
    plt.tight_layout()
    plt.savefig("misc/histogram.pdf")


if __name__ == "__main__":
    main()
