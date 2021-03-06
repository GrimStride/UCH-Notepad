import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import ttk, font, messagebox
import lzma, pathlib, PIL, bs4, os, hashlib, json, sys, urllib, webbrowser, subprocess
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import ImageTk, Image, ImageGrab
from io import BytesIO
from urllib import request, error

shldiscr= 1
check = 0
chash = "68b329da9893e34099c7d8ad5cb9c940"
filepath= ""
unsaved= False
frmat = None
linec = "1.0"


def loadJson():
    #a= os.path.isfile("config.json")
    #print(a)
    #f = open(os.path.join(sys.path[0], 'config.json'), "r")
    f = open('config.json', "r")
    data= json.loads(f.read())
    f.close()
    return data
def saveJson():
    global data
    f = open('config.json', "w+")
    data["state"] = root.attributes('-zoomed')
    if root.attributes('-zoomed') == 1:
        root.attributes('-zoomed', False)
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
        scy = int(((root.winfo_y() + (root.winfo_height()/2) - 133)**2)**0.5)
        scx = int(root.winfo_x() + (root.winfo_width()/2) - 250)
        self.root.geometry("+" + str(scx) + "+" + str(scy))
        self.root.transient(root)
        self.root.rowconfigure(6, weight=1)
        self.root.rowconfigure(8, weight=0)
        self.root.minsize(500,263)
        self.root.columnconfigure(3, weight=1)
        self.root.grab_set()
        self.root.focus_set()
        panel = ttk.Frame(self.root, relief="groove", style="A.TFrame", borderwidth=2)
        panel.grid(row=1, column=0, sticky="nsw", padx=8, rowspan=7)
        self.sel = tk.Frame(panel, bg= "#0078D7", width= 130, height=26)
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
        self.desct = ttk.Labelframe(self.root, style="A.TLabelframe")
        if data["theme"] == "dark":
            self.root["bg"]= "#454545"
            self.cont["bg"]= "#45457c"
        self.desc = ttk.Label(self.desct, style="A.TLabel", justify="left")
        self.desct.grid(row=1, column=1, sticky="nsew", columnspan=5)
        self.foont = ttk.Labelframe(self.root, style="A.TLabelframe")
        self.desc1 = ttk.Label(self.foont, style="A.TLabel", justify="left")
        self.desc.grid(row=1, column=1, sticky="nw", rowspan=3)
        self.desc1.grid(row=5, column=1, sticky="nsew", rowspan=3)
        self.gen.bind("<Button-1>", self.change_tab1)
        self.theme.bind("<Button-1>", self.change_tab2)
        self.info.bind("<Button-1>", self.change_tab3)
        self.rdf = ttk.Button(self.root, text= "Reset to Defaults", style="A.TButton", width=16, command= self.ask)
        self.bok = ttk.Button(self.root, text= "OK", style="A.TButton", width=10, command= self.okb)
        self.bcl = ttk.Button(self.root, text= "Cancel", style="A.TButton", width=10, command= self.ext)
        self.bap = ttk.Button(self.root, text= "Apply", style="A.TButton", width=10, command= self.applyb)
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
        self.onftn = ttk.Checkbutton(self.foont, style="A.TCheckbutton", variable= self.showtn, text= "Show level thumbnails")
        self.onflc = ttk.Checkbutton(self.foont, style="A.TCheckbutton", variable= self.showlc, text= "Show current line/column position")
        self.onstr = ttk.Checkbutton(self.foont, style="A.TCheckbutton", variable= self.sortx, text= "Sort XML values alphabetically")
        self.supp = ttk.Frame(self.foont, style="A.TFrame")
        self.onsyt = ttk.Checkbutton(self.supp, style="A.TCheckbutton", variable= self.sythl, text= "Syntax highlighting:")
        self.warn = ttk.Label(self.foont, font= "{Segoe UI} 8", style="A.TLabel", text= "Warning: Syntax highlighting \"Everything\" will increase\nloading times and scroll lag if used with small font size")
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
        self.txf= ttk.Label(self.foont, style="A.TLabel", anchor= tk.W, text= data["fnt"].translate(str.maketrans({'{': '', '}': ''})), font= data["fnt"])
        self.ctxf= ttk.Button(self.foont, style="A.TButton", text="Change...", command= self.cht)
        self.uxf= ttk.Label(self.foont, style="A.TLabel", anchor= tk.W, text= data["ufnt"].translate(str.maketrans({'{': '', '}': ''})), font= data["ufnt"])
        self.cuxf= ttk.Button(self.foont, style="A.TButton", text="Change...", command= self.chu)
        self.upt= ttk.Button(self.desct, style="A.TButton", text= "Check for updates", command= self.update)
        self.result= ttk.Label(self.desct, style="A.TLabel", text= "...", justify="left")
        self.dwl= tk.Button(self.desct, relief="flat", activeforeground= "#0094FF", fg= "#0094FF", text="(Download)", command= self.browupt)
        root.bind("<FocusIn>", self.focuz)
        self.root.protocol("WM_DELETE_WINDOW", self.ext)
    def ext(self):
        root.unbind("<FocusIn>")
        self.root.grab_release()
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
        self.desc["font"]="{DejaVu Sans} 10"
        self.foont.grid(row=6, column=1, sticky="nsew", columnspan=5)
        self.desc.grid(row=1, column=1, sticky="nw", rowspan=4, columnspan=1)
        self.sel.grid(row= 1)
        self.gen["bg"]= "#BFDDF5"
        self.theme["bg"]= "gray94"
        self.info["bg"]= "gray94"
        wmcx = root.winfo_x() - 2
        wmcy = tk.StringVar()
        wmcy.set(root.winfo_y() - 23)
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
        self.wmw.grid(row=2,column=2, sticky="nw", padx=2, pady=9)
        self.wmh = tk.Entry(self.desct, width=6, textvariable= wmch)
        self.wmh.grid(row=2,column=3, sticky="nw", padx=6, pady=9)
        self.desct.rowconfigure(1, weight=1)
        self.desct.columnconfigure(3, weight=30)
        self.filler= ttk.Label(self.root, style="A.TLabel", text=" ")
        self.filler.grid(row=0, column=6, sticky="ns", rowspan=4)
        self.filler1= ttk.Label(self.root, style="A.TLabel", text=" ", font= "Courier 1")
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
        self.desc1["text"]="   Text font:\n\n\n   UI font:"
        self.themeli.grid(row=1,column=1, sticky="nw", padx=10, columnspan=3)
        self.themedk.grid(row=2,column=1, sticky="nw", padx=10, columnspan=3)
        self.desc1.grid(row=6, column=1, sticky="nw", rowspan=3, columnspan=1)
        self.txf.grid(row=6, column=2, sticky="nw", pady=4, padx=4)
        self.ctxf.grid(row=6, column=3, sticky="ne")
        self.uxf.grid(row=7, column=2, sticky="nw", pady=23, padx=4)
        self.cuxf.grid(row=7, column=3, sticky="ne", pady=19)
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
        self.desc["font"]= "{DejaVu Sans} 9"
        self.desc["text"]="   Version 1.2\n   Made by Grim Stride using Python 3.9.0 and\n   cx-Freeze\n   This is a heavily modified version of Real Python's\n   Tkinter tutorial\n   Text editor functionality based on Notepad++\n   Icons taken from The GNOME Project and material.io"
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
        else:
            tlight()
            data["theme"]= "light"
            self.root["bg"]= "#d9d9d9"
            self.cont["bg"]= "#d9d9d9"
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
        if self.sortx.get() == "0":
            data["sort"] = False
            frmat = UnsortedAttributes()
        else:
            data["sort"] = True
            frmat= None
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
        self.nsuf= "{DejaVu Sans} 10"
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
        self.root.grab_release()
    def font_changed(self, font):
        self.root.grab_set()
        self.nsf = font
        self.txf["font"]= font
        self.txf["text"]= font.translate(str.maketrans({'{': '', '}': ''}))
    def chu(self):
        global data
        self.root.tk.call('tk', 'fontchooser', 'configure', '-font', self.nsuf, '-command', root.register(self.ufont_changed))
        self.root.tk.call('tk', 'fontchooser', 'show')
        self.root.grab_release()
    def ufont_changed(self, font):
        self.root.grab_set()
        self.nsuf = font
        self.uxf["font"]= font
        self.uxf["text"]= font.translate(str.maketrans({'{': '', '}': ''}))
