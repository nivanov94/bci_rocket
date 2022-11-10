import os

orig_ui_file_path = 'main.ui'
ui_file_path = 'modules/ui_main.py'

# compile .ui file
cmd = 'pyuic5 ' + orig_ui_file_path + ' > ' + ui_file_path
os.system(cmd)

# compile .qrc file
cmd = 'pyrcc5 resources.qrc -o modules/resources_rc.py'
os.system(cmd)
print('Compiled resources (.qrc) file')

# change encoding to utf-8 and update resources path
f = open(ui_file_path, 'r')
content = f.read()
f.close()
content = content.replace('import resources_rc', 'from . resources_rc import *')
f = open(ui_file_path, 'w', encoding='utf-8')
f.write(content)
f.close()

print("Compiled UI (.ui) file")