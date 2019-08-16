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

def editplist():
    pass

def packapp():

    title("Choose macOS Version")
    print("1: High Sierra")
    print("2: Mojave")
    print("Q: Quit")
    print("M: Main Menu")
    option = input("Please enter an option: ")
    version = ""
    if option == "1":
        version = "High Sierra"
    elif option == "2":
        version = "Mojave"
    elif version == "Q":
        quit()

    clear()

    title("Packing Files to Application")

    noline("Mounting BaseSystem.dmg... ")
    os.system("hdiutil attach ../BaseSystem.dmg")
    print("Done.")

    noline("Copying Installer from BaseSystem.dmg... ")
    shutil.copy(r"/Volumes/macOS Base System/Install macOS {}.app".format(version), r"./")
    print("Done.")

    noline("Making Directories... ")
    os.makedirs(r"./Install macOS {}.app/Contents/SharedSupport".format(version))
    print("Done.")

    print("Copying Files...")
    for f in neededfiles:
        noline("Copying {}... ".format(neededfiles))
        shutil.copy(f, r"./Install macOS {}.app/Contents/SharedSupport".format(version))
        print("Done.")
    print("Done.")

    print("Editting InstallInfo.plist")
    editplist()

def convert():
    pass

def checkfiles():
    clear()
    title("Checking Required Files...")
    time.sleep(0.5)
    for f in neededfiles:
        if isfile(f) == False:
            print("Missing Files.")
            sys.exit()

def quit():
    print("Goodbye! Have a good day!")
    sys.exit()

def mainmenu():
    clear()
    title("Main Menu")
    print("1: Pack files to an Install macOS Application")
    print("2: Convert Network Recovery macOS Installer USB to a Full Installer")
    print("Q: Quit")
    option = input("Enter an option: ")
    if option == "Q" or option == "q":
        quit()
    elif option == "1":
        packapp()
    elif option == "2":
        convert()
    else:
        mainmenu()

def main():
    checkfiles()
    mainmenu()


main()