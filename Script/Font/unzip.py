import os
import zipfile

path = os.path.join(os.getcwd(), 'AnsonFont-1.01.zip')

z = zipfile.ZipFile(path)

z.extractall()