class UnsortedAttributes(bs4.formatter.XMLFormatter):
    def attributes(self, tag):
        for k, v in tag.attrs.items():
            yield k, v

def open_file(mode):
    if mode != "2":
        if mode == "1":
            stype= "rules"
            ftype= (("UCH Compressed Ruleset", "*.ruleset"), ("All Files", "*.*"))
        else:
            stype= "snapshots"
            ftype= (("UCH Compressed Level", "*.v.snapshot *.c.snapshot"), ("UCH Compressed Party Level", "*.v.snapshot"), ("UCH Compressed Challenge Level", "*.c.snapshot"), ("UCH Uncompressed Party Level", "*.v"), ("UCH Uncompressed Challenge Level", "*.c"), ("All Files", "*.*"))
        filepath1 = askopenfilename(
            initialdir=str(Path.home()) + "/.config/unity3d/Clever Endeavour Games/Ultimate Chicken Horse/" + stype, filetypes= ftype)
    else:
        filepath1= os.path.abspath(sys.argv[1]).replace("\\", "/")
    if not filepath1:
        return
    txt_edit.delete("1.0", tk.END)
    extension = os.path.splitext(filepath1)[1]
    if extension == ".snapshot" or extension == ".ruleset":
        with lzma.open(filepath1, "r") as input_file:
            text = input_file.read()
            text1 = BeautifulSoup(text, "xml")
            text2 = text1.prettify(formatter=frmat)
            text3 = text2.replace("<?xml version=\"1.0\" encoding=\"utf-8\"?>" + "\n", "")
            txt_edit.insert(tk.END, text3)
            checksyntax(None)
    else:
        with open(filepath1, "r") as input_file:
            text = input_file.read()
            text1 = BeautifulSoup(text, "xml")
            text2 = text1.prettify(formatter=frmat)
            text3 = text2.replace("<?xml version=\"1.0\" encoding=\"utf-8\"?>" + "\n", "")
            txt_edit.insert(tk.END, text3)
            checksyntax(None)
    global filepath
    filepath = filepath1
    TButton()
    bhash= txt_edit.get(1.0, tk.END)
    global chash
    chash = hashlib.md5(bhash.encode('utf-8')).hexdigest()
    txt_edit.mark_set("insert", "1.0")
    root.title(f"{filepath} - UCH Notepad 1.2")

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
        if extension == ".ruleset" or extension == ".snapshot":
            with lzma.open(filepath, "w", format=lzma.FORMAT_ALONE) as output_file:
                text = txt_edit.get(1.0, tk.END)
                output_file.write(bytes(text, "utf-8"))
        else:
            with open(filepath, "w") as output_file:
                text = txt_edit.get(1.0, tk.END)
                output_file.write(text)
        bhash= txt_edit.get(1.0, tk.END)
        global chash
        chash = hashlib.md5(bhash.encode('utf-8')).hexdigest()
        root.title(f"{filepath} - UCH Notepad 1.2")
    else: save_file()

