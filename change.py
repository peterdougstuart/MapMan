#https://forum.omz-software.com/topic/3744/xcode-template-for-pythonista/3

# Change these:
pylib_path1 = r'/Users/stuart/MapMan/PythonistaAppTemplate/PythonistaKit.framework/pylib'
pylib_path2 = r'/Users/stuart/MapMan/PythonistaAppTemplate/PythonistaKit.framework/pylib_ext'

import shutil
import os
import subprocess

def check_is_executable(file_path):
    file_output = subprocess.check_output(['file', file_path])
    if 'executable' in file_output:
        return True, file_output
    return False, file_output

def fix_executable(file_path):
    with open(file_path, 'r') as f:
        source = f.read()
    with open(file_path, 'w') as f:
        f.write('#\input texinfo\n' + source)
    is_executable, out = check_is_executable(file_path)
    return not is_executable

def fix_pylib(pylib_path, dry_run=False):
    print pylib_path
    for path, dirs, files in os.walk(pylib_path):
        for filename in files:
            full_path = full_path = os.path.join(path, filename)
            is_executable, file_output = check_is_executable(full_path)
            if is_executable:
                extension = os.path.splitext(full_path)[1].lower()
                if extension == '.py' or extension == '.pym' or filename == 'command_template':
                    if dry_run:
                        print '### Executable found: %s' % (filename,)
                    else:
                        print 'Fixing %s...' % (filename,)
                        fixed = fix_executable(full_path)
                        if not fixed:
                            print '### FIXING %s FAILED' % (full_path,)
                        else:
                            print 'Fixed'
                else:
                    print '### Executable found, but does not seem to be Python code: %s' % (full_path,)

if __name__ == '__main__':
    fix_pylib(pylib_path1)
    fix_pylib(pylib_path2)

