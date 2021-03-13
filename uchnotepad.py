import tkinter.filedialog
import tkinter as tk
#from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import ttk, font, messagebox
import lzma, xml.dom.minidom, pathlib, PIL, os, win32clipboard, hashlib, json, sys, urllib, webbrowser
from pathlib import Path
from PIL import ImageTk, Image, ImageGrab
from io import BytesIO
from urllib import request, error
from pyglet import font as pyfont

shldiscr= 1
check = 0
chash = "68b329da9893e34099c7d8ad5cb9c940"
filepath= ""
unsaved= False
frmat = None
linec = "1.0"
#global fnd
fnd = 0
rpl = 0
lastcol= None
lastpatt= ""
whlm = 0

pyfont.add_file("lib/SearchIcons.ttf")
def loadJson():
    f = open(os.path.join(sys.path[0], 'config.json'), "r")
    data= json.loads(f.read())
    f.close()
    return data
def saveJson():
    global data
    f = open(os.path.join(sys.path[0], 'config.json'), "w+")
    data["state"] = root.state()
    if root.state() == "zoomed":
        root.state("normal")
    data["wm"] = root.winfo_geometry()
    f.write(json.dumps(data, indent=4))
    f.close()
def updateJson():
    try: a= data["sort"]
    except KeyError: data["sort"]= False
    try: b= data["syntax"]
    except KeyError: data["syntax"]= True
    try: c= data["stxtype"]
    except KeyError: data["stxtype"]= "Current line + tags"
