import shutil
import os


class FileOrganize:
    def fileOrganize(self, src_dir, dest_dir):
        # getting all the files in the source directory
        files = os.listdir(src_dir)
        shutil.copytree(src_dir, dest_dir)

        return True
