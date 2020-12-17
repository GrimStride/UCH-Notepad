#Based on rockyourcode.com readme.md template tutorial
import httpClient, os, terminal, system, zip/zipfiles
from os import fileExists, getCurrentDir
from terminal import getch
from system import quit

{.passl: "-lz".}

var url = "https://github.com/GrimStride/UCH-Notepad/releases/download/1.2/uchnotepad-v1.2-win64.zip"
var check = fileExists("uchnotepad.exe")
var current = getCurrentDir()

proc downloadUpdate(link: string) =
  var client = newHttpClient()
  try:
    echo("Downloading update 1.2 ...")
    var file = open("uchnotepad-v1.2-win64.zip", fmWrite)
    defer: file.close()
    file.write(client.getContent(link))
    echo("Update downloaded succesfully.")
  except IOError as err:
    echo("Error: " & err.msg)
    return
  var z: ZipArchive
  if not z.open("uchnotepad-v1.2-win64.zip"):
    echo("Opening zip failed")
    quit(1)
  z.extractAll(current)

when isMainModule:
  echo("UCH Notepad Updater v0.2 by Grim Stride")
  if check == true:
    downloadUpdate(url)
  else:
    echo("Error: UCH Notepad executable not found, please move this file to the folder containing UCH Notepad's executable")
  echo("Press any key to exit...")
  var c = getch()
  quit()
