import os
import shutil
# delete the folders bag, bb, boxes, filtered, flim, iou, label, layer0, layer1, objs, salie

folders_to_delete = ['bag', 'bb', 'boxes', 'filtered', 'flim', 'iou', 'label', 'layer0', 'layer1', 'layer2','objs', 'salie']


for folder in folders_to_delete:
    folder_path = './' + folder
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
        print(f"Deleted folder: {folder}")
    else:
        print(f"Folder {folder} does not exist")
