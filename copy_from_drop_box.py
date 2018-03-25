import os
import datetime
from shutil import copyfile

def include_file(file_name, allowed_extensions):

    for extension in allowed_extensions:
        if file_name.endswith(extension):
            return True

    return False

def sync_folder(drop_box_folder, xcode_folder, allowed_extensions=['.py', '.png', '.caf', '.txt'], sub_folder='', reverse=False):

    if len(sub_folder) > 0:
        source_folder = os.path.join(drop_box_folder, sub_folder)
        target_folder = os.path.join(xcode_folder, sub_folder)
    else:
        source_folder = drop_box_folder
        target_folder = xcode_folder

    if reverse:
        temp = target_folder
        target_folder = source_folder
        source_folder = temp

    for file_name in os.listdir(source_folder):

        if include_file(file_name, allowed_extensions): 
            
            drop_box_path = os.path.join(source_folder, file_name)
            drop_box_last_modified_date = datetime.datetime.fromtimestamp(os.path.getmtime(drop_box_path))

            xcode_path = os.path.join(target_folder, file_name)

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
                pass
                #print "{0} is up to date".format(file_name)

def sync_in_app(drop_box_folder, xcode_folder, in_app_from_drop_box=True):

    file_name = 'in_app.py'
    drop_box_path = os.path.join(drop_box_folder, file_name)
    xcode_path = os.path.join(xcode_folder, file_name)

    if in_app_from_drop_box:
        copyfile(drop_box_path, xcode_path)
    else:
        copyfile(xcode_path, drop_box_path)

    print "in_app.py synced"

drop_box_base_folder = r"/Users/stuart/Dropbox/Apps/MapMan2/MapMan"
xcode_base_folder = r"/Users/stuart/MapMan/Script"

#sync_in_app(drop_box_base_folder, xcode_base_folder)
sync_folder(drop_box_base_folder, xcode_base_folder)
sync_folder(drop_box_base_folder, xcode_base_folder, allowed_extensions=['.png'], sub_folder='Hearts')
sync_folder(drop_box_base_folder, xcode_base_folder, allowed_extensions=['.png'], sub_folder='Heart')
sync_folder(drop_box_base_folder, xcode_base_folder, allowed_extensions=['.png'], sub_folder='Vortex')
sync_folder(drop_box_base_folder, xcode_base_folder, allowed_extensions=['.png'], sub_folder='Effects')
sync_folder(drop_box_base_folder, xcode_base_folder, allowed_extensions=['.png'], sub_folder='Buttons')
sync_folder(drop_box_base_folder, xcode_base_folder, allowed_extensions=['.png'], sub_folder='Menu')
sync_folder(drop_box_base_folder, xcode_base_folder, allowed_extensions=['.png'], sub_folder='Checkpoint')
sync_folder(drop_box_base_folder, xcode_base_folder, allowed_extensions=['.png'], sub_folder='Gradients')
sync_folder(drop_box_base_folder, xcode_base_folder, allowed_extensions=['.caf'], sub_folder='GameMusic')
sync_folder(drop_box_base_folder, xcode_base_folder, allowed_extensions=['.caf'], sub_folder='SoundEffects')
sync_folder(drop_box_base_folder, xcode_base_folder, allowed_extensions=['.png'], sub_folder=os.path.join('Man', 'Death'))
sync_folder(drop_box_base_folder, xcode_base_folder, allowed_extensions=['.png'], sub_folder=os.path.join('Man', 'Frames'))
sync_folder(drop_box_base_folder, xcode_base_folder, allowed_extensions=['.png'], sub_folder=os.path.join('Man', 'Idle'))
sync_folder(drop_box_base_folder, xcode_base_folder, allowed_extensions=['.png'], sub_folder=os.path.join('Woman', 'Frames'))
sync_folder(drop_box_base_folder, xcode_base_folder, allowed_extensions=['.png'], sub_folder=os.path.join('Woman', 'Idle'))
sync_folder(drop_box_base_folder, xcode_base_folder, allowed_extensions=['.png'], sub_folder='Tiles')

print("Done")