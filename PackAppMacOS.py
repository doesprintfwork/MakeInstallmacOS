import os, shutil, plistlib, time, sys

line = "--------------------------------------------------"
folder = ""

def noline(string):
    print(string,end="")

def title(string):
    print(line)
    print("{:^50}".format(string))
    print(line)

def isfile(string):
    return os.path.isfile(string)

def clear():
    os.system("clear")

neededfiles = [r"../AppleDiagnostics.chunklist", r"../AppleDiagnostics.dmg", r"../BaseSystem.chunklist", r"../BaseSystem.dmg", r"../InstallESDDmg.pkg", r"../InstallInfo.plist"]

def copyfiles(sharedsupportloc):
    for f in neededfiles:
        noline("    Copying {}... ".format(f))

        shutil.copy(f, sharedsupportloc)
        print("Done.")

def editplist():
    fp = open(r"./InstallInfo.plist","rb")
    installinfo = plistlib.load(fp)
    del installinfo["Payload Image Info"]["chunklistURL"]
    del installinfo["Payload Image Info"]["chunklistid"]
    installinfo["Payload Image Info"]["URL"] = "InstallESD.dmg"
    installinfo["Payload Image Info"]["id"] = "com.apple.dmg.InstallESD"
    plistlib.dump(installinfo, open(r"./InstallInfo.plist", "wb"))

def packapp():

    clear()
    ### Here we choose our macOS Version
    title("Choose macOS Version")
    print("1: High Sierra")
    print("2: Mojave")
    print("Q: Quit")
    print("M: Main Menu")
    option = input("Please enter an option: ")
    version = ""
    diskname = ""
    if option == "1":
        version = "High Sierra"
        diskname = "'OS X Base System'"
    elif option == "2":
        version = "Mojave"
        diskname = "'macOS Base System'"
    elif option == "Q":
        quit()
    elif option == "M":
        mainmenu()
    else:
        packapp()

    clear()
    sharedsupportloc = r"./Install macOS {}.app/Contents/SharedSupport".format(version)

    title("Packing Files to Application")

    # We need to grab the base of the App out
    # from BaseSystem.dmg

    noline("Mounting BaseSystem.dmg... ")
    os.system("hdiutil attach ../BaseSystem.dmg > /dev/null")
    print("Done.")

    noline("Copying Installer from BaseSystem.dmg... ")
    os.system("cp -Rf /Volumes/{}/'Install macOS {}.app' ./'Install macOS {}.app'".format(diskname, version, version))
    print("Done.")

    noline("Unmounting BaseSystem.dmg... ")
    os.system("umount /Volumes/{}".format(diskname))
    print("Done.")

    # We need to make a folder call
    # SharedSupport inside the App.
    # This is where we save our files.

    noline("Making Directories... ")
    os.makedirs(sharedsupportloc)
    print("Done.")

    print("Copying Files...")
    copyfiles(sharedsupportloc)
    print("Done.")

    # We need to edit the InstallInfo.plist
    # to make sure we matches the settings
    # we want.

    noline("Editting InstallInfo.plist... ")
    os.chdir(sharedsupportloc)
    editplist()
    print("Done.")

    # We need to rename InstallESDDmg.pkg
    # to InstallESD.dmg to match the settings
    # in InstallInfo.plist

    noline("Renaming InstallESD.dmg... ")
    os.rename("InstallESDDmg.pkg", "InstallESD.dmg")
    print("Done.")

    print("All Done")
    time.sleep(1)

    mainmenu()
    

def SharedSupport():
    clear()

    title("Packing files to SharedSupport")

    noline("Making Directories... ")
    os.mkdir("SharedSupport")
    print("Done.")

    print("Copying files... ")
    copyfiles(r"./SharedSupport")
    print("Done.")

    noline("Editting InstallInfor.plist... ")
    os.chdir(r"./SharedSupport")
    editplist()
    os.rename("InstallESDDmg.pkg", "InstallESD.dmg")
    print("Done")

    print("All Done.")
    time.sleep(1)

    mainmenu()

def packimg():
    clear()

    title("Choose macOS Version")
    print("1: High Sierra")
    print("2: Mojave")
    print("Q: Quit")
    print("M: Main Menu")
    option = input("Please enter an option: ")
    version = ""
    diskname = ""
    if option == "1":
        version = "High Sierra"
        diskname = "OS X Base System"
    elif option == "2":
        version = "Mojave"
        diskname = "macOS Base System"
    elif option == "Q":
        quit()
    elif option == "M":
        mainmenu()
    else:
        SharedSupport()

    clear()

    title("Packing files to SharedSupport")

    noline("Making Directories... ")

    os.mkdir("SharedSupport")
    print("Done.")

    print("Copying files... ")

    copyfiles(r"./SharedSupport")
    print("Done.")

    noline("Editting InstallInfo.plist... ")

    os.chdir(r"./SharedSupport")
    editplist()
    os.rename("InstallESDDmg.pkg", "InstallESD.dmg")
    print("Done.")

    noline("Converting BaseSystem.dmg to have Read and Write Access... ")
    os.chdir(r"../")
    os.system("hdiutil convert -format UDRW -o ./BaseSystem.dmg ../BaseSystem.dmg")
    print("Done.")

    noline("Extend BaseSystem.dmg capacity... ")
    os.system("hdiutil resize -size 8192m ./BaseSystem.dmg")
    print("Done.")

    noline("Mounting BaseSystem.dmg... ")
    os.system("hdiutil attach ./BaseSystem.dmg")
    print("Done.")

    noline("Moving files in place... ")
    shutil.move(r"./SharedSupport", r"/Volumes/{}/Install macOS {}.app/Contents".format(diskname, version))
    print("Done.")


    print("All Done.")
    time.sleep(1)

    mainmenu()

def checkfiles():
    clear()
    title("Checking Required Files...")
    folder = input("Please drag and drop your download macOS folder here: ")
    os.chdir(folder)
    time.sleep(0.5)
    for f in neededfiles:
        if isfile(f) == False:
            print("Missing Files.")
            sys.exit()
    time.sleep(1)

def quit():
    print("Goodbye! Have a good day!")
    sys.exit()

def mainmenu():
    clear()
    title("Main Menu")
    print("A: Pack files to an Install macOS Application")
    print("B: Pack files to disk image (This will take a long time!)")
    print("P: Pack files for convert the current Network Recovery Installer to a Full Installer (SharedSupport)")
    print("Q: Quit")
    option = input("Enter an option: ")
    if option == "Q" or option == "q":
        quit()
    elif option == "A" or option == "a":
        os.chdir(folder)
        packapp()
    elif option == "B" or option == "b":
        os.chdir(folder)
        packimg()
    elif option == "P" or option == "p":
        os.chdir(folder)
        SharedSupport()
    else:
        mainmenu()

def main():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    checkfiles()
    mainmenu()

if __name__ == "__main__":
    main()
