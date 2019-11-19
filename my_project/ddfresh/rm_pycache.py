import os
import shutil
for root, dirs, files in os.walk(os.getcwd(), topdown=True):
    print(dirs)
    for dir in dirs:
        if dir == '__pycache__':
            shutil.rmtree(dir)
