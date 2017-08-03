import os
import datetime
from shutil import copyfile

drop_box_folder = r"/Users/stuart/Dropbox/Apps/MapMan/MapMan"
xcode_folder = r"/Users/stuart/MapMan/Script"

file_name = 'in_app.py'
drop_box_path = os.path.join(drop_box_folder, file_name)
xcode_path = os.path.join(xcode_folder, file_name)
copyfile(xcode_path, drop_box_path)
print "in_app.py synced"

for file_name in os.listdir(drop_box_folder):

    if file_name.endswith(".py") or file_name.endswith(".png"): 
    	
    	drop_box_path = os.path.join(drop_box_folder, file_name)
        drop_box_last_modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(drop_box_path))

    	xcode_path = os.path.join(xcode_folder, file_name)

        if not os.path.isfile(xcode_path):
        	copy = True
        else:
        	xcode_last_modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(xcode_path))
        	if drop_box_last_modified_date > xcode_last_modified_date:
	        	copy = True
	        else:
	        	copy = False

        if copy:
        	print "Copying {0}".format(file_name)
        	copyfile(drop_box_path, xcode_path)
        else:
        	print "{0} is up to date".format(file_name)
