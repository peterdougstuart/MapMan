import shutil
import os.path

path='../MapMan/ImagePrep/Original/MissMapMan/Walk Cycle'

path_new='imageprep/original/missmapman/Walk Cycle'

for file in os.listdir(path):
	shutil.copyfile(os.path.join(path, file), os.path.join(path_new, file))
