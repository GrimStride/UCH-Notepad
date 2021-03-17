import iupp as iup
import strformat

proc open_file(ih:PIhandle) =
  echo("heh")
  let filename = iup.fileDlg()
  iup.setAttribute(filename, "DIALOGTYPE", "OPEN")
  iup.setAttributeHandle(filename, "PARENTDIALOG", iup.getDialog(ih))
  iup.popup(filename, IUP_CENTERPARENT, IUP_CENTERPARENT)
  iup.destroy(filename)
  #return iup.IUP_DEFAULT

proc getline(ih:PIhandle, lin:int, col:int): int =
  #echo ("hey")
  let cln = iup.getDialogChild(ih, "STATUSBAR")
  #echo (fmt"Ln: {lin} Col: {col}")
  #echo(cln)
  iup.setfAttribute(cln, "TITLE", fmt"Ln: {lin} Col: {col}")
  let st = iup.getDialogChild(ih, "BAR")
  iup.refreshChildren(st)
  return iup.IUP_DEFAULT


discard iup.open(nil, nil)
iup.imageLibOpen()
iup.glControlsOpen()

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
iup.setAttribute(txt_edit, "CPADDING", "4x4")
iup.setCallback(txt_edit, "CARET_CB", cast[ICallback](getline))

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
iup.setAttribute(info, "PADDING", "0x3")

var cln = iup.label(nil)
iup.setAttribute(cln, "TITLE", "Ln: 1 Col: 1")
iup.setAttribute(cln, "PADDING", "0x3")
iup.setAttribute(cln, "NAME", "STATUSBAR")
iup.setAttribute(cln, "ALIGNMENT", "ARIGHT")
#echo (iup.getHandle(cln))

var conf = iup.button(nil)
#iup.setAttribute(conf, "ACTION", nil)
iup.setAttribute(conf, "IMAGE", "IUP_ToolsSettings")


var statusbar = iup.hbox(info, cln, conf, nil)
iup.setAttribute(statusbar, "NAME", "BAR")

var root = iup.dialog(iup.vbox(septp, container, sepfr, statusbar,nil))
iup.setAttribute(root, "TITLE", "UCH Notepad")
iup.setAttribute(root, "USERSIZE", "600x300")
iup.setAttribute(root, "MINSIZE", "200x270")
iup.setAttribute(root, "SHRINK", "YES")

discard iup.showXY(root, IUP_CENTER, IUP_CENTER)
discard iup.mainLoop()

iup.close()
