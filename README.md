# UCH Notepad

A simple Ultimate Chicken Horse ruleset and custom level file editor written in Python. (Windows and Linux 64bit only at the moment)

**Important**: the program will not read uncompressed levels with the `.snapshot` extension. Change the extension to `.v` or `.c`

## TO-DO list

- Optimize code functionality and readability.
- Fix buttons not changing when the dark theme is enabled.
- Implement right-click menu in Text box.
- Implement Find and Replace functionality.
- Implement Drag and drop.
- Detect file formats with error handlers instead of file extension (Still considering this one, maybe i will leave it like that).
- macOS version.
- 32 bit version for all OSes.

## Installation and Usage instructions

- Go to the **Releases** section and download the binaries for your platform.
- Unzip the downloaded file in any folder.
  * **Windows:** Run uchnotepad.exe inside the extracted folder.
  * **Linux:** Open a terminal in the extracted folder and enter `./uchnotepad` to run the tool.
- Use "Open Level" to edit a custom level file, or "Open ruleset" to edit a custom ruleset file.
- Click the settings button in the lower right corner to modify the program settings.

If you want to get the latest unstable version:
- Download python from www.python.org
- Download the repository.
- Install the following modules with **pip**:
  * Pillow
  * pyglet
  * pywin32 (Windows-only)
- For unstable versions prior to [02f8a7a](https://github.com/GrimStride/UCH-Notepad/commit/02f8a7aa6328cbb402538ad81fdc12765e5aa058), the following modules are also required:
  * Beautifulsoup4
  * requests (For commits prior to [51bce7e](https://github.com/GrimStride/UCH-Notepad/commit/51bce7ee2e7e97fb3d8dbb271a737616e5122775))
- Run the **.py** script.

## Features

- Automatic XML "beautifier".
- Unlimited undos and redos.
- Level thumbnail displayer.

## FAQ
- Q: vcruntime140.dll is missing / The program is not opening.

  A: Download Visual C++ Redistributable for Visual Studio 2015 or 2017 here: https://aka.ms/vs/16/release/vc_redist.x64.exe
  
- Q: The program is only giving me the option to save as a **LZMA Encoded File** in the **Save As...** dialog.

  A: The file header is being recognized as an invalid UCH level/ruleset file format. Your file should start with `<scene` or `<Ruleset`.
  
- Q: The program is not opening my file.

  A: Make sure the file is formatted as a XML. If it is formatted as an XML and still it is not being opened, open an **Issue** showing your file.
