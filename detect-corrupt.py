# to-do:
# - add option to run quicker and lighter tests (without doing the longest tests);
# - add option to further investigate files that fail on the first test;

# I wonder if there is a way to more accurately determine an image file integrity.
# A deep scan to detect signs of corruption in the binary data of the image file
# or something like that.

from PIL import Image
import shutil
import os
import psutil
from tkinter import Tk
from tkinter.filedialog import askdirectory

# using tkinter's fancy gui to get user input
mainWindow = Tk().withdraw()
rec_dir = askdirectory(title="Choose the dir to be analyzed") + "/"
unrec_dir = askdirectory(title="Choose the dir to place unrecoverable files") + "/"
to_further_investigate_dir = askdirectory(title="Choose the dir to place semi-corrupted files") + "/"

dir_tree = os.walk(rec_dir)
for dirpath, dirname, filename in dir_tree:
    for file in filename:
        print("\nCurrent file:", file)
        current_img = rec_dir+file  # path + file name

        # TEST - open()
        # On the first test, both working and non-working images can fail, so
        # either way, they're both going into a "to-further-investigate" folder.
        try:
            current_img_object = Image.open(current_img)
            print("File", file, "was successfully objectified")
        except OSError:
            print("The file", file, "could NOT be objectified, but may still work normally. "
            						"We gonna place it in a separate folder and continue.")
            current_img_object.close()
            shutil.move(current_img, to_further_investigate_dir)
            print("The file was successfuly moved.")
            continue

        # TEST - verify()
        try:
            print("Lets verify it for corruption or truncation.")
            current_img_object.verify()
            print("No errors here, but in rare cases, some broken files can pass unseen in this method, "
                  "lets try a few more things.")

        # if img fails the verification, move to the unrecoverable folder
        except OSError:
            print("Fail... moving to unrecoverable dir")
            try:
                shutil.move(current_img, unrec_dir)
                print("The file", file, "was successfully moved.")
                continue
            except:
                continue

        # TEST - show()
        try:
            current_img_object.show()
            print("Attribute show() worked")

        # if img can't be opened, move to the unrecoverable folder
        except OSError:
            print("Attribute show() did NOT work, moving to unrecoverable dir")
            try:
                shutil.move(current_img, unrec_dir)
                print("The file", file, "was successfully moved.")
                continue
            except:
                continue

        # TEST - load()
        try:
            print("Lets try one last thing. We gonna load() it now")
            current_img_object.load()
            print("Works! Well, if even load() works, its at least 95% clean, but remember that even a truncated "
                  "image can be partially decoded and .load()ed. Its very unlikely though.")

        # if img can't be loaded, move to the unrecoverable folder
        except OSError:
            print("Fail... moving to unrecoverable dir")
            try:
                shutil.move(current_img, unrec_dir)
                print("The file", file, "was successfully moved.")
                continue
            except:
                continue

        # closes the app used to open the img file
        proc_to_kill = "Microsoft.Photos.exe"  # When I wrote this, I was using windows 10 native img viewer
        for proc in psutil.process_iter():
            if proc.name() == proc_to_kill:
                proc.kill()
    break
