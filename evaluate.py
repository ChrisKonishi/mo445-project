import argparse
import cv2
import numpy as np
import os
import sklearn.metrics as metrics

import iou


def main(label_dir, gt_dir, ori_img_dir):
    # Create a directory for saving visualizations if it doesn't exist
    iou_dir = "iou"
    bb_dir = "bb"
    if not os.path.exists(iou_dir):
        os.makedirs(iou_dir)
    if not os.path.exists(bb_dir):
        os.makedirs(bb_dir)
    # Get the list of mask images
    mask_images = get_mask_images(label_dir)
    # Get the list of ground truth images
    gt_images = os.listdir(gt_dir)
    # Get the list of original images
    original_images = os.listdir(ori_img_dir)

    # Sort the images to ensure that they are aligned

    gt_images = remove_gt_not_used(mask_images, gt_images)

    mask_images.sort()
    gt_images.sort()
    original_images.sort()

    acc_iou_seg = 0
    acc_dice_seg = 0
    acc_iou_bb = 0
    # Iterate over the images and calculate IoU
    for idx, (mask_image, gt_image, ori_img) in enumerate(
        zip(mask_images, gt_images, original_images)
    ):
        print("\nMask image: ", idx)
        # Get the path to mask and ground truth images
        mask_image_path = os.path.join(label_dir, mask_image)
        gt_image_path = os.path.join(gt_dir, gt_image)

        # Calculate IoU
        visualization, iou_seg_img = iou.visualize_intersection_union(
            gt_image_path, mask_image_path
        )
        # read images
        mask_image_pred = cv2.imread(mask_image_path, cv2.IMREAD_GRAYSCALE).flatten()
        mask_image_pred[mask_image_pred > 0] = 1
        gt_image = cv2.imread(gt_image_path, cv2.IMREAD_GRAYSCALE).flatten()
        gt_image[gt_image > 0] = 1
        # calculate dice
        dice = metrics.f1_score(
            gt_image, mask_image_pred, average="binary", zero_division=1
        )
        print(f"Dice: {dice}")
        acc_dice_seg += dice

        # Save the visualization in the 'iou' folder
        visualization_path = os.path.join(iou_dir, mask_image)
        cv2.imwrite(visualization_path, visualization)

        # Accumulate the IoU score
        acc_iou_seg += iou_seg_img

        # calculate bounding box
        gt_mask = cv2.imread(gt_image_path, cv2.IMREAD_GRAYSCALE)
        gt_mask[gt_mask > 0] = 1
        gt_bb = get_bb(gt_mask)
        pred_mask = cv2.imread(mask_image_path, cv2.IMREAD_GRAYSCALE)
        pred_bb = get_bb(pred_mask)
        iou_bb = bb_iou(gt_bb, pred_bb)
        print(f"IoU bb: {iou_bb}")
        acc_iou_bb += iou_bb

        # Draw bounding boxes
        img = cv2.imread(os.path.join(ori_img_dir, ori_img))
        cv2.rectangle(img, (gt_bb[0], gt_bb[1]), (gt_bb[2], gt_bb[3]), (0, 255, 0), 2)
        cv2.rectangle(
            img, (pred_bb[0], pred_bb[1]), (pred_bb[2], pred_bb[3]), (0, 0, 255), 2
        )
        cv2.imwrite(os.path.join(bb_dir, ori_img), img)

    iou_score_seg = acc_iou_seg / len(mask_images)
    dice_score_seg = acc_dice_seg / len(mask_images)
    iou_score_bb = acc_iou_bb / len(mask_images)
    print(f"Average IoU seg: {iou_score_seg}")
    print(f"Average Dice seg: {dice_score_seg}")
    print(f"Average IoU bb: {iou_score_bb}")


def get_mask_images(label_dir):
    # Get the list of mask images
    mask_images = [i for i in os.listdir(label_dir) if "modified" in i]
    # Sort the images to ensure that they are aligned
    mask_images.sort()
    if len(mask_images) == 0 and len(os.listdir(label_dir)) > 0:
        import mask_converter

        mask_converter.change_pixels_in_folder(label_dir)
        mask_images = [i for i in os.listdir(label_dir) if "modified" in i]

    return mask_images


def get_bb(mask: np.array):
    """
    Get bounding box of mask
    """
    if mask[mask > 0].size == 0:
        return (0, 0, 0, 0)
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    y_min, y_max = (
        np.where(rows)[0][[0, -1]] if rows[rows].size > 1 else np.where(rows)[0][[0, 0]]
    )
    x_min, x_max = (
        np.where(cols)[0][[0, -1]] if cols[cols].size > 1 else np.where(cols)[0][[0, 0]]
    )
    return (x_min, y_min, x_max, y_max)


def bb_iou(gt_bb, pred_bb):
    """
    Calculate IoU of bounding boxes
    """
    # determine the coordinates of the intersection rectangle

    x_left = max(gt_bb[0], pred_bb[0])
    y_top = max(gt_bb[1], pred_bb[1])
    x_right = min(gt_bb[2], pred_bb[2])
    y_bottom = min(gt_bb[3], pred_bb[3])

    if x_right < x_left or y_bottom < y_top:
        return 0.0

    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # compute the area of bbs
    gt_area = (gt_bb[2] - gt_bb[0]) * (gt_bb[3] - gt_bb[1])
    pred_area = (pred_bb[2] - pred_bb[0]) * (pred_bb[3] - pred_bb[1])
    union_area = gt_area + pred_area - intersection_area
    if union_area == 0:
        return 1.0

    iou = intersection_area / union_area
    return iou

def remove_gt_not_used(masked_images, gt_images):
    """
    Remove ground truth images that are not used
    """
    maks_ids = [i.split("_")[1] for i in masked_images]

    cleaned_gt_images = []
    for gt_image in gt_images:
        gt_id = gt_image.split(".")[0]
        if gt_id in maks_ids:
            cleaned_gt_images.append(gt_image)
    
    return cleaned_gt_images


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
    parser.add_argument(
        "--ori_img_dir",
        default="./images",
        type=str,
        help="Path to the original image directory",
    )
    args = parser.parse_args()
    main(args.label_dir, args.gt_dir, args.ori_img_dir)
