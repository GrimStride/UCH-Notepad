import iupp as iup
import strformat, lzma, os, strutils, encodings

# - - - - - Images - - - - -
proc loadf():PIhandle =
  let imgdata =
    [
    0'u8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 32, 0, 0, 0, 111, 0, 0, 0, 79, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 0, 0, 0, 239, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 128, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 128, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 48, 0, 0, 0, 160, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 128, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 64, 0, 0, 0, 128, 0, 0, 0, 128, 0, 0, 0, 144, 0, 0, 0, 255, 0, 0, 0, 159, 0, 0, 0, 223, 0, 0, 0, 208, 0, 0, 0, 128, 0, 0, 0, 128, 0, 0, 0, 128, 0, 0, 0, 128, 0, 0, 0, 128, 0, 0, 0, 128, 0, 0, 0, 128, 0, 0, 0, 64, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 144, 0, 0, 0, 240, 0, 0, 0, 208, 0, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 0, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 207, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 96, 0, 0, 0, 191, 0, 0, 0, 191, 0, 0, 0, 191, 0, 0, 0, 191, 0, 0, 0, 191, 0, 0, 0, 191, 0, 0, 0, 191, 0, 0, 0, 239, 0, 0, 0, 208, 0, 0, 0, 96, 0, 0, 0, 255, 0, 0, 0, 207, 0, 0, 0, 191, 0, 0, 0, 191, 0, 0, 0, 96, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 96, 0, 0, 0, 192, 0, 0, 0, 192, 0, 0, 0, 192, 0, 0, 0, 192, 0, 0, 0, 192, 0, 0, 0, 192, 0, 0, 0, 192, 0, 0, 0, 240, 0, 0, 0, 191, 0, 0, 0, 95, 0, 0, 0, 255, 0, 0, 0, 208, 0, 0, 0, 192, 0, 0, 0, 192, 0, 0, 0, 96, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 80, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 208, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 0, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 144, 0, 0, 0, 239, 0, 0, 0, 207, 0, 0, 0, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 64, 0, 0, 0, 127, 0, 0, 0, 127, 0, 0, 0, 143, 0, 0, 0, 255, 0, 0, 0, 176, 0, 0, 0, 224, 0, 0, 0, 207, 0, 0, 0, 127, 0, 0, 0, 127, 0, 0, 0, 127, 0, 0, 0, 127, 0, 0, 0, 127, 0, 0, 0, 127, 0, 0, 0, 127, 0, 0, 0, 64, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 128, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 32, 0, 0, 0, 160, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 128, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 16, 0, 0, 0, 240, 0, 0, 0, 255, 0, 0, 0, 255, 0, 0, 0, 128, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 32, 0, 0, 0, 112, 0, 0, 0, 80, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    ]

  let p_imgdata = cast[ptr cuchar](unsafeAddr(imgdata))
  var image = iup.imageRGBA(18, 18, p_imgdata)
  discard setHandle("Tecgraf", image)

  return image

#var xd = iup.setHandle("CONFI", iup.imageRGBA(48, 48, cast[ptr cuchar](unsafeAddr(confpic))))

# - - - - - File Handling - - - - -

proc prettyxml(xml: string): string = xml.replace("></", ">\n</").replace("><", ">\n <").replace(" />", "/>").strip(leading=false)

proc open_file(ih:PIhandle) =
  let mode = iup.getAttribute(ih, "TITLE")
  let filename = iup.fileDlg()
  iup.setAttribute(filename, "DIALOGTYPE", "OPEN")
  iup.setAttributeHandle(filename, "PARENTDIALOG", iup.getDialog(ih))
  if mode == "Open Level":
    iup.setAttribute(filename, "DIRECTORY", os.getHomeDir() & "AppData\\LocalLow\\Clever Endeavour Games\\Ultimate Chicken Horse\\snapshots")
  else:
    iup.setAttribute(filename, "DIRECTORY", os.getHomeDir() & "AppData\\LocalLow\\Clever Endeavour Games\\Ultimate Chicken Horse\\rules")
    #echo(os.getHomeDir() & "AppData\\LocalLow\\Clever Endeavor Games\\Ultimate Chicken Horse\\rules")
  #echo(iup.getAttribute(ih, "TITLE"))
  iup.popup(filename, IUP_CENTERPARENT, IUP_CENTERPARENT)
  if iup.getInt(filename, "STATUS") != -1:
    let filename1 = iup.getAttribute(filename, "VALUE")
    #var b = readFile($(filename1))
    #echo(getCurrentEncoding($(filename1)))
    #a.close()
    let fnd = iup.getDialogChild(ih, "TXT")
    iup.setAttribute(fnd, "VALUE", prettyxml(readFile(convert($(filename1), "UTF-8")).decompress))
    #echo(iup.getFloat(fnd, "DY"))
  iup.destroy(filename)
  #return iup.IUP_DEFAULT

proc save_file(ih:PIhandle) =
  let filename = iup.fileDlg()
  iup.setAttribute(filename, "DIALOGTYPE", "SAVE")
  iup.setAttributeHandle(filename, "PARENTDIALOG", iup.getDialog(ih))
  iup.popup(filename, IUP_CENTERPARENT, IUP_CENTERPARENT)
  iup.destroy(filename)

proc getline(ih:PIhandle, lin:int, col:int): int =
  let cln = iup.getDialogChild(ih, "STATUSBAR")
  #echo (fmt"Ln: {lin} Col: {col}")
  #echo(cln)
  iup.setfAttribute(cln, "TITLE", fmt"Ln: {lin} Col: {col}")
  let st = iup.getDialogChild(ih, "BAR")
  iup.refreshChildren(st)
  #let fnd = iup.getDialogChild(ih, "TXT")
  #echo(iup.getFloat(fnd, "DY"))
  return iup.IUP_DEFAULT


discard iup.open(nil, nil)
iup.imageLibOpen()
#iup.glControlsOpen()

var septp = iup.flatseparator(nil)
iup.setAttribute(septp, "ORIENTATION", "HORIZONTAL")
iup.setAttribute(septp, "STYLE", "LINE")
iup.setAttribute(septp, "BARSIZE", "1")
iup.setAttribute(septp, "COLOR", "#D7D7D7")

var btn_open = iup.button("Open Level", nil)
var btn_orul = iup.button("Open Ruleset", nil)
var btn_nsav = iup.button("Save", nil)
var btn_save = iup.button("Save As...", nil)

iup.setAttribute(btn_open, "PADDING", "0x1")
iup.setAttribute(btn_orul, "PADDING", "0x1")
iup.setAttribute(btn_nsav, "PADDING", "0x1")
iup.setAttribute(btn_save, "PADDING", "0x1")


iup.setCallback(btn_open, "ACTION", cast[ICallback](open_file))
iup.setCallback(btn_orul, "ACTION", cast[ICallback](open_file))
iup.setCallback(btn_save, "ACTION", cast[ICallback](save_file))

var sepmn = iup.flatseparator(nil)
iup.setAttribute(sepmn, "ORIENTATION", "VERTICAL")
iup.setAttribute(sepmn, "STYLE", "LINE")
iup.setAttribute(sepmn, "BARSIZE", "1")
iup.setAttribute(sepmn, "COLOR", "#D7D7D7")


var txt_edit = iup.multiline(nil)
#iup.setAttribute(txt_edit, "MULTILINE", "YES")
iup.setAttribute(txt_edit, "BORDER", "NO")
iup.setAttribute(txt_edit, "EXPAND", "YES")
iup.setAttribute(txt_edit, "FORMATTING", "YES")
iup.setAttribute(txt_edit, "CPADDING", "2x4")
iup.setAttribute(txt_edit, "FONT", "Courier New, 10")
iup.setCallback(txt_edit, "CARET_CB", cast[ICallback](getline))
iup.setAttribute(txt_edit, "NAME", "TXT")
#iup.setAttribute(txt_edit, "VISIBLELINES", "20")
#iup.setFloat(txt_edit, "LINEY", iup.getFloat(txt_edit, "DY"))
#iup.setFloat(txt_edit, "LINEY", 1.0)

var sepfr = iup.flatseparator(nil)
iup.setAttribute(sepfr, "ORIENTATION", "HORIZONTAL")
iup.setAttribute(sepfr, "STYLE", "LINE")
iup.setAttribute(sepfr, "BARSIZE", "1")
iup.setAttribute(sepfr, "COLOR", "#D7D7D7")

var fr_buttons = iup.vbox(btn_open, btn_orul, btn_nsav, btn_save, nil)
iup.setAttribute(fr_buttons, "NMARGIN", "6x6")
iup.setAttribute(fr_buttons, "NORMALIZESIZE", "HORIZONTAL")
iup.setAttribute(fr_buttons, "NGAP", "10")

var container = iup.hbox(fr_buttons, sepmn,txt_edit, nil)
#iup.setAttribute(container, "EXPANDCHILDREN", "YES")
#iup.setAttribute(container, "NORMALIZESIZE", "YES")
#iup.setAttribute(container, "EXPAND", "YES")
#iup.setAttribute(container, "SIZE", "800x800")

var info = iup.label(nil)
iup.setAttribute(info, "TITLE", " By Grim Stride")
iup.setAttribute(info, "EXPAND", "HORIZONTAL")
#iup.setAttribute(info, "PADDING", "0x3")

var cln = iup.label(nil)
iup.setAttribute(cln, "TITLE", "Ln: 1 Col: 1")
iup.setAttribute(cln, "PADDING", "6x0")
iup.setAttribute(cln, "NAME", "STATUSBAR")
iup.setAttribute(cln, "ALIGNMENT", "ARIGHT")
#echo (iup.getHandle(cln))

#var xd = iup.setHandle("CONFI", iup.imageRGBA(48, 48, cast[ptr cuchar](unsafeAddr(confpic))))

var conf = iup.button(nil, nil)
#iup.setAttribute(conf, "ACTION", nil)
#iup.setAttribute(conf, "IMAGE", "CONFI")
#iup.setAttribute(conf, "IMAGE", "C:\\nim-1.4.2\\scripts\\kk.bmp")
#iup.setAttributeHandle(conf, "IMAGE", iup.imageRGBA(48, 48, cast[ptr cuchar](unsafeAddr(confpic))))
iup.setAttributeHandle(conf, "IMAGE", loadf())
#iup.setAttribute(conf, "IMAGE", "IUP_ToolsSettings")
iup.setAttribute(conf, "FLAT", "YES")
iup.setAttribute(conf, "TIP", "Settings")

var statusbar = iup.hbox(info, cln, conf, nil)
iup.setAttribute(statusbar, "NAME", "BAR")
iup.setAttribute(statusbar, "ALIGNMENT", "ACENTER")

var root = iup.dialog(iup.vbox(septp, container, sepfr, statusbar,nil))
iup.setAttribute(root, "TITLE", "UCH Notepad")
iup.setAttribute(root, "RASTERSIZE", "800x600")
iup.setAttribute(root, "MINSIZE", "200x270")
iup.setAttribute(root, "SHRINK", "YES")

discard iup.showXY(root, IUP_CENTER, IUP_CENTER)
#iup.setAttribute(conf, "IMAGE", "C:\\nim-1.4.2\\scripts\\kk.bmp")

discard iup.mainLoop()

iup.close()
