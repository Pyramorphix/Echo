import shutil
import os

def setup_output_dir(output_dir: str):

    # Removing all the contents of output_dir:

    if os.path.isdir(output_dir):
        for obj in os.listdir(output_dir):

            path = os.path.join(output_dir, obj)

            if os.path.isfile(path) or os.path.islink(path):
                os.unlink(path)

            elif os.path.isdir(path):
                shutil.rmtree(path)

    

    paths = [os.path.join(output_dir, dir) for dir in ["histograms", "word_clouds", "activity_plots"]]

    for path in paths:
        os.makedirs(path)