def save_file():
    global filepath
    itlvl = txt_edit.search("<scene", "1.0", "1.7")
    itrul = txt_edit.search("<Ruleset", "1.0", "1.9")
    if itlvl == "1.0":
        filepaths = asksaveasfilename(
            initialdir= filepath.replace(os.path.basename(filepath),""),
            defaultextension=".v.snapshot",
            filetypes=[("UCH Compressed Party Level", "*.v.snapshot"), ("UCH Compressed Challenge Level", "*.c.snapshot"), ("UCH Uncompressed Party Level", "*.v"), ("UCH Uncompressed Challenge Level", "*.c"), ("All Files", "*.*")],
        )
        if not filepaths:
            return
        extension = os.path.splitext(filepaths)[1]
        if extension == ".snapshot":
            with lzma.open(filepaths, "w", format=lzma.FORMAT_ALONE) as output_file:
                text = txt_edit.get(1.0, tk.END)        
                output_file.write(bytes(text, "utf-8"))
        else:
            with open(filepaths, "w") as output_file:
                text = txt_edit.get(1.0, tk.END)
                output_file.write(text)
    elif itrul == "1.0":
        filepaths = asksaveasfilename(
            initialdir= filepath.replace(os.path.basename(filepath),""),
            defaultextension="v.snapshot",
            filetypes=[("UCH Compressed Ruleset", "*.ruleset"), ("All Files", "*.*")],
        )
        if not filepaths:
            return
        extension = os.path.splitext(filepaths)[1]
        if extension == ".ruleset":
            with lzma.open(filepaths, "w", format=lzma.FORMAT_ALONE) as output_file:
                text = txt_edit.get(1.0, tk.END)        
                output_file.write(bytes(text, "utf-8"))
        else:
            with open(filepaths, "w") as output_file:
                text = txt_edit.get(1.0, tk.END)
                output_file.write(text)
    else:
        filepaths = asksaveasfilename(initialdir= filepath.replace(os.path.basename(filepath),""), defaultextension="lzma", filetypes=[("LZMA Encoded File", "*.lzma"), ("Text File", "*.txt"), ("All Files", "*.*")])
        if not filepaths:
            return
        extension = os.path.splitext(filepaths)[1]
        if extension == ".lzma":
            with lzma.open(filepaths, "w", format=lzma.FORMAT_ALONE) as output_file:
                text = txt_edit.get(1.0, tk.END)        
                output_file.write(bytes(text, "utf-8"))
        else:
            with open(filepaths, "w") as output_file:
                text = txt_edit.get(1.0, tk.END)
                output_file.write(text)
    filepath = filepaths
    bhash= txt_edit.get(1.0, tk.END)
    global chash
    chash = hashlib.md5(bhash.encode('utf-8')).hexdigest()
    root.title(f"{filepath} - UCH Notepad 1.2")

