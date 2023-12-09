import os
import cv2

def main():
    img_dir = 'images'
    mask_dir = 'truelabels'
    out_dir = 'misc/bb_images'

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    
    for img_name in os.listdir(img_dir):
        img_path = os.path.join(img_dir, img_name)
        mask_path = os.path.join(mask_dir, img_name)
        img = cv2.imread(img_path)
        mask = cv2.imread(mask_path)
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
        out_path = os.path.join(out_dir, img_name)
        cv2.imwrite(out_path, img)
        


if __name__ == '__main__':
    main()