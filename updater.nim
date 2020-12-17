#Based on rockyourcode.com readme.md template tutorial
import httpClient, os, terminal, system, zip/zipfiles
from os import fileExists, dirExists, getCurrentDir, moveFile, removeFile, removeDir
from terminal import getch
from system import quit

{.passl: "-lz".}

var url = "https://github.com/GrimStride/UCH-Notepad/releases/download/1.2/uchnotepad-v1.2-win64.zip"
var check = fileExists("uchnotepad.exe")
var prev = dirExists("lib/urllib3")
var current = getCurrentDir()

proc downloadUpdate(link: string) =
  var client = newHttpClient()
  try:
    echo("Downloading update 1.2 ...")
    var file = open("uchnotepad-v1.2-win64.zip", fmWrite)
    defer: file.close()
    file.write(client.getContent(link))
    echo("Update downloaded succesfully")
  except IOError as err:
    echo("Error: " & err.msg)
    return
  echo("Backing up user preferences...")
  moveFile("config.json", "config.json1")
  removeDir("lib")
  echo("User preferences backed up")
  var z: ZipArchive
  if not z.open("uchnotepad-v1.2-win64.zip"):
    echo("Opening zip failed")
    quit(1)
  echo ("Extracting update files...")
  z.extractAll(current)
  echo("Extraction completed")
  echo("Restoring user preferences...")
  removeFile("config.json")
  moveFile("config.json1", "config.json")
  echo("User preferences restored")
  echo("Cleaning up...")
  z.close()
  removeFile("uchnotepad-v1.2-win64.zip")
  echo("DONE")
  echo("UCH Notepad has been updated to version 1.2 succesfully")

when isMainModule:
  echo("UCH Notepad Updater v0.5 by Grim Stride")
  if check == true:
    if prev == true:
      downloadUpdate(url)
    else:
      echo("UCH Notepad 1.2 or greater is already installed")
  else:
    echo("Error: UCH Notepad executable not found, please move this file to the folder containing UCH Notepad's executable")
  echo("Press any key to exit...")
  var c = getch()
  quit()