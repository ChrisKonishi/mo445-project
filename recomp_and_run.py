import os

os.system("python3 clean_project.py")
os.system("bash ./compile.sh 1")
os.system("python3 exec.py 2 2 2")
os.system("python3 evaluate.py")