class config():
    def __init__(self):
        global data
        self.root = tk.Toplevel(root)
        self.root.title("Settings")
        scy = int(((root.winfo_y() + (root.winfo_height()/2) - 132)**2)**0.5)
        scx = int(root.winfo_x() + (root.winfo_width()/2) - 250)
        self.root.geometry("+" + str(scx) + "+" + str(scy))
        self.root.transient(root)
        self.root.iconbitmap('icon.ico')
        self.root.rowconfigure(6, weight=1)
        self.root.rowconfigure(8, weight=0)
        self.root.minsize(500,263)
        self.root.columnconfigure(3, weight=1)
        root.attributes('-disabled', True)
        self.root.focus_set()
        panel = ttk.Frame(self.root, relief="groove", borderwidth=2)
        panel.grid(row=1, column=0, sticky="nsw", padx=8, rowspan=7)
        self.sel = tk.Frame(panel, bg= "#0078D7", width= 130, height=28)
        self.sel.grid(padx=2, pady=2)
        panel.genshw = tk.PhotoImage(data="R0lGODlhEgASANUAAP////7+/vv7+/r6+vn5+fj4+Pb29vX19e7u7urq6ufn597e3tra2tnZ2djY2NfX19PT08zMzLy8vKurq6qqqqmpqZ+fn52dnZycnJubm5aWlpGRkYKCgoGBgXV1dW5ubmxsbGVlZV5eXlxcXFhYWFRUVFNTU09PT01NTUdHR0FBQTg4ODExMSwsLCcnJyUlJSMjIxoaGhQUFBMTExISEgQEBAEBAQAAAP///wAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAADgALAAAAAASABIAAAaqQBwOQBwSaCyTJwIQOocDIuBxq94ozScg4boADhzrDZIVAgSqKoomvnmlxE973gEsLADDat62vaoMAAUhYiQSEy1zG0QOVidSCDJtKQABGVYVTUQjYjEgIDFiGnApVhgBAKViMApEEjVWDUQbczIiJbBWIQUADFUvNnxiKwYAFgsAHcJWH3BEF20zKFUqAmVDEGIcxRcuCddDFGIPUlFPZhEeJiw0BJpFOEEAOw==")
        panel.theme= tk.PhotoImage(data="R0lGODlhEgASAOYAAP////7+/vz8/Pv7+/n5+fb29vX19fT09PHx8ezs7Ojo6OXl5ePj4+Dg4N/f39vb29TU1NDQ0M7Ozs3NzcnJycbGxsPDw8HBwcDAwL+/v7u7u7q6ura2trGxsbCwsKmpqaioqKSkpJiYmJaWlpSUlJCQkI2NjYiIiIeHh4aGhoWFhXp6enl5eXd3d3FxcXBwcGpqamhoaGZmZmRkZF1dXVxcXFtbW1dXV0pKSkZGRkVFRUBAQD09PS8vLy0tLSYmJiUlJSQkJCMjIxcXFxUVFRMTExISEg8PDwwMDAsLCwgICAcHBwYGBgUFBQQEBAMDAwICAgAAAP///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAFIALAAAAAASABIAAAergFKCg4SFhACIhopSAA4yFwCLhQAvUUUJkZKCABlRUTOZmow3UVAVkYihkwxIUT4DABs1HaqHJ54pNJ5NELWbBD9RT57CIL6IGELEUTpDK74FNstBGgAYTR6pqB/ESioEqShGJiEkFIgPTK4NqQUWASpOUUoiqCMsSxMABxICMD1HiLRYEAqRDCEICOTokQRICQOJDhXwsQMHFB4cAvgaBEBBDBcRImrSJikQADs=")
        panel.info= tk.PhotoImage(data="R0lGODlhEgASAMQAAP////z8/Pn5+fj4+PDw8O3t7evr6+rq6qOjo5OTk5CQkI2NjWBgYFpaWllZWVhYWAYGBgUFBQAAAP///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAABMALAAAAAASABIAAAVz4CSOQGmOKGkOgwmkYnk8kSRFz1Gm5WL/P8UuBvD9Fkab8DUBHICSQACqawIeUAYD2nDVoGDICkwggFuAAVgKFpi+PzZQbMIC5b/uC2CA4m0GTCUKQAgIQAlDVoRgEolMKgYOEDYQDQWKKC4sLjCaLpAjIQA7")
        self.gen = tk.Label(panel, text="  General", width=114, relief="flat", anchor="w", pady=2, compound="left", image=panel.genshw)
        self.gen.grid(row=1, column=0, sticky="ew", padx=3, pady=3)
        self.theme = tk.Label(panel, text="  Appearance", relief="flat", width=114, anchor="w", image=panel.theme, compound="left", pady=2)
        self.theme.grid(row=2, column=0, sticky="ew", padx=3, pady=3)
        self.info = tk.Label(panel, text="  About", relief="flat", width=114, anchor="w", image=panel.info, compound="left", pady=2)
        self.info.grid(row=3, column=0, sticky="ew", padx=3, pady=3)
        self.cont = tk.Frame(self.root)
        self.desct = ttk.Labelframe(self.root)
        if data["theme"] == "dark":
            self.root["bg"]= "#454545"
            self.cont["bg"]= "#45457c"
        self.desc = ttk.Label(self.desct, justify="left")
        self.desct.grid(row=1, column=1, sticky="nsew", columnspan=5)
        self.foont = ttk.Labelframe(self.root)
        self.desc1 = ttk.Label(self.foont, justify="left")
        self.desc.grid(row=1, column=1, sticky="nw", rowspan=3)
        self.desc1.grid(row=5, column=1, sticky="nsew", rowspan=3)
        self.gen.bind("<Button-1>", self.change_tab1)
        self.theme.bind("<Button-1>", self.change_tab2)
        self.info.bind("<Button-1>", self.change_tab3)
        self.rdf = ttk.Button(self.root, text= "Reset to Defaults", width=16, command= self.ask)
        self.bok = ttk.Button(self.root, text= "OK", width=10, command= self.okb)
        self.bcl = ttk.Button(self.root, text= "Cancel", width=10, command= self.ext)
        self.bap = ttk.Button(self.root, text= "Apply", width=10, command= self.applyb)
        self.rdf.grid(row=8, column=0, sticky="sw", padx=8, pady=8)
        self.bok.grid(row=8, column=3, sticky="se", pady=8)
        self.bcl.grid(row=8, column=4, sticky="se", pady=8, padx=8)
        self.bap.grid(row=8, column=5, sticky="se", pady=8)
        self.showtn= tk.StringVar()
        self.showlc= tk.StringVar()
        self.sortx= tk.StringVar()
        self.sythl= tk.StringVar()
        self.showtn.set(data["shwtn"])
        self.showlc.set(data["shwlc"])
        self.sortx.set(data["sort"])
        self.sythl.set(data["syntax"])
        self.onftn = ttk.Checkbutton(self.foont, variable= self.showtn, text= "Show level thumbnails")
        self.onflc = ttk.Checkbutton(self.foont, variable= self.showlc, text= "Show current line/column position")
        self.onstr = ttk.Checkbutton(self.foont, variable= self.sortx, text= "Sort XML values alphabetically")
        self.supp = ttk.Frame(self.foont)
        self.onsyt = ttk.Checkbutton(self.supp, variable= self.sythl, text= "Syntax highlighting:")
        self.warn = ttk.Label(self.foont, font= "{Segoe UI} 8", text= "Warning: Syntax highlighting \"Everything\" will increase\nloading times and scroll lag if used with small font size")
        self.combo1 = ttk.Combobox(self.supp, state="readonly", width=17, values=('Current line', 'Current line + tags', 'Everything'))
        self.combo1.set(data["stxtype"])
        self.change_tab1(None)
        self.crtf = tk.StringVar()
        self.cruf = tk.StringVar()
        self.crtf.set(data["fnt"])
        self.cruf.set(data["ufnt"])
        self.nsf= data["fnt"]
        self.nsuf= data["ufnt"]
        self.currenttheme= tk.StringVar()
        self.themeli= ttk.Radiobutton(self.desct, text="Light Theme", variable=self.currenttheme, value= "light")
        self.themedk= ttk.Radiobutton(self.desct, text="Dark Theme", variable=self.currenttheme, value= "dark")
        self.currenttheme.set(data["theme"])
        self.txf= ttk.Label(self.foont, anchor= tk.W, text= data["fnt"].translate(str.maketrans({'{': '', '}': ''})), font= data["fnt"])
        self.ctxf= ttk.Button(self.foont, text="Change...", command= self.cht)
        self.uxf= ttk.Label(self.foont, anchor= tk.W, text= data["ufnt"].translate(str.maketrans({'{': '', '}': ''})), font= data["ufnt"])
        self.cuxf= ttk.Button(self.foont, text="Change...", command= self.chu)
        self.upt= ttk.Button(self.desct, text= "Check for updates", command= self.update)
        self.result= ttk.Label(self.desct, text= "...", justify="left")
        self.dwl= tk.Button(self.desct, relief="flat", activeforeground= "#0094FF", fg= "#0094FF", text="(Download)", command= self.browupt)
        root.bind("<FocusIn>", self.focuz)
        self.root.protocol("WM_DELETE_WINDOW", self.ext)
    def ext(self):
        root.unbind("<FocusIn>")
        root.attributes('-disabled', False)
        self.root.destroy()
    def focuz(self, event):
        self.root.focus_force()
        self.root.bell()
    def change_tab1(self, event):
        for widgts in self.desct.winfo_children():
            widgts.grid_remove()
        for widgetts in self.foont.winfo_children():
            widgetts.grid_remove()
        self.desct.grid(rowspan=1)
        self.foont.grid(row=6, column=1, sticky="nsew", columnspan=5)
        self.desc.grid(row=1, column=1, sticky="nw", rowspan=4, columnspan=1)
        self.sel.grid(row= 1)
        self.gen["bg"]= "#BFDDF5"
        self.theme["bg"]= "gray94"
        self.info["bg"]= "gray94"
        wmcx = root.winfo_x()
        wmcy = tk.StringVar()
        wmcy.set(root.winfo_y())
        wmcw = tk.StringVar()
        wmcw.set(root.winfo_width())
        wmch = tk.StringVar()
        wmch.set(root.winfo_height())
        self.desct["text"]=" Window "
        self.desc["text"]="   Window position (X,Y):\n\n   Window size (W, H):"
        self.foont["text"]=" Options "
        self.onftn.grid(row=6, column=1, sticky="w", padx=10)
        self.onflc.grid(row=7, column=1, sticky="w", padx=10)
        self.onstr.grid(row=8, column=1, sticky="w", padx=10)
        self.supp.grid(row=9, column=1, sticky="w", padx=10)
        self.onsyt.grid(row=9, column=1, sticky="w")
        self.warn.grid(row=10, column=1, sticky="w", padx=10)
        self.combo1.grid(row=9, column=2, sticky="w")
        self.wmx = tk.Entry(self.desct, width=6)
        self.wmx.insert(10, wmcx)
        self.wmx.grid(row=1,column=2, sticky="nw", padx=2)
        self.wmy = tk.Entry(self.desct, width=6, textvariable= wmcy)
        self.wmy.grid(row=1,column=3, sticky="nw", padx=6)
        self.wmw = tk.Entry(self.desct, width=6, textvariable= wmcw)
        self.wmw.grid(row=2,column=2, sticky="nw", padx=2, pady=11)
        self.wmh = tk.Entry(self.desct, width=6, textvariable= wmch)
        self.wmh.grid(row=2,column=3, sticky="nw", padx=6, pady=11)
        self.desct.rowconfigure(1, weight=1)
        self.desct.columnconfigure(3, weight=30)
        self.filler= ttk.Label(self.root, text=" ")
        self.filler.grid(row=0, column=6, sticky="ns", rowspan=4)
        self.filler1= ttk.Label(self.root, text=" ", font= "Courier 1")
        self.filler1.grid(row=0, column=0, sticky="new")
    def change_tab2(self, event):
        for widgts in self.desct.winfo_children():
            widgts.grid_remove()
        for widgetts in self.foont.winfo_children():
            widgetts.grid_forget()
        self.desct.grid(rowspan=1)
        self.foont.grid(row=6, column=1, sticky="nsew", columnspan=5)
        self.sel.grid(row= 2)
        self.theme["bg"]= "#BFDDF5"
        self.gen["bg"]= "gray94"
        self.info["bg"]= "gray94"
        self.desct["text"]=" Theme "
        self.desc1["text"]="   Text font:\n\n   UI font:"
        self.themeli.grid(row=1,column=1, sticky="nw", padx=10, columnspan=3)
        self.themedk.grid(row=2,column=1, sticky="nw", padx=10, columnspan=3)
        self.desc1.grid(row=6, column=1, sticky="nw", rowspan=3, columnspan=1)
        self.txf.grid(row=6, column=2, sticky="nw")
        self.ctxf.grid(row=6, column=3, sticky="ne")
        self.uxf.grid(row=7, column=2, sticky="nw", pady=5)
        self.cuxf.grid(row=7, column=3, sticky="ne", pady=5)
        self.foont["text"]=" Font "
    def change_tab3(self, event):
        for widgts in self.desct.winfo_children():
            widgts.grid_remove()
        for widgetts in self.foont.winfo_children():
            widgetts.grid_remove()
        self.foont.grid_forget()
        self.desct.grid(sticky="nsew", rowspan=7)
        self.desc.grid(row=0, column=1, sticky="nw", rowspan=1, columnspan=9)
        self.sel.grid(row= 3)
        self.info["bg"]= "#BFDDF5"
        self.gen["bg"]= "gray94"
        self.theme["bg"]= "gray94"
        self.desct["text"]=" About UCH Notepad "
        self.desc["text"]="   Version 1.3 Beta 1\n   Made by Grim Stride using Python 3.9.0 and cx-Freeze\n   This is a heavily modified version of Real Python's Tkinter\n   tutorial\n   Text editor functionality based on Notepad++\n   Icons taken from The GNOME Project and material.io"
        self.upt.grid(row=1, column=1, sticky="nw", padx=8, pady=8)
        self.result.grid(row=1, column=2, sticky="nw", pady=11)
    def update(self):
        try:
            r = urllib.request.urlopen("https://github.com/GrimStride/UCH-Notepad/releases/latest")
            e = r.geturl()
            d = os.path.basename(e)
            if d > str(1.2):
                self.result["text"]= "Version " + d + " is available"
                self.dwl.configure(bg= self.root["bg"], activebackground= self.root["bg"])
                self.dwl.grid(row=7, column=3, pady=3)
            else: self.result["text"]= "No updates are available"
        except urllib.error.URLError: self.result["text"]= "No internet connection"
    def browupt(self):
        webbrowser.open('https://github.com/GrimStride/UCH-Notepad/releases/latest', new=2)
    def okb(self):
        self.savechges()
        root.update()
        self.ext()
    def applyb(self):
        self.savechges()
        root.update()
    def savechges(self):
        global s
        global frmat
        b = False
        x = self.wmx.get()
        y = self.wmy.get()
        w = self.wmw.get()
        h = self.wmh.get()
        a = root.geometry(str(w) + "x" + str(h) + "+" + str(x) + "+" + str(y))
        if self.currenttheme.get() != data["theme"]: b=True
        if self.currenttheme.get() == "dark":
            tdark()
            data["theme"]= "dark"
            self.root["bg"]= "#454545"
            self.cont["bg"]= "#454545"
            txt_edit.tag_configure("curr1", selectbackground= "#4d5d60", background= "#394447")
            try:
                txt_edit.tag_configure("search", background="#773f1f", foreground="white", selectbackground="#7f6a00")
            except: pass    
        else:
            tlight()
            data["theme"]= "light"
            self.root["bg"]= "#f0f0f0"
            self.cont["bg"]= "#f0f0f0"
            txt_edit.tag_configure("curr1", selectbackground= "#c0c0c0", background= "#e8e8ff")
            try: txt_edit.tag_configure("search", background="#F5CC84", foreground="black", selectbackground="#ffa657")
            except: pass
        if self.nsf != data["fnt"]:
            txt_edit["font"] = self.nsf
            data["fnt"] = self.nsf 
        else: pass
        if self.nsuf != data["ufnt"]:
            s.configure("TButton", font= self.nsuf)
            for change in uif:
                change["font"]= self.nsuf
                data["ufnt"] = self.nsuf
        else: pass
        if self.showtn.get() == "0":
            data["shwtn"] = False
        else: data["shwtn"] = True
        if self.showlc.get() == "0":
            data["shwlc"] = False
            txpos["text"] = ""
        else: data["shwlc"] = True
        '''if self.sortx.get() == "0":
            data["sort"] = False
            frmat = UnsortedAttributes()
        else:
            data["sort"] = True
            frmat= None'''
        if self.sythl.get() == "0":
            data["syntax"] = False
            try:
                for tag in txt_edit.tag_names():
                    txt_edit.tag_delete(tag)
            except NameError: pass
        else:
            data["syntax"] = True
        if self.combo1.get() != data["stxtype"]: b= True
        if self.combo1.get() == "Current line + tags":
            data["stxtype"]= "Current line + tags"
            try: txt_edit.tag_remove("sids", "1.0", "end")
            except NameError: pass
        elif self.combo1.get() == "Everything":
            data["stxtype"]= "Everything"
        else: data["stxtype"]= "Current line"
        if b == True: checksyntax(None)
    def ask(self):
        a= messagebox.askyesnocancel(parent= self.root, message='All preferences will be reset to their defaults.\nProceed?', icon='question', title='Settings')
        if a == True:
            self.defaults()
        else: return
    def defaults(self):
        self.nsf= "Courier 10"
        self.nsuf= "{Segoe UI} 9"
        self.currenttheme.set("light")
        self.showtn.set("1")
        self.showlc.set("1")
        self.sortx.set("0")
        self.sythl.set("1")
        self.combo1.set("Current line + tags")
        self.savechges()
        self.txf.configure(text= self.nsf.translate(str.maketrans({'{': '', '}': ''})), font= self.nsf)
        self.uxf.configure(text= self.nsuf.translate(str.maketrans({'{': '', '}': ''})), font= self.nsuf)
        self.cont.update()
    def cht(self):
        global data
        self.root.tk.call('tk', 'fontchooser', 'configure', '-font', self.nsf, '-command', root.register(self.font_changed))
        self.root.tk.call('tk', 'fontchooser', 'show')
    def font_changed(self, font):
        self.nsf = font
        self.txf["font"]= font
        self.txf["text"]= font.translate(str.maketrans({'{': '', '}': ''}))
    def chu(self):
        global data
        self.root.tk.call('tk', 'fontchooser', 'configure', '-font', self.nsuf, '-command', root.register(self.ufont_changed))
        self.root.tk.call('tk', 'fontchooser', 'show')
    def ufont_changed(self, font):
        self.nsuf = font
        self.uxf["font"]= font
        self.uxf["text"]= font.translate(str.maketrans({'{': '', '}': ''}))

