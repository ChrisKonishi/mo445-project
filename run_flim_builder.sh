#!/bin/bash

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
cd $SCRIPT_DIR/libmo445/demo/Qt/FLIMbuilder/FLIMbuilder
LD_LIBRARY_PATH=~/Qt/6.3.2/gcc_64/lib ./FLIMbuilder
