import os
import shutil

for root, dirs, files in os.walk('.'):
    for name in files:
        path1 = os.path.join(root, name)
        path1 = path1.replace('.\\', '')
        path2 = '../djangodemo/' + path1
        shutil.copy(path1, path2)
    break