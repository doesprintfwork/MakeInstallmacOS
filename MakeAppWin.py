import os, shutil, plistlib

line = "--------------------------------------------------\n"

def tit(string):
    print(line)
    print(string)
    print(line)

def noline(string):
    print(string, end="")

def editinfoplist(location):
    fp = open(location,"wb")
    plist = plistlib.load(fp)
    ver = plist['Payload Image Info']['version']
    del plist['Payload Image Info']
    plist.update({
        'Payload Image Info': dict(
            URL = 'InstallESD.dmg',
            version = ver,
        )}
    )