def open_file(mode):
    if mode != "2":
        if mode == "1":
            stype= "rules"
            ftype= (("UCH Compressed Ruleset", "*.ruleset"), ("All Files", "*.*"))
        else:
            stype= "snapshots"
            ftype= (("UCH Compressed Level", "*.v.snapshot *.c.snapshot"), ("UCH Compressed Party Level", "*.v.snapshot"), ("UCH Compressed Challenge Level", "*.c.snapshot"), ("UCH Uncompressed Party Level", "*.v"), ("UCH Uncompressed Challenge Level", "*.c"), ("All Files", "*.*"))
        filepath1 = tk.filedialog.askopenfilename(
            initialdir=str(Path.home()) + "/AppData/LocalLow/Clever Endeavour Games/Ultimate Chicken Horse/" + stype, filetypes= ftype)
    else:
        filepath1= os.path.abspath(sys.argv[1]).replace("\\", "/")
    if not filepath1:
        return
    txt_edit.delete("1.0", tk.END)
    extension = os.path.splitext(filepath1)[1]
    if extension == ".snapshot" or extension == ".ruleset":
        with lzma.open(filepath1, "r") as input_file:
            text = input_file.read()
            if text.decode("utf-8").find("\n ") == -1: b = True
            else: b = False
    else:
        with open(filepath1, "r") as input_file:
            text = input_file.read()
            if text.find("\n ") == -1: b = True
            else: b = False
    if b == False:
        text3 = text
    else:
        text1 = xml.dom.minidom.parseString(text)
        text2 = text1.toprettyxml(indent=" ")
        text3 = text2.replace("<?xml version=\"1.0\" ?>" + "\n", "")
    txt_edit.insert(1.0, text3.rstrip())
    txt_edit.edit_modified(0)
    txt_edit.edit_reset()
    checksyntax(None)
    #print(b)
    #print(text)
    global filepath
    global lastcol
    filepath = filepath1
    TButton()
    bhash= txt_edit.get(1.0, tk.END)
    global chash
    chash = hashlib.md5(bhash.encode('utf-8')).hexdigest()
    txt_edit.mark_set("insert", "1.0")
    lastcol = None
    root.title(f"{filepath} - UCH Notepad ")