def TButton():
    destroyTN()
    extension = os.path.splitext(filepath)[1]
    global cv
    cv = tk.Button(fr_buttons, bg="black", activebackground="black", highlightthickness=0)
    cv.grid(row=0, column=0, sticky="nsew")
    if extension == ".snapshot" or extension == ".v" or extension == ".c":
        ofile = (Path(filepath).with_suffix('').with_suffix(''))
        clvl = os.path.basename(ofile)
        lvlthumb = str(Path.home()) + "/.config/unity3d/Clever Endeavour Games/Ultimate Chicken Horse/snapshots/thumbnails/" + "l_" + clvl + ".jpg"
        check = os.path.isfile(lvlthumb)
        if check == True and data["shwtn"] == True:
            cv.img = Image.open(lvlthumb)
            cv.res = cv.img.resize((104, 74), Image.ANTIALIAS)
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
        self.lvlthumb = str(Path.home()) + "/.config/unity3d/Clever Endeavour Games/Ultimate Chicken Horse/snapshots/thumbnails/" + "l_" + clvl + ".jpg"
        self.root = tk.Toplevel(parent, bg="white")
        self.root.title(clvl)
        self.root.geometry("512x366")
        self.root.resizable(False,False)
        self.root.focus_set()
        self.root.photo = ImageTk.PhotoImage(file= self.lvlthumb)
        cw = tk.Canvas(self.root, height=512, width=366, bg="black")
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
        cpyim= Image.open(self.lvlthumb)
        output = BytesIO()
        cpyim.save(output, format='png')
        sub = subprocess.Popen(("xclip", "-selection", "clipboard", "-t", "image/png", "-i"), 
                          stdin=subprocess.PIPE)
        sub.stdin.write(output.getvalue())
        sub.stdin.close()
    def save_thmb(self):
        thmbpath = asksaveasfilename(
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
        change["bg"]= "#d9d9d9"
    for change in uif:
        change["fg"]= "black"
    txt_edit.configure(bg="white", fg="black", insertbackground="black", selectbackground= "#c0c0c0", selectforeground= "black")
    btn_conf['activebackground'] = "#d9d9d9"
    s.configure("TSeparator", background= "#d9d9d9")
    s.configure("A.TFrame", background= "white")
    s.configure("A.TButton", background= "#d9d9d9", foreground="black")
    s.map("A.TButton", background=[("active", "#ececec")])
    s.configure("A.TLabel", background= "#d9d9d9", foreground= "black")
    s.configure("A.TLabelframe", background= "#d9d9d9", foreground= "black")
    s.configure("A.TLabelframe.Label", background= "#d9d9d9", foreground= "black")
    s.configure("A.TCheckbutton", background= "#d9d9d9", foreground= "black")
    s.map("A.TCheckbutton", background=[("active", "#ececec")])
    s.configure("TRadiobutton", background= "#d9d9d9", foreground= "black")
    s.map("TRadiobutton", background=[("active", "#ececec")])
    s.configure("A.Vertical.TScrollbar", troughcolor="#c3c3c3", background="#d9d9d9", arrowcolor="black")
    s.configure("A.Horizontal.TScrollbar", troughcolor="#c3c3c3", background="#d9d9d9", arrowcolor="black")
    s.map("A.Vertical.TScrollbar", background=[("active", "#ececec")])
    s.map("A.Horizontal.TScrollbar", background=[("active", "#ececec")])
def tdark():
    for change in wmcol:
        change["bg"]= "#242424"
    for change in uif:
        change["fg"]= "#dedede"
    txt_edit.configure(bg="#2e2e2e", fg="#dedede", insertbackground="#dedede", selectbackground= "#4d5d60", selectforeground= "#e2e2e2", highlightbackground= "#454545")
    btn_conf['activebackground'] = "#2e2e2e"
    s.configure("TSeparator", background= "black")
    s.configure("A.TFrame", background= "#323232")
    s.configure("A.TButton", background= "#555555", foreground="#dedede")
    s.map("A.TButton", background=[("active", "#757575")])
    s.configure("A.TLabel", background= "#454545", foreground= "#dedede")
    s.configure("A.TLabelframe", background= "#454545", foreground= "#dedede")
    s.configure("A.TLabelframe.Label", background= "#454545", foreground= "#dedede")
    s.configure("A.TCheckbutton", background= "#454545", foreground= "#dedede")
    s.map("A.TCheckbutton", background=[("active", "#555555")])
    s.configure("TRadiobutton", background= "#454545", foreground= "#dedede")
    s.map("TRadiobutton", background=[("active", "#555555")])
    s.configure("A.Vertical.TScrollbar", troughcolor="#242424", background="#6a6a6a", arrowcolor="#dedede")
    s.configure("A.Horizontal.TScrollbar", troughcolor="#242424", background="#6a6a6a", arrowcolor="#dedede")
    s.map("A.Vertical.TScrollbar", background=[("active", "#757575")])
    s.map("A.Horizontal.TScrollbar", background=[("active", "#757575")])

def get_line1():
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
            root.title(f"*{filepath} - UCH Notepad 1.2")
            unsaved= True
        else:
            root.title(f"*UCH Notepad 1.2")
            unsaved= True
    else:
        if chash != "68b329da9893e34099c7d8ad5cb9c940":
            root.title(f"{filepath} - UCH Notepad 1.2")
            unsaved= False
        else:
            root.title(f"UCH Notepad 1.2")
            unsaved= False
    try:
        txt_edit.tag_delete("curr1", "1.0", "end")
        txt_edit.tag_delete("curr2", "1.0", "end")
    except NameError: pass
    if data["theme"] == "dark":
        selc= "#4d5d60"
        curc= "#394447"
    else:
        selc= "#c0c0c0"
        curc= "#e8e8ff"
    txt_edit.tag_add("curr1", "insert linestart", "insert")
    txt_edit.tag_add("curr2", "insert", "insert lineend")
    txt_edit.tag_configure("curr1", selectbackground= selc, background= curc)
    txt_edit.tag_configure("curr2", selectbackground= selc, background= curc)
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
if data["sort"] == False: frmat = UnsortedAttributes()
else: frmat = None
root = tk.Tk()
root.title("UCH Notepad 1.2")
ww= data["wm"].split("+")[0]
wx= int(data["wm"].split("+")[1]) - 2
wy= int(data["wm"].split("+")[2]) - 23
root.geometry(ww + "+" + str(wx) + "+" + str(wy))
root.minsize(200,270)
if data["state"] == 1:
    root.attributes('-zoomed', True)
iicon=tk.PhotoImage(file="icon.png")
root.tk.call("wm", "iconphoto", root._w, iicon)
root.rowconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.protocol("WM_DELETE_WINDOW", winquit)

s = ttk.Style()
s.theme_use("default")
s.configure("TButton", font= data["ufnt"])

scroll = ttk.Scrollbar(root, orient="vertical", style="A.Vertical.TScrollbar")
xascroll = ttk.Scrollbar(root, orient="horizontal", style="A.Horizontal.TScrollbar")
txt_edit = tk.Text(root, padx=4, undo=True, autoseparators=True, font= data["fnt"], wrap="none", xscrollcommand= xascroll.set, yscrollcommand=scroll.set)

scroll.config(command=y_scroll)
xascroll.config(command=x_scroll)

fr_buttons = tk.Frame(root)
btn_open = ttk.Button(fr_buttons, text="Open Level", style="A.TButton", command= lambda:[open_file("0")])
btn_orul = ttk.Button(fr_buttons, text="Open Ruleset", style="A.TButton", command= lambda:[open_file("1")])
btn_nsav = ttk.Button(fr_buttons, text="Save", style="A.TButton", command=nsave)
btn_save = ttk.Button(fr_buttons, text="Save As...", style="A.TButton", command=save_file)
btn_open.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
btn_orul.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
btn_nsav.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
fr_buttons.grid(row=0, column=0, sticky="ns")

txt_edit.grid(row=0, column=1, sticky="nsew")

scroll.grid(column=2, row=0, sticky="nsw")
xascroll.grid(column=1, row=1, sticky="we")

statusbar = tk.Label(root, text=" By Grim Stride", anchor=tk.W, bd=0, relief="solid")
sepfr = tk.Frame(root)
sep = ttk.Separator(sepfr, orient="horizontal")
sepfr.grid(row=5, column=0, sticky="ew", columnspan=30)
statusbar.grid(row=6, column=0, sticky="sew", columnspan=2, pady=4)

conb = tk.Frame(root)
conf = "R0lGODlhEAASANUAAP////7+/v39/fj4+PT09PHx8ZKSkomJiX9/f319fXt7e3BwcG5ubmJiYmFhYWBgYF9fX1JSUlFRUUVFRUNDQyYmJiIiIhoaGhcXFxQUFBEREQ0NDQoKCgkJCQgICAAAAP///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAACAALAAAAAAQABIAAAZxQJAQBCgOj8OiAOKhFIpQIwDxqVqvVUTRYLlYM5aw2AAgFhOVxiAKRbaRcPg7yQYQJBhGQHrQ+P8cVhsaB0V9f36BVYOFZmwEERgLe2VxQnNuRpaOChUPa3VEXF5VYGJhZFNYqx9aZgIOHRNPoUeYSEEAOw=="
confshw = tk.PhotoImage(data=conf)
btn_conf = tk.Button(conb, image= confshw, relief="flat", command=config, bd=0, highlightthickness=0)
btn_conf.grid(row=6, column=2, sticky="ew")
conb.grid(row=6, column=2, sticky="e")

root.update()
sep.grid(row=5, column=0, sticky="ew", columnspan=1, ipadx= root.winfo_reqwidth())
txpos = tk.Label(root, width= 15, anchor="center", bd=0, relief="solid")
txpos.grid(row=6, column=1, sticky="e")

scroll.bind("<ButtonRelease-1>", scrllstop)
xascroll.bind("<ButtonRelease-1>", scrllstop)
txt_edit.bind("<ButtonRelease-1>", scrllstop)
txt_edit.bind("<KeyRelease>", checksyntax)
txt_edit.bind("<KeyRelease-Control_L>", checksyntax)
txt_edit.bind("<KeyRelease-Control_R>", checksyntax)

wmcol = (root, fr_buttons, sepfr, txpos, statusbar, btn_conf)
uif = (txpos, statusbar)
buttons = (btn_open, btn_orul, btn_nsav, btn_save)
if data["theme"] == "dark": tdark()
else: tlight()
if len(sys.argv) >= 2:
    open_file("2")
else: pass
root.after(5, get_line1)

root.mainloop()
