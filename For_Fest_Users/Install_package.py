import subprocess

used_package = "fpdf2,numpy,opencv-python,opencv-contrib-python".split(',')

def Install_Package():
    for pack in used_package:
        try:
            subprocess.check_call(['pip', 'install', pack])
            print("Successfully installed", pack)
        except subprocess.CalledProcessError as e:
            print("Error installing", pack, e)

def Uninstall_Package():
    for pack in used_package:
        try:
            subprocess.check_call(['pip', 'uninstall', pack, '-y'])
            print("Successfully uninstalled", pack)
        except subprocess.CalledProcessError as e:
            print("Error uninstalling", pack, e)


