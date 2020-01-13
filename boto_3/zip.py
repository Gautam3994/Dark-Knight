import os
from zipfile import ZipFile, ZIP_DEFLATED

path = "C:/Users/Gautam/PycharmProjects/cdk_examples/functions/first_big_project"
with ZipFile("Lambda.zip", "w", compression=ZIP_DEFLATED) as zip_file:
    os.chdir(path)
    for root, direc, files in os.walk(path):
        for file in files:
            zip_file.write(os.path.relpath(os.path.join(root, file), os.path.join(path, '.')))

