import os, shutil, plistlib, time, sys

line = "--------------------------------------------------"

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
    os.system("hdiutil attach ../BaseSystem.dmg")
    print("Done.")

    noline("Copying Installer from BaseSystem.dmg... ")
    os.system("cp -rf /Volumes/{}/'Install macOS {}.app' ./'Install macOS {}.app'".format(diskname, version, version))
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

    # While there are some aliases laying around
    # in the installer, shutil.copy copies
    # the original files. So we need to delete
    # them and make them by our own.

    noline("Deleting Files... ")
    os.chdir(r"../Frameworks/OSInstallerSetup.framework")
    os.remove("OSInstallerSetup")
    shutil.rmtree("Resources")
    shutil.rmtree(r"Versions/Current")
    print("Done")

    noline("Creating Alias... ")
    os.chdir("Versions")
    os.system("ln -fs A Current")
    os.chdir("../")
    os.system("ln -s Versions/A/OSInstallerSetup")
    os.system("ln -s Versions/A/Resources")
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

    noline("Copying files... ")
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


def checkfiles():
    clear()
    title("Checking Required Files...")
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
    print("P: Pack files to a folder (SharedSupport)")
    print("Q: Quit")
    option = input("Enter an option: ")
    if option == "Q" or option == "q":
        quit()
    elif option == "A":
        packapp()
    elif option == "P":
        SharedSupport()
    else:
        mainmenu()

def main():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    checkfiles()
    mainmenu()

if __name__ == "__main__":
    main()