def syntax(pattern, tag, color, start, end,regexp=False):
    if data["stxtype"] == "Current line":
        try: txt_edit.tag_remove(tag, "1.0", "end")
        except NameError: pass
        start= txt_edit.index("insert linestart")
        end= txt_edit.index("insert lineend")
    elif data["stxtype"] == "Current line + tags" and tag == "sids":
        try: txt_edit.tag_remove(tag, "1.0", "end")
        except NameError: pass
        start= txt_edit.index("insert linestart")
        end= txt_edit.index("insert lineend")
    else:
        try:
            txt_edit.tag_remove(tag, start, end)
        except NameError: pass
        start = txt_edit.index(start)
        end = txt_edit.index(end)
    txt_edit.mark_set("matchStart", start)
    txt_edit.mark_set("matchEnd", start)
    txt_edit.mark_set("searchLimit", end)

    count = tk.IntVar()
    while True:
        index = txt_edit.search(pattern, "matchEnd","searchLimit", count=count, regexp=regexp)
        if index == "": break
        if count.get() == 0: break
        txt_edit.mark_set("matchStart", index)
        txt_edit.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
        '''try:
            for tag in text.tag_names():
                txt_edit.tag_remove(tag)
        except NameError: pass'''
        if pattern[-1] == " ":
            txt_edit.tag_add(tag, "matchStart+1c", "matchEnd")
            txt_edit.tag_configure(tag, foreground=color)
        elif pattern[-1] == ">":
            txt_edit.tag_add(tag, "matchStart+1c", "matchEnd-1c")
            txt_edit.tag_configure(tag, foreground=color)
        else:
            txt_edit.tag_add(tag, "matchStart-1c wordstart", "matchEnd")
            txt_edit.tag_configure(tag, foreground=color)

def checksyntax(event):
    if data["syntax"] == False: return
    if event == None or event.keysym == "Control_L" or event.keysym == "Control_R":
        strt= "1.0"
        fin= "end"
    else:
        strt= "insert linestart"
        fin= "insert lineend"
    if data["theme"] == "dark":
        colh= "#63bf63"
        colr= "#ab758b"
        colru= "#a55dc6"
        colb= "#d4863b"
        colm= "#9b933b"
        cold= "#f85149"
        colp= "#c17c00"
        colt= "#569cd6"
    else:
        colh= "#008000"
        colr= "#bc2b6a"
        colru= "#680099"
        colb= "#bc4b00"
        colm= "#a88b1c"
        cold= "#880000"
        colp= "#a56800"
        colt= "#006abc"
    syntax("<scene ", "header", colh, strt, fin)
    syntax("<Ruleset ", "header1", colh, strt, fin)
    syntax("</scene>", "footer", colh, strt, fin)
    syntax("</Ruleset>", "footer1", colh, strt, fin)
    syntax("<mods ", "mod", colr, strt, fin)
    syntax("<rules ", "rul", colru, strt, fin)
    syntax("<block ", "blocks", colb, strt, fin)
    syntax("<moved ", "moveds", colm, strt, fin)
    syntax("<destroyed ", "destroys", cold, strt, fin)
    syntax("<points>", "points", colp, strt, fin)
    syntax("</points>", "points1", colp, strt, fin)
    syntax("<point ", "point", colm, strt, fin)
    syntax("<blocks>", "blockos", cold, strt, fin)
    syntax("</blocks>", "blockos1", cold, strt, fin)
    syntax("=", "sids", colt, strt, fin)

def nsave():
    global filepath
    if filepath != "":
        extension = os.path.splitext(filepath)[1]
        if extension == ".ruleset" or extension == ".snapshot" or extension == ".lzma":
            with lzma.open(filepath, "w", format=lzma.FORMAT_ALONE) as output_file:
                text = txt_edit.get(1.0, tk.END)
                text1= text.replace("  ", " ").replace("\n ", "").replace("\n", "")
                output_file.write(bytes(text1, "utf-8"))
                #print("Save - - - -:\n" + text1)
        else:
            with open(filepath, "w") as output_file:
                text = txt_edit.get(1.0, tk.END)
                text1= text.replace("  ", " ").replace("\n ", "").replace("\n", "")
                output_file.write(text1)
        bhash= txt_edit.get(1.0, tk.END)
        global chash
        chash = hashlib.md5(bhash.encode('utf-8')).hexdigest()
        root.title(f"{filepath} - UCH Notepad 1.3 Beta 1")
    else: save_file()

