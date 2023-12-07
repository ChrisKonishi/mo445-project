import os
import sys
    
if (len(sys.argv) != 4):
    print("python exec <P1> <P2>")
    print("P1: number of layers (if negative, do not encode layers again)")
    print("P2: layer for the results")
    print("P3: model_type (0, 1, 2)")
    exit()

nlayers      = int(sys.argv[1])
target_layer = int(sys.argv[2])
model_type   = int(sys.argv[3])

os.system("./bin/preproc images 1.5 filtered")
npts_per_marker = 5
line = "./bin/bag_of_feature_points filtered markers {} bag".format(npts_per_marker)
os.system(line)

for layer in range(1,nlayers+1):
    line = "./bin/create_layer_model bag arch.json {} flim".format(layer)
    os.system(line)
    if (model_type == 0):
        line = "./bin/encode_layer arch.json {} flim".format(layer)
        os.system(line)
    else:
        line = "./bin/merge_layer_models arch.json {} flim".format(layer)
        os.system(line)
        line = "./bin/encode_merged_layer arch.json {} flim".format(layer)
        os.system(line)

line = "./bin/decode_layer {} arch.json flim {} salie".format(target_layer, model_type)
os.system(line)
line = "./bin/detection salie {} boxes".format(target_layer)
os.system(line)
line = "./bin/delineation salie {} objs".format(target_layer)
os.system(line)
        
