# UCH Notepad

A simple Ultimate Chicken Horse ruleset and custom level file editor written in Python. (Windows 64bit only at the moment)

**Important**: the program will not read uncompressed levels with the `.snapshot` extension. Change the extension to `.v` or `.c`

## TO-DO list

- Optimize code functionality and readability.
- Fix buttons not changing when the dark theme is enabled.
- Implement right-click menu in Text box.
- Implement Find and Replace functionality.
- Implement Drag and drop.
- Detect file formats with error handlers instead of file extension (Still considering this one, maybe i will leave it like that).
- macOS and Linux version.
- 32 bit version for all OSes.
- Updater

## Installation and Usage instructions

- Unzip the downloaded file in any folder.
- Run uchnotepad.exe inside the extracted folder.
- Use "Open Level" to edit a custom level file, or "Open ruleset" to edit a custom ruleset file.

## Features

- Automatic XML "beautifier".
- 25 undos and redos (Might increase it if needed).
- Level thumbnail displayer.

## FAQ
- Q: vcruntime140.dll is missing/The program is not opening.

  A: Download Visual C++ Redistributable for Visual Studio 2015 or 2017 here: https://aka.ms/vs/16/release/vc_redist.x64.exe
  
- Q: The program is only giving me the option to save as a **LZMA Encoded File** in the **Save As...** dialog.

  A: The file header is being recognized as an invalid UCH level/ruleset file format. Your file should start with `<scene` or `<Ruleset`.
  
- Q: The program is not opening my file.

  A: Make sure the file is formatted as a XML. If it is formatted as an XML and still it is not being opened, open an **Issue** showing your file.
