from sys import platform
import os

def LinuxFolders():
    folder = '.OpenCouture'
    home = os.path.expanduser('~')
    try:
        os.makedirs(os.path.join(home, folder))
    except OSError:
        if not os.path.isdir(path):
            raise

#def WindowsFolders():
    # To be written # 


def main():
    if platform == "linux" or platform == "linux2":
        print "You are running Linux"
        LinuxFolders()
    elif platform == "win32": 
        print "You are running Windows"
    else:
        print "You are not running Linux or Windows"

if __name__ == '__main__':
    main()
