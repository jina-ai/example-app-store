from jina import DocumentArrayMemmap
import os
from glob import glob

folder_name = "./workspace/indexer/0/index/"
# for dir in glob(f"{folder_name}/**"):
    # if os.path.isdir(dir):
        # print(dir)
        # try:
            # dam = DocumentArrayMemmap(folder_name)
            # print(dam)
            # print(len(dam))
        # except:
            # pass


dam = DocumentArrayMemmap(folder_name)
print(dam)
print(len(dam))
