import argparse
import cv2
import os

import iou


def main(label_dir, gt_dir):
    # Create a directory for saving visualizations if it doesn't exist
    iou_dir = "iou"
    if not os.path.exists(iou_dir):
        os.makedirs(iou_dir)
    # Get the list of mask images
    mask_images = [i for i in os.listdir(label_dir) if "modified" in i]
    # Get the list of ground truth images
    gt_images = os.listdir(gt_dir)

    # Sort the images to ensure that they are aligned
    mask_images.sort()
    gt_images.sort()

    acc_iou = 0
    # Iterate over the images and calculate IoU
    for mask_image, gt_image in zip(mask_images, gt_images):
        # Get the path to mask and ground truth images
        mask_image_path = os.path.join(label_dir, mask_image)
        gt_image_path = os.path.join(gt_dir, gt_image)

        # Calculate IoU
        visualization, iou_score = iou.visualize_intersection_union(
            gt_image_path, mask_image_path
        )

        # Save the visualization in the 'iou' folder
        visualization_path = os.path.join(iou_dir, mask_image)
        cv2.imwrite(visualization_path, visualization)

        # Accumulate the IoU score
        acc_iou += iou_score
    iou_score = acc_iou / len(mask_images)
    print(f"Average IoU: {iou_score}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--label_dir", default="./label", type=str, help="Path to the label directory"
    )
    parser.add_argument(
        "--gt_dir",
        default="./truelabels",
        type=str,
        help="Path to the ground truth directory",
    )
    args = parser.parse_args()
    main(args.label_dir, args.gt_dir)
