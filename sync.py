import dropbox
from datetime import datetime
import os, shutil, sys

# dropbox token 
TOKEN = "D-lBzrPi4vcAAAAAAAAAAWI8NdYcbuPnQHjzXVDRlzbyyOqrURDnhbWcExVAXYVT"

# game save data (Citra)
GAME = "pokemon_ultra_sun"
save_location = ""
save_location_win = r"C:\Users\LENOVO\AppData\Roaming\Citra\sdmc\Nintendo 3DS\00000000000000000000000000000000\00000000000000000000000000000000\title\00040000\001b5000\data\00000001"
save_location_android = "/sdcard/citra-emu/sdmc/Nintendo 3DS/00000000000000000000000000000000/00000000000000000000000000000000/title/00040000/001b5000/data/00000001"
filename = "main"


def connect_to_dropbox():
    try:
        dbx = dropbox.Dropbox(TOKEN)
        print("connect sucessfully")
    except Exception as e:
        print(str(e))
    return dbx


def list_files_in_folder(dbx):
    try:
        folder_path = "/path"
        files = dbx.files_list_folder(folder_path).entries
        print("------------Listing Files in Folder------------ ")

        for file in files:

            # listing
            print(file.name)

    except Exception as e:
        print(str(e))

def get_time():
    a = str(datetime.now())
    return a.replace(":", ".")

def backupAndUpload():
    dbx = connect_to_dropbox()
    # cloud backup
    try:
        dbx.files_copy_v2("/citra-emu/" + GAME + "/" + filename, "/citra-emu/" +
                          GAME + "/" + filename + '_' + get_time())
    except:
        print("backup not found")
    # upload 
    with open(save_location + '/' + filename, 'rb') as f:
        dbx.files_upload(f.read(), path="/citra-emu/" + GAME +
                         "/" + filename, mode=dropbox.files.WriteMode.overwrite)

def backupAndDownload():
    dbx = connect_to_dropbox()
    # local backup 
    if not os.path.exists(save_location + '/' + GAME + '-BACKUP'):
        os.makedirs(save_location + '/' + GAME + '-BACKUP')
    shutil.copyfile(save_location + '/' + filename, save_location + '/' + GAME + '-BACKUP/' + filename + '_' + get_time() )
    # download 
    with open(save_location + '/' + filename, "wb") as f:
        metadata, res = dbx.files_download(path=f"/citra-emu/" + GAME + "/" + filename)
        f.write(res.content)


if __name__ == '__main__':
    if (len(sys.argv) != 3):
        print("Invalid input, use -u[-d] game_name")
    else:
        if (hasattr(sys, 'getandroidapilevel')):
            save_location = save_location_android
            print("android platform detect")
        else:
            save_location = save_location_win
            print("other platfrom detect")
        print("save location: ", save_location)
        GAME = sys.argv[2]
        print("game name: ", GAME)
        if(sys.argv[1] == "-d"):
            backupAndDownload()
        elif (sys.argv[1] == "-u"):
            backupAndUpload()
        print("done")