def save_file():
    global filepath
    known = [".snapshot", ".ruleset", ".lzma"]
    itlvl = txt_edit.search("<scene", "1.0", "1.7")
    itrul = txt_edit.search("<Ruleset", "1.0", "1.9")
    if itlvl == "1.0":
        filepaths = tk.filedialog.asksaveasfilename(
            initialdir= filepath.replace(os.path.basename(filepath),""),
            defaultextension="v.snapshot",
            filetypes=[("UCH Compressed Party Level", "*.v.snapshot"), ("UCH Compressed Challenge Level", "*.c.snapshot"), ("UCH Uncompressed Party Level", "*.v"), ("UCH Uncompressed Challenge Level", "*.c"), ("All Files", "*.*")],
        )
    elif itrul == "1.0":
        filepaths = tk.filedialog.asksaveasfilename(
            initialdir= filepath.replace(os.path.basename(filepath),""),
            defaultextension="ruleset",
            filetypes=[("UCH Compressed Ruleset", "*.ruleset"), ("All Files", "*.*")],
        )
    else:
        filepaths = tk.filedialog.asksaveasfilename(initialdir= filepath.replace(os.path.basename(filepath),""), defaultextension="lzma", filetypes=[("LZMA Encoded File", "*.lzma"), ("Text File", "*.txt"), ("All Files", "*.*")])
    if not filepaths: return
    extension = os.path.splitext(filepaths)[1]
    if extension in known:
        with lzma.open(filepaths, "w", format=lzma.FORMAT_ALONE) as output_file:
            text = txt_edit.get(1.0, tk.END)
            text1= text.replace("  ", " ").replace("\n ", "")
            output_file.write(bytes(text1, "utf-8"))
    else:
        with open(filepaths, "w") as output_file:
            text = txt_edit.get(1.0, tk.END)
            text1= text.replace("  ", " ").replace("\n ", "")
            output_file.write(text1)
    filepath = filepaths
    bhash= txt_edit.get(1.0, tk.END)
    global chash
    chash = hashlib.md5(bhash.encode('utf-8')).hexdigest()
    root.title(f"{filepath} - UCH Notepad 1.3 Beta 1")

def TButton():
    destroyTN()
    extension = os.path.splitext(filepath)[1]
    global cv
    cv = tk.Button(fr_buttons, bg="black", activebackground="black")
    cv.grid(row=0, column=0, sticky="nsew")
    if extension == ".snapshot" or extension == ".v" or extension == ".c":
        ofile = (Path(filepath).with_suffix('').with_suffix(''))
        clvl = os.path.basename(ofile)
        lvlthumb = str(Path.home()) + "\\AppData\\LocalLow\\Clever Endeavour Games\\Ultimate Chicken Horse\\snapshots\\thumbnails\\" + "l_" + clvl + ".jpg"
        check = os.path.isfile(lvlthumb)
        if check == True and data["shwtn"] == True:
            cv.img = Image.open(lvlthumb)
            cv.res = cv.img.resize((84, 60), Image.ANTIALIAS)
            cv.thumb = ImageTk.PhotoImage(cv.res)
            cv["image"] = cv.thumb
            cv["command"] = opnthb
        else:
            destroyTN()
    else:
        destroyTN()

def destroyTN():
    try:
        cv.grid_remove()
    except NameError:
        return
def opnthb():
    Thumbnail = ShowTN(root)
class ShowTN:
    def __init__(self, parent):
        ofile = (Path(filepath).with_suffix('').with_suffix(''))
        clvl = os.path.basename(ofile)
        self.lvlthumb = str(Path.home()) + "\\AppData\\LocalLow\\Clever Endeavour Games\\Ultimate Chicken Horse\\snapshots\\thumbnails\\" + "l_" + clvl + ".jpg"
        self.root = tk.Toplevel(parent, bg="white")
        self.root.title(clvl)
        self.root.geometry("512x366")
        self.root.resizable(False,False)
        self.root.iconbitmap('icon.ico')
        self.root.focus_set()
        self.root.photo = ImageTk.PhotoImage(file= self.lvlthumb)
        cw = tk.Canvas(self.root, height=512, width=366)
        cw.create_image(256, 183, image = self.root.photo)
        cw.pack(fill="both", expand=True)
        self.root.bind("<Button-3>", self.popup)
        self.m = tk.Menu(self.root, tearoff=0)
        self.m.add_command(label ="Copy", command=self.copyim)
        self.m.add_separator() 
        self.m.add_command(label ="Save As...", command=self.save_thmb)
    def popup(self, event):
        try: 
            self.m.tk_popup(event.x_root, event.y_root) 
        finally: 
            self.m.grab_release()
    def copyim(self):
        output = BytesIO()
        cpyim= Image.open(self.lvlthumb)
        imcnv= cpyim.convert("RGB").save(output, "BMP")
        data = output.getvalue()[14:]
        output.close()
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
        win32clipboard.CloseClipboard()
    def save_thmb(self):
        thmbpath = tk.filedialog.asksaveasfilename(
        defaultextension="jpg",
        filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("BMP", "*.bmp"), ("GIF", "*.gif"), ("TGA", "*.tga")],
        parent= self.root)
        if not thmbpath:
            self.root.focus_set()
            return
        else:
            iformat = os.path.splitext(thmbpath)[1]
            target= Image.open(self.lvlthumb)
            target.save(thmbpath)
            self.root.focus_set()
def tlight():
    for change in wmcol:
        change["bg"]= "#f0f0f0"
    for change in uif:
        change["fg"]= "black"
    for change in shbt:
        change.configure(bg="#f0f0f0", fg="black", activebackground="#f0f0f0", activeforeground="black")
    for change in chkbts:
        change.configure(bg = "#f0f0f0", selectcolor = "#d0d0d0", fg="black", highlightcolor="black", activebackground="#f0f0f0", activeforeground="black")
    expand.configure(bg="#f0f0f0", fg="black", activebackground="#f0f0f0", activeforeground="black")
    txt_edit.configure(bg="white", fg="black", insertbackground="black", selectbackground= "#c0c0c0", selectforeground= "black")
    for change in sentries: change.configure(bg="white", fg="black", disabledbackground="#f0f0f0", insertbackground="black")
    btn_conf['activebackground'] = "#f0f0f0"
    s.configure("TSeparator", background= "#f0f0f0")
    s.configure("TFrame", background= "white")
    s.configure("S.TFrame", background= "#f0f0f0")
    #s.map("S.TFrame", highlightbackground =[('focus', 'green'),('!focus', 'red')], highlightcolor= [('focus', 'green'),('!focus', 'red')])
    s.configure("TLabel", background= "#f0f0f0", foreground= "black")
    s.configure("S.TLabel", background= "#f0f0f0", foreground= "black")
    #s.map("S.TLabel", borderwidth=[("hover", 1)])
    s.configure("TLabelframe", background= "#f0f0f0", foreground= "black")
    s.configure("TLabelframe.Label", background= "#f0f0f0", foreground= "black")
    s.configure("TCheckbutton", background= "#f0f0f0", foreground= "black")
    s.configure("TRadiobutton", background= "#f0f0f0", foreground= "black")
