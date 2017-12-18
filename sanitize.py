#https://forum.omz-software.com/topic/3744/xcode-template-for-pythonista/3

# Change these:
pylib_path1 = r'/Users/stuart/MapMan/PythonistaAppTemplate/PythonistaKit.framework/pylib'
pylib_path2 = r'/Users/stuart/MapMan/PythonistaAppTemplate/PythonistaKit.framework/pylib_ext'

import os
import os.path

def sanitize(directory):

    for root, _, files in os.walk(directory):

        for f in files:

            if os.path.splitext(f)[1] == '.py':

                print f

                edited = False
                fullpath = os.path.join(root, f)
                with open(fullpath, 'r') as open_file:
                    contents = open_file.read()
                    if contents[:3] == "'''" or contents[:3] == '"""':
                        edited = True
                        contents = "#dummycomment\n" + contents
                        
                    if contents[:2] == '#!':
                        edited = True
                        contents = contents.splitlines(True)
                        contents[0] = '#dummycomment\n'
                        contents = ''.join(contents)

                if edited:
                    with open(fullpath, 'w') as open_file:
                        open_file.write(contents)
                

if __name__ == '__main__':
    sanitize(pylib_path1)
    sanitize(pylib_path2)

