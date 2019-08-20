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
    os.system("cls")

def copyfiles(sharedsupportloc):
    for f in neededfiles:
        noline("    Copying {}... ".format(f))

        shutil.copy(f, sharedsupportloc)
        print("Done.")

def checkfiles():
    clear()
    title("Checking Required Files...")
    time.sleep(0.5)
    for f in neededfiles:
        if isfile(f) == False:
            print("Missing Files.")
            sys.exit()
    time.sleep(1)

neededfiles = [r"../AppleDiagnostics.chunklist", r"../AppleDiagnostics.dmg", r"../BaseSystem.chunklist", r"../BaseSystem.dmg", r"../InstallESDDmg.pkg", r"../InstallInfo.plist"]

def editplist():
    fp = open(r"./InstallInfo.plist","rb")
    installinfo = plistlib.load(fp)
    del installinfo["Payload Image Info"]["chunklistURL"]
    del installinfo["Payload Image Info"]["chunklistid"]
    installinfo["Payload Image Info"]["URL"] = "InstallESD.dmg"
    installinfo["Payload Image Info"]["id"] = "com.apple.dmg.InstallESD"
    plistlib.dump(installinfo, open(r"./InstallInfo.plist", "wb"))

def SharedSupport():
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
        diskname = "'OS X Base System'"
    elif option == "2":
        version = "Mojave"
        diskname = "'macOS Base System'"
    elif option == "Q":
        quit()
    elif option == "M":
        mainmenu()
    else:
        SharedSupport()
    title("Packing files to SharedSupport")

    noline("Making Directories... ")
    os.mkdir("SharedSupport")
    print("Done.")

    noline("Copying files... ")
    copyfiles(r"./SharedSupport")
    print("Done.")

    noline("Editting InstallInfo.plist... ")
    os.chdir(r"./SharedSupport")
    editplist()
    os.rename("InstallESDDmg.pkg", "InstallESD.dmg")
    print("Done.")

    print("Extracting files from BaseSystem.dmg...")
    os.chdir(r"../")
    l7z = input("Please Drag and Drop the 7zip.exe from your Program Files: ")
    os.system("{} x BaseSystem.dmg > NUL:".format(l7z))
    print("Done.")

    noline("Moving files in place... ")
    shutil.move(r"./SharedSupport", r"./{}/Install macOS {}.app/Contents".format(diskname, version))
    print("Done.")

    print("All Done.")
    time.sleep(1)

    mainmenu()

def mainmenu():
    clear()
    title("Main Menu")
    print("P: Pack files for creating a Full Installer")
    print("Q: Quit")
    option = input("Enter an option: ")
    if option == "Q" or option == "q":
        quit()
    elif option == "P" or option == "p":
        SharedSupport()
    else:
        mainmenu()

def main():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    checkfiles()
    mainmenu()

if __name__ == "__main__":
    main()