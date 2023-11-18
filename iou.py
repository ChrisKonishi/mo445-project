import cv2
import numpy as np
import os

def calculate_iou(gt, label):
    # Calculate the intersection and union
    intersection = np.logical_and(gt, label)
    union = np.logical_or(gt, label)

    iou_score = np.sum(intersection) / np.sum(union)

    return iou_score

def visualize_intersection_union(gt_image, label_image):
    # Read the images
    gt = cv2.imread(gt_image, cv2.IMREAD_GRAYSCALE)
    label = cv2.imread(label_image, cv2.IMREAD_GRAYSCALE)

    # Threshold the images to ensure binary masks
    _, gt = cv2.threshold(gt, 127, 255, cv2.THRESH_BINARY)
    _, label = cv2.threshold(label, 127, 255, cv2.THRESH_BINARY)

    # Calculate the IoU score
    iou = calculate_iou(gt, label)
    print(f'IoU: {iou}')

    # Calculate the intersection and union
    intersection = cv2.bitwise_and(gt, label)
    union = cv2.bitwise_or(gt, label)

    # Create images with intersection in red and union in green
    intersection_red = cv2.merge((intersection, np.zeros_like(intersection), np.zeros_like(intersection)))
    union_green = cv2.merge((np.zeros_like(union), union, np.zeros_like(union)))

    # Combine the images to visualize intersection in red and union in green
    result = cv2.addWeighted(intersection_red, 1, union_green, 1, 0)

    return result, iou

# Replace these paths with the paths to your ground truth and label images
ground_truth_path = 'truelabels/000001.png'
label_path = 'label/modified_000001_label.png'

# Create a directory for saving visualizations if it doesn't exist
iou_dir = 'iou'
if not os.path.exists(iou_dir):
    os.makedirs(iou_dir)

visualization, iou = visualize_intersection_union(ground_truth_path, label_path)

# Save the visualization in the 'iou' folder
visualization_path = os.path.join(iou_dir, 'iou_visualization.png')
cv2.imwrite(visualization_path, visualization)