def tdark():
    for change in wmcol:
        change["bg"]= "#242424"
    for change in uif:
        change["fg"]= "#dedede"
    for change in shbt:
        change.configure(bg="#343434", fg="#dedede", activebackground="#242424", activeforeground="#dedede",highlightbackground = "#dedede", highlightcolor= "#dedede")
    for change in chkbts:
        change.configure(bg = "#242424", selectcolor = "#444444", fg = "#dedede", highlightcolor="#dedede", activebackground="#242424", activeforeground="white")
    expand.configure(bg="#242424", fg="#dedede", activebackground="#242424", activeforeground="#dedede")
    txt_edit.configure(bg="#2e2e2e", fg="#dedede", insertbackground="#dedede", selectbackground= "#4d5d60", selectforeground= "#e2e2e2")
    for change in sentries: change.configure(bg= "#3e3e3e", fg= "#dedede", disabledbackground="#303030", insertbackground="#dedede")
    btn_conf['activebackground'] = "#2e2e2e"
    s.configure("TSeparator", background= "black")
    s.configure("TFrame", background= "#323232")
    s.configure("S.TFrame", background= "#242424")
    #s.map("S.TFrame", highlightbackground = "black", highlightcolor= "black")
    s.configure("TLabel", background= "#454545", foreground= "#dedede")
    s.configure("S.TLabel", background= "#242424", foreground= "#dedede")
    #s.map("S.TLabel", borderwidth=[("hover", 1)])
    s.configure("TLabelframe", background= "#454545", foreground= "#dedede")
    s.configure("TLabelframe.Label", background= "#454545", foreground= "#dedede")
    s.configure("TCheckbutton", background= "#454545", foreground= "#dedede")
    s.configure("TRadiobutton", background= "#454545", foreground= "#dedede")

def get_line1():
    global lastcol
    global txpos
    global chash
    global filepath
    global unsaved
    if data["shwlc"] == True:
        ln, col = txt_edit.index("insert").split(".")
        coll= int(float(col) + 1)
        txpos["text"]= "Ln: " + ln + "   Col: " + str(coll)
    else: pass
    if shldiscr == 0:
        txt_edit.see("insert")
    else:
        pass
    cwork= txt_edit.get(1.0, tk.END)
    gethash= hashlib.md5(cwork.encode('utf-8')).hexdigest()
    if gethash != chash:
        if chash != "68b329da9893e34099c7d8ad5cb9c940":
            root.title(f"*{filepath} - UCH Notepad 1.3 Beta 1")
            unsaved= True
        else:
            root.title(f"*UCH Notepad 1.3 Beta 1")
            unsaved= True
    else:
        if chash != "68b329da9893e34099c7d8ad5cb9c940":
            root.title(f"{filepath} - UCH Notepad 1.3 Beta 1")
            unsaved= False
        else:
            root.title(f"UCH Notepad 1.3 Beta 1")
            unsaved= False
    '''try:
        txt_edit.tag_delete("curr1", "1.0", "end")
        #txt_edit.tag_delete("curr2", "1.0", "end")
    except NameError: pass'''
    if data["theme"] == "dark":
        selc= "#4d5d60"
        curc= "#394447"
    else:
        selc= "#c0c0c0"
        curc= "#e8e8ff"
    if lastcol != txt_edit.index("insert").split(".")[0]:
        try: txt_edit.tag_delete("curr1", "1.0", "end")
        except NameError: pass
        txt_edit.tag_add("curr1", "insert linestart", "insert lineend+1c")
        #txt_edit.tag_add("curr2", "insert", "insert lineend+1c")
        txt_edit.tag_configure("curr1", selectbackground= selc, background= curc)
        if "search" in txt_edit.tag_names():
            txt_edit.tag_lower("curr1", belowThis="search")
        '''    print("3")
            txt_edit.tag_configure("search", background="#F5CC84", foreground="black", underline=True, underlinefg="#ffa657")
        #txt_edit.tag_configure("curr2", selectbackground= selc, background= curc)
        '''
        #txt_edit.tag_lower("curr1", belowThis="search")
        lastcol = txt_edit.index("insert").split(".")[0]
    if data["syntax"] == True and data["stxtype"] != "Everything":
        checksyntax(None)
    root.after(33, get_line1)

def x_scroll(*args):
    global shldiscr
    shldiscr = 1
    global txt_edit
    txt_edit.xview(*args)
    txt_edit.config(state="disabled")
def y_scroll(*args):
    global shldiscr
    shldiscr = 1
    global txt_edit
    txt_edit.yview(*args)
    txt_edit.config(state="disabled")
def scrllstop(event):
    shldiscr = 0
    txt_edit.config(state="normal")

def rclkmenu(event):
    global filepath
    if filepath == "": tempst="normal"
    else: tempst="disabled"
    template=tk.Menu(root, tearoff=0, activebackground="#91c9f7", activeforeground="black")
    template.add_command(label="Blank Level")
    template.add_command(label="Crumbling Bridge")
    template.add_command(label="Dance Party")
    template.add_command(label="Iceberg")
    template.add_command(label="Jungle Temple")
    template.add_command(label="Metal Plant")
    template.add_command(label="Nuclear Plant")
    template.add_command(label="Old Mansion")
    template.add_command(label="Pyramid", command=lambda: insertemp("pyr"))
    template.add_command(label="Rooftops")
    template.add_command(label="Space")
    template.add_command(label="The Ballroom")
    template.add_command(label="The Farm")
    template.add_command(label="The Mainframe")
    template.add_command(label="The Pier")
    template.add_command(label="Volcano")
    template.add_command(label="Waterfall")
    template.add_command(label="Windmill")
    m = tk.Menu(root, tearoff=0, activebackground="#91c9f7", activeforeground="black")
    m.add_command(label ="Cut", command= lambda: copycut(0))
    m.add_command(label ="Copy", command= lambda: copycut(1))
    m.add_command(label ="Paste", command= paste)
    m.add_command(label ="Delete", command=lambda: copycut(2))
    m.add_separator() 
    m.add_cascade(label ="Insert template", menu= template, state=tempst)
    try:
        m.tk_popup(event.x_root, event.y_root) 
    finally:
        m.grab_release()
def mundo(event):
    try:
        txt_edit.edit_redo()
    except tk.TclError: return

def findtool(event):
    global fnd
    if fnd == 1:
        finder.grid_forget()
        expand.grid_forget()
        ent.grid_forget()
        prev.grid_forget()
        nxt.grid_forget()
        clse.grid_forget()
        fnd= 0
        txt_edit.focus_set()
        try: txt_edit.tag_remove("searchsel", 1.0, "end")
        except NameError: pass
        try: txt_edit.tag_remove("search", 1.0, "end")
        except NameError: pass
        return
    fnd = 1
    finder.grid(row=0, column=1, sticky="ne")
    finder.rowconfigure(1, pad=4)
    finder.rowconfigure(1, pad=7)
    finder.rowconfigure(2, pad=4)
    expand.grid(row=0, column=0, padx=4)
    ent.grid(row=0, column=1, ipady=2, columnspan=25)
    prev.grid(row=0, column=26, padx=4, ipadx=1, ipady=1)
    nxt.grid(row=0, column=27, ipadx=1, ipady=1)
    clse.grid(row=0, column=28, padx=4, pady=4, ipadx=1, ipady=1)
    casematch.grid(row=2, column=1, sticky="nw")
    wordmatch.grid(row=2, column=2, sticky="nw", ipadx=1)
    regmatch.grid(row=2, column=3, sticky="nw")
    #bluethingy.grid(row=3, column=0, columnspan=29, sticky="nsew")
    ent.focus_set()
