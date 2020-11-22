# UCH Notepad

A simple Ultimate Chicken Horse ruleset and custom level file editor written in Python.

## TO-DO list

- Optimize code functionality and readability.
- Implement right-click menu in Text box.
- Detect file formats with error handlers instead of file extension.
- macOS and Linux version.
- 32 bit version for all OSes.

## Installation and Usage instructions

- Unzip the downloaded file in any folder.
- Run uchnotepad.exe inside the extracted folder.
- Use "Open Level" to edit a custom level file, or "Open ruleset" to edit a custom ruleset file.

## FAQ
- Q: The program is only giving me the option to save as a **LZMA Encoded File** in the **Save As...** dialog.

  A: The file header is being recognized as an invalid UCH level/ruleset file format. Your file should start with `<scene` or `<Ruleset`.
  
- Q: The program is not opening my file.

  A: Make sure the file is formatted as a XML. If it is formatted as an XML and still it is not being opened, open an **Issue** showing your file.