def searchtxt(event):
    global lastpatt, csem
    pattern = ent.get()
    try: txt_edit.tag_remove("sel", 1.0, "end")
    except NameError: pass
    try: txt_edit.tag_remove("searchsel", 1.0, "end")
    except NameError: pass
    try: txt_edit.tag_remove("search", "1.0", "end")
    except NameError: pass
    if pattern == "": return
    txt_edit.mark_set("searchStart", "1.0")
    txt_edit.mark_set("searchEnd", "1.0")
    txt_edit.mark_set("Limit", "end")
    count = tk.IntVar()
    a = 0
    current= txt_edit.index("insert")
    while True:
        try:
            index = txt_edit.search(pattern, "searchEnd","Limit", count=count, regexp=regm.get(), nocase=csem.get())
        except tk.TclError: return
        if index == "": break
        if count.get() == 0: break
        #if a == 0: txt_edit.mark_set("insert", index); print("xd"); a += 1
        txt_edit.mark_set("searchStart", index)
        txt_edit.mark_set("searchEnd", "%s+%sc" % (index, count.get()))
        txt_edit.tag_add("search", "searchStart", "searchEnd")
    if lastpatt != pattern:
        try:
            #txt_edit.mark_set("insert", txt_edit.tag_nextrange("search", "insert", "end")[1])
            txt_edit.tag_add("sel", txt_edit.tag_nextrange("search", "insert", "end")[0], txt_edit.tag_nextrange("search", "insert", "end")[1])
            txt_edit.mark_set("insert", "sel.first")
        except IndexError:
            try:
                #txt_edit.mark_set("insert", txt_edit.tag_nextrange("search", "1.0", "end")[1])
                txt_edit.tag_add("sel", txt_edit.tag_nextrange("search", "1.0", "end")[0], txt_edit.tag_nextrange("search", "insert", "end")[1])
                txt_edit.mark_set("insert", "sel.first")
            except IndexError: return
    if data["theme"] == "dark":
        tbg="#773f1f"
        tfg="white"
        tsbg="#7f6a00"
    else:
        tbg="#f5cc84"
        tfg="black"
        tsbg="#ffa657"
    txt_edit.tag_configure("search", background=tbg, foreground=tfg, selectbackground=tsbg)
    txt_edit.tag_raise("search")
    lastpatt == pattern
    txt_edit.see("insert")

def movesearch(mode):
    if ent.get() == "" or not "search" in txt_edit.tag_names(): return
    if txt_edit.tag_ranges("sel"):
        fidx= "sel.last"
        bidx= "sel.first"
    else:
        fidx, bidx= "insert", "insert"
    if mode == 0:
        try: idx1, idx2 = txt_edit.tag_nextrange("search", fidx, "end")
        except ValueError: idx1, idx2 = txt_edit.tag_nextrange("search", "1.0", "end")
    else:
        try: idx1, idx2 = txt_edit.tag_prevrange("search", bidx, "1.0")
        except ValueError: idx1, idx2 = txt_edit.tag_prevrange("search", "end", "1.0")
    try: txt_edit.tag_remove("sel", "1.0", "end")
    except NameError: pass
    txt_edit.tag_add("sel", idx1, idx2)
    txt_edit.mark_set("insert", "sel.first")
    txt_edit.see("insert")

def replacetool():
    global rpl
    if rpl == 0:
        expand["text"]="¸"
        replent.grid(row=1, column=1, ipady=2, columnspan=25)
        rplnext.grid(row=1, column=26, padx=4)
        rplall.grid(row=1, column=27)
        rpl = 1
    else:
        expand["text"]="¹"
        replent.grid_forget()
        rplnext.grid_forget()
        rplall.grid_forget()
        rpl = 0
def rpldefault(event):
    if replace.get()== "":
        replent["state"]="disabled"
        replace.set("Replace...‏‏‎ ‎")
def rpltip(event):
    if replace.get() == "Replace...‏‏‎ ‎":
        replace.set("")
        replent["state"]="normal"
        replent.focus_set()
        replent.bind("<FocusOut>", rpldefault)
def dorpl(mode):
    if replace.get() == "Replace...‏‏‎ ‎" or not txt_edit.tag_ranges("search"): return
    if mode == 0 and txt_edit.tag_ranges("sel"):
        if 'search' in txt_edit.tag_names("sel.first"):
            txt_edit.replace('sel.first','sel.last', replent.get())
        else: return
    elif mode == 1:
        data = txt_edit.tag_ranges("search")
        for i,k in zip(data[-1::-2], data[-2::-2]): txt_edit.replace(str(k), str(i), replent.get())
    else: return

def copycut(mode):
    if txt_edit.tag_ranges("sel"):
        if mode == 2:
            txt_edit.delete("sel.first", "sel.last")
            return
        else: pass
        root.clipboard_clear()
        root.clipboard_append(txt_edit.get("sel.first", "sel.last"))
        if mode == 0: txt_edit.delete("sel.first", "sel.last")
    else: return
def paste():
    txt_edit.insert("insert", root.clipboard_get())
def insertemp(mode):
    if mode == "pyr":
        txt_edit.insert("insert", r'<scene levelSceneName="Pyramid" saveFormatVersion="1">' + "\n " + r'<mods GravityMode="0" JumpSpeedMode="0" SprintSpeedMode="0" WallJumpsDisabled="False" WallSlidesDisabled="False" GameSpeedMode="0" DanceInvincibility="False" InvisibilityMode="0" MirrorControls="False" PlatformSpeedMode="0" RateOfFireMode="0" MultiJumpMode="0" ProjectileExplosionMode="0" CharacterSizeMode="0" JetpackMode="False" PostDeathBehaviorMode="0" CameraFlipMode="0" DoomsdayMeteorsMode="0" DoomsdayLavaMode="0" PlayerPlayerCollisions="False" ProjectileSpeedMode="0" PreviewModsInTreehouse="False" ForceLobbyModifiers="False" Frictionless="False"/>')
def winquit():
    if unsaved == True:
        a= messagebox.askyesnocancel(parent= root, message='Want to save your changes?', icon='warning', title='Unsaved Changes')
        if a == True:
            nsave()
        elif a == False: pass
        else: return
    saveJson()
    root.destroy()

data = loadJson()
updateJson()

root = tk.Tk()
root.title("UCH Notepad 1.3 Beta 1")
root.geometry(data["wm"])
root.minsize(200,270)
root.state(data["state"])
root.iconbitmap('icon.ico')
root.rowconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.protocol("WM_DELETE_WINDOW", winquit)

s = ttk.Style()
s.theme_use("vista")
s.configure("TButton", font= data["ufnt"])

scroll = ttk.Scrollbar(root, orient="vertical")
xascroll = ttk.Scrollbar(root, orient="horizontal")
base= tk.Frame(root)

txt_edit = tk.Text(base, padx=4, undo=True, autoseparators=True, font= data["fnt"], wrap="none", xscrollcommand= xascroll.set, yscrollcommand=scroll.set)

csem = tk.IntVar()
regm = tk.IntVar()
csem.set(1)

a= "🡰"
b= "🡲"
finder = ttk.Frame(base, relief="solid", borderwidth=1, style="S.TFrame")
#bluethingy= tk.Frame(finder, relief="solid", borderwidth=0, highlightthickness=0, bg="#007acc", height=4)
search= tk.StringVar()
replace= tk.StringVar()
replace.set("Replace...‏‏‎ ‎")
ent = tk.Entry(finder, textvariable= search, relief="solid", width=30)
#expand= tk.Button(finder, text="🞃", relief="solid", width=2, font="{Segoe UI} 8", borderwidth=0, command=None)
expand= tk.Button(finder, text="¹", relief="solid", width=2, font="SearchIcons 11", borderwidth=0, command= replacetool)
prev= tk.Button(finder, text=a, command= lambda:[movesearch(1)], relief="solid", width=2, font="{Segoe UI} 8", borderwidth=1, compound="center")
nxt= tk.Button(finder, text=b, command= lambda:[movesearch(0)], relief="solid", width=2, font="{Segoe UI} 8", borderwidth=1)#, style="S.TLabel")
clse= tk.Button(finder, text="·", relief="solid", width=2, font="SearchIcons 11", borderwidth=1, command=lambda:[findtool(None)])
casematch= tk.Checkbutton(finder, text="¼", overrelief="solid", offrelief="flat", width=2, font="SearchIcons 12", borderwidth=1, indicatoron= False, variable=csem, onvalue=0, offvalue=1)
wordmatch= tk.Checkbutton(finder, text="½", overrelief="solid", offrelief="flat", width=2, font="SearchIcons 12", borderwidth=1, indicatoron= False, variable=whlm)
regmatch= tk.Checkbutton(finder, text="¾", overrelief="solid", offrelief="flat", width=2, font="SearchIcons 12", borderwidth=1, indicatoron= False, variable=regm)

replent = tk.Entry(finder, textvariable= replace, relief="solid", width=30, state="disabled")
rplnext= tk.Button(finder, text="º", command= lambda:[dorpl(0)], relief="solid", width=2, font="SearchIcons 12", borderwidth=1)
rplall= tk.Button(finder, text="»", command= lambda:[dorpl(1)], relief="solid", width=2, font="SearchIcons 12", borderwidth=1)
replent.bind("<ButtonRelease-1>", rpltip)

scroll.config(command=y_scroll)
xascroll.config(command=x_scroll)

fr_buttons = tk.Frame(root)
btn_open = ttk.Button(fr_buttons, text="Open Level", command= lambda:[open_file("0")])
btn_orul = ttk.Button(fr_buttons, text="Open Ruleset", command= lambda:[open_file("1")])
btn_nsav = ttk.Button(fr_buttons, text="Save", command=nsave)
btn_save = ttk.Button(fr_buttons, text="Save As...", command=save_file)
btn_open.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
btn_orul.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
btn_nsav.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
fr_buttons.grid(row=0, column=0, sticky="ns")

base.grid(row=0, column=1, sticky="nsew")
base.rowconfigure(0, weight=1)
base.columnconfigure(0, weight=1)
txt_edit.grid(row=0, column=0, sticky="nsew", columnspan=2)

scroll.grid(column=2, row=0, sticky="nse", ipadx=1)
xascroll.grid(column=1, row=1, sticky="we")

statusbar = tk.Label(root, text=" By Grim Stride", anchor=tk.W, bd=0, relief="solid")
sepfr = tk.Frame(root)
sep = ttk.Separator(sepfr, orient="horizontal")
sepfr.grid(row=5, column=0, sticky="ew", columnspan=30)
statusbar.grid(row=6, column=0, sticky="sew", columnspan=2, pady=4)

conb = tk.Frame(root)
conf = "R0lGODlhEAASANUAAP////7+/v39/fj4+PT09PHx8ZKSkomJiX9/f319fXt7e3BwcG5ubmJiYmFhYWBgYF9fX1JSUlFRUUVFRUNDQyYmJiIiIhoaGhcXFxQUFBEREQ0NDQoKCgkJCQgICAAAAP///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAACAALAAAAAAQABIAAAZxQJAQBCgOj8OiAOKhFIpQIwDxqVqvVUTRYLlYM5aw2AAgFhOVxiAKRbaRcPg7yQYQJBhGQHrQ+P8cVhsaB0V9f36BVYOFZmwEERgLe2VxQnNuRpaOChUPa3VEXF5VYGJhZFNYqx9aZgIOHRNPoUeYSEEAOw=="
confshw = tk.PhotoImage(data=conf)
btn_conf = tk.Button(conb, image= confshw, relief="flat", command=config, bd=0)
btn_conf.grid(row=6, column=2, sticky="ew")
conb.grid(row=6, column=2, sticky="e")

root.update()
sep.grid(row=5, column=0, sticky="ew", columnspan=1, ipadx= root.winfo_reqwidth())
txpos = tk.Label(root, width= 15, anchor="center", bd=0, relief="solid")
txpos.grid(row=6, column=1, sticky="e")

scroll.bind("<ButtonRelease-1>", scrllstop)
xascroll.bind("<ButtonRelease-1>", scrllstop)
txt_edit.bind("<ButtonRelease-1>", scrllstop)
txt_edit.bind("<ButtonRelease-3>", rclkmenu)
txt_edit.bind("<Control-Shift-Z>", mundo)
root.bind("<Control-f>", findtool)
root.bind("<Control-F>", findtool)
txt_edit.bind("<KeyRelease>", checksyntax)
txt_edit.bind("<KeyRelease-Control_L>", checksyntax)
txt_edit.bind("<KeyRelease-Control_R>", checksyntax)
#txt_edit.bind("<<ThemeChanged>>", lambda x:[print("yay")])
ent.bind("<KeyRelease>", searchtxt)


wmcol = (root, fr_buttons, sepfr, txpos, statusbar, btn_conf)
uif = (txpos, statusbar)
shbt = (prev, nxt, clse, rplnext, rplall)
buttons = (btn_open, btn_orul, btn_nsav, btn_save)
chkbts = (casematch, wordmatch, regmatch)
sentries = (ent, replent)
if data["theme"] == "dark": tdark()
else: tlight()
if len(sys.argv) >= 2:
    open_file("2")
else: pass
#print(base.bbox("all"))
root.after(5, get_line1)

root.mainloop()
