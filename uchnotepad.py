import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import ttk, font, messagebox
import lzma, pathlib, PIL, bs4, os, win32clipboard, hashlib, json, sys, requests, webbrowser
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import ImageTk, Image, ImageGrab
from io import BytesIO

shldiscr= 1
check = 0
chash = "68b329da9893e34099c7d8ad5cb9c940"
filepath= ""
unsaved= False
frmat = None
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
    try:
        a= data["sort"]
    except KeyError:
        data["sort"]= False
class config():
    def __init__(self):
        global data
        self.root = tk.Toplevel(root)
        self.root.title("Settings")
        scy = int(((root.winfo_y() + (root.winfo_height()/2) - 132)**2)**0.5)
        scx = int(root.winfo_x() + (root.winfo_width()/2) - 250)
        self.root.geometry("+" + str(scx) + "+" + str(scy))
        self.root.transient(root)
        self.root.iconbitmap(os.path.join(sys.path[0], 'icon.ico'))
        self.root.rowconfigure(8, weight=1)
        self.root.minsize(500,263)
        self.root.columnconfigure(3, weight=1)
        root.attributes('-disabled', True)
        self.root.focus_set()
        panel = ttk.Frame(self.root, relief="groove", borderwidth=2)
        panel.grid(row=0, column=0, sticky="ns", padx=8, pady=8, rowspan=5)
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
        self.desct = tk.Label(self.root, pady=6, justify="left")
        self.cont = tk.Frame(self.root)
        if data["theme"] == "dark":
            self.root["bg"]= "#454545"
            self.cont["bg"]= "#454545"
            self.desct.configure(bg="#454545", fg= "white")
        self.desc = ttk.Label(self.cont, justify="left")
        self.desct.grid(row=0, column=1, sticky="nw", columnspan=9)
        self.foont = ttk.Label(self.cont)
        self.cont.grid(row=1, column=1, sticky="nw", columnspan=9, rowspan=4)
        self.desc.grid(row=1, column=1, sticky="nw", rowspan=3)
        self.change_tab1(None)
        self.gen.bind("<Button-1>", self.change_tab1)
        self.theme.bind("<Button-1>", self.change_tab2)
        self.info.bind("<Button-1>", self.change_tab3)
        self.rdf = ttk.Button(self.root, text= "Reset to Defaults", width=16, command= self.ask)
        self.bok = ttk.Button(self.root, text= "OK", width=10, command= self.okb)
        self.bcl = ttk.Button(self.root, text= "Cancel", width=10, command= self.ext)
        self.bap = ttk.Button(self.root, text= "Apply", width=10, command= self.applyb)
        self.rdf.grid(row=8, column=0, sticky="sw", padx=8, pady=8)
        self.bok.grid(row=8, column=6, sticky="se", padx=8, pady=8)
        self.bcl.grid(row=8, column=7, sticky="se", pady=8)
        self.bap.grid(row=8, column=8, sticky="se", padx=8, pady=8)
        self.crtf = tk.StringVar()
        self.cruf = tk.StringVar()
        self.crtf.set(data["fnt"])
        self.cruf.set(data["ufnt"])
        self.nsf= data["fnt"]
        self.nsuf= data["ufnt"]
        self.currenttheme= tk.StringVar()
        self.themeli= ttk.Radiobutton(self.cont, text="Light Theme", variable=self.currenttheme, value= "light")
        self.themedk= ttk.Radiobutton(self.cont, text="Dark Theme", variable=self.currenttheme, value= "dark")
        self.currenttheme.set(data["theme"])
        self.txf= ttk.Label(self.cont, anchor= tk.W, text= data["fnt"].translate(str.maketrans({'{': '', '}': ''})), font= data["fnt"])
        self.ctxf= ttk.Button(self.cont, text="Change...", command= self.cht)
        self.uxf= ttk.Label(self.cont, anchor= tk.W, text= data["ufnt"].translate(str.maketrans({'{': '', '}': ''})), font= data["ufnt"])
        self.cuxf= ttk.Button(self.cont, text="Change...", command= self.chu)
        self.upt= ttk.Button(self.cont, text= "Check for updates", command= self.update)
        self.result= ttk.Label(self.cont, text= "...", justify="left")
        self.dwl= tk.Button(self.cont, relief="flat", activeforeground= "#0094FF", fg= "#0094FF", text="(Download)", command= self.browupt)
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
        for widgets in self.cont.winfo_children():
            widgets.grid_remove()
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
        self.desct["text"]="Window╶──────────────────────╸"
        self.desc["text"]="   Window position (X,Y):\n\n   Window size (W, H):"
        self.foont["text"]="Options╶──────────────────────╸"
        self.foont.grid(row=5, column=1, sticky="w", columnspan=9)
        self.showtn= tk.StringVar()
        self.showlc= tk.StringVar()
        self.sortx= tk.StringVar()
        self.showtn.set(data["shwtn"])
        self.showlc.set(data["shwlc"])
        self.sortx.set(data["sort"])
        self.onftn = ttk.Checkbutton(self.cont, variable= self.showtn, text= "Show level thumbnails")
        self.onflc = ttk.Checkbutton(self.cont, variable= self.showlc, text= "Show current line/column position")
        self.onstr = ttk.Checkbutton(self.cont, variable= self.sortx, text= "Sort XML values alphabetically")
        self.onftn.grid(row=6, column=1, sticky="w", padx=10, columnspan=9)
        self.onflc.grid(row=7, column=1, sticky="w", padx=10, columnspan=9)
        self.onstr.grid(row=8, column=1, sticky="w", padx=10, columnspan=9)
        self.wmx = tk.Entry(self.cont, width=6)
        self.wmx.insert(10, wmcx)
        self.wmx.grid(row=1,column=2, sticky="nw", padx=2)
        self.wmy = tk.Entry(self.cont, width=6, textvariable= wmcy)
        self.wmy.grid(row=1,column=3, sticky="nw", padx=6)
        self.wmw = tk.Entry(self.cont, width=6, textvariable= wmcw)
        self.wmw.grid(row=2,column=2, sticky="nw", padx=2, pady=11)
        self.wmh = tk.Entry(self.cont, width=6, textvariable= wmch)
        self.wmh.grid(row=2,column=3, sticky="nw", padx=6, pady=11)
        self.filler= ttk.Label(self.cont, text= "\n\n")
        self.filler.grid(row=9, column=1, ipady=0)
    def change_tab2(self, event):
        for widgets in self.cont.winfo_children():
            widgets.grid_remove()
        self.sel.grid(row= 2)
        self.theme["bg"]= "#BFDDF5"
        self.gen["bg"]= "gray94"
        self.info["bg"]= "gray94"
        self.desct["text"]="Theme╶───────────────────────╸"
        self.desc["text"]="   Text font:\n\n   UI font:"
        self.themeli.grid(row=1,column=1, sticky="nw", padx=10, columnspan=3)
        self.themedk.grid(row=2,column=1, sticky="nw", padx=10, columnspan=3)
        self.desc.grid(row=6, column=1, sticky="nw", rowspan=3, columnspan=1)
        self.txf.grid(row=6, column=2, sticky="nw")
        self.ctxf.grid(row=6, column=3, sticky="ne")
        self.uxf.grid(row=7, column=2, sticky="nw", pady=5)
        self.cuxf.grid(row=7, column=3, sticky="ne", pady=5)
        self.foont["text"]="Font╶────────────────────────╸"
        self.foont.grid(row=5, column=1, sticky="w", columnspan=15)
        self.filler.grid(row=8, column=1, ipady=10)
    def change_tab3(self, event):
        for widgets in self.cont.winfo_children():
            widgets.grid_remove()
        self.desc.grid(row=3, column=1, sticky="nw", rowspan=4, columnspan=9)
        self.sel.grid(row= 3)
        self.info["bg"]= "#BFDDF5"
        self.gen["bg"]= "gray94"
        self.theme["bg"]= "gray94"
        self.desct["text"]="About UCH Notepad╶─────────────────╸"
        self.desc["text"]="   Version 1.1\n   Made by Grim Stride using Python 3.9.0 and cx-Freeze\n   This is a heavily modified version of Real Python's Tkinter\n   tutorial\n   Icons taken from The GNOME Project and material.io"
        self.upt.grid(row=7, column=1, sticky="nw", padx=8, pady=8)
        self.result.grid(row=7, column=2)
        self.filler.grid(row=8, column=1, ipady=11)
    def update(self):
        try:
            r = requests.get("https://github.com/GrimStride/UCH-Notepad/releases/latest")
            e = r.url.replace("https:/", "")
            d = os.path.basename(e)
            if d > str(1.1):
                self.result["text"]= "Version " + d + " is available"
                self.dwl.configure(bg= self.root["bg"], activebackground= self.root["bg"])
                self.dwl.grid(row=7, column=3, pady=3)
            else: self.result["text"]= "No updates are available"
        except requests.ConnectionError: self.result["text"]= "No internet connection"
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
        x = self.wmx.get()
        y = self.wmy.get()
        w = self.wmw.get()
        h = self.wmh.get()
        a = root.geometry(str(w) + "x" + str(h) + "+" + str(x) + "+" + str(y))
        if self.currenttheme.get() == "dark":
            tdark()
            data["theme"]= "dark"
            self.root["bg"]= "#454545"
            self.cont["bg"]= "#454545"
            self.desct.configure(bg="#454545", fg= "white")
        else:
            tlight()
            data["theme"]= "light"
            self.root["bg"]= "#f0f0f0"
            self.cont["bg"]= "#f0f0f0"
            self.desct.configure(bg="#f0f0f0", fg= "black")
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
class UnsortedAttributes(bs4.formatter.XMLFormatter):
    def attributes(self, tag):
        for k, v in tag.attrs.items():
            yield k, v

def open_file():
    filepath1 = askopenfilename(
        initialdir=str(Path.home()) + "/AppData/LocalLow/Clever Endeavour Games/Ultimate Chicken Horse/snapshots",filetypes=(("UCH Compressed Level", "*.v.snapshot *.c.snapshot"), ("UCH Compressed Party Level", "*.v.snapshot"), ("UCH Compressed Challenge Level", "*.c.snapshot"), ("UCH Uncompressed Party Level", "*.v"), ("UCH Uncompressed Challenge Level", "*.c"), ("All Files", "*.*")))
    if not filepath1:
        return
    txt_edit.delete("1.0", tk.END)
    extension = os.path.splitext(filepath1)[1]
    if extension == ".snapshot":
        with lzma.open(filepath1, "r") as input_file:
            text = input_file.read()
            text1 = BeautifulSoup(text, "xml")
            text2 = text1.prettify(formatter=frmat)
            text3 = text2.replace("<?xml version=\"1.0\" encoding=\"utf-8\"?>" + "\n", "")
            txt_edit.insert(tk.END, text3)
    else:
        with open(filepath1, "r") as input_file:
            text = input_file.read()
            text1 = BeautifulSoup(text, "xml")
            text2 = text1.prettify(formatter=frmat)
            text3 = text2.replace("<?xml version=\"1.0\" encoding=\"utf-8\"?>" + "\n", "")
            txt_edit.insert(tk.END, text3)
    global filepath
    filepath = filepath1
    TButton()
    bhash= txt_edit.get(1.0, tk.END)
    global chash
    chash = hashlib.md5(bhash.encode('utf-8')).hexdigest()
    txt_edit.mark_set("insert", "1.0")
    root.title(f"{filepath} - UCH Notepad 1.1")

def open_rule():
    filepath1 = askopenfilename(
        initialdir=str(Path.home()) + "/AppData/LocalLow/Clever Endeavour Games/Ultimate Chicken Horse/rules",filetypes=(("UCH Compressed Ruleset", "*.ruleset"), ("All Files", "*.*")))
    if not filepath1:
        return
    txt_edit.delete("1.0", tk.END)
    extension = os.path.splitext(filepath1)[1]
    if extension == ".ruleset":
        with lzma.open(filepath1, "r") as input_file:
            text = input_file.read()
            text1 = BeautifulSoup(text, "xml")
            text2 = text1.prettify(formatter=frmat)
            text3 = text2.replace("<?xml version=\"1.0\" encoding=\"utf-8\"?>" + "\n", "")
            txt_edit.insert(tk.END, text3)
    else:
        with open(filepath1, "r") as input_file:
            text = input_file.read()
            text1 = BeautifulSoup(text, "xml")
            text2 = text1.prettify(formatter=frmat)
            text3 = text2.replace("<?xml version=\"1.0\" encoding=\"utf-8\"?>" + "\n", "")
            txt_edit.insert(tk.END, text3)
    global filepath
    filepath = filepath1
    bhash= txt_edit.get(1.0, tk.END)
    global chash
    chash = hashlib.md5(bhash.encode('utf-8')).hexdigest()
    root.title(f"{filepath} - UCH Notepad 1.1")
    txt_edit.mark_set("insert", "1.0")
    destroyTN()

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
        root.title(f"{filepath} - UCH Notepad 1.1")
    else: save_file()

def save_file():
    itlvl = txt_edit.search("<scene", "1.0", "1.7")
    itrul = txt_edit.search("<Ruleset", "1.0", "1.9")
    if itlvl == "1.0":
        filepaths = asksaveasfilename(
            defaultextension="v.snapshot",
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
        filepaths = asksaveasfilename(defaultextension="lzma", filetypes=[("LZMA Encoded File", "*.lzma"), ("Text File", "*.txt"), ("All Files", "*.*")])
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
    global filepath
    filepath = filepaths
    bhash= txt_edit.get(1.0, tk.END)
    global chash
    chash = hashlib.md5(bhash.encode('utf-8')).hexdigest()
    root.title(f"{filepath} - UCH Notepad 1.1")

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
        self.root.iconbitmap(os.path.join(sys.path[0], 'icon.ico'))
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
        change["bg"]= "#f0f0f0"
    for change in uif:
        change["fg"]= "black"
    txt_edit["bg"]="white"
    txt_edit["fg"]="black"
    txt_edit["insertbackground"]="black"
    btn_conf['activebackground'] = "#f0f0f0"
    s.configure("TSeparator", background= "#f0f0f0")
    s.configure("TFrame", background= "white")
    s.configure("TLabel", background= "#f0f0f0", foreground= "black")
    s.configure("TCheckbutton", background= "#f0f0f0", foreground= "black")
    s.configure("TRadiobutton", background= "#f0f0f0", foreground= "black")
def tdark():
    for change in wmcol:
        change["bg"]= "#2a2a2a"
    for change in uif:
        change["fg"]= "white"
    txt_edit["bg"]="#323232"
    txt_edit["fg"]="#f0f0f0"
    txt_edit["insertbackground"]="#f0f0f0"
    btn_conf['activebackground'] = "#2a2a2a"
    s.configure("TSeparator", background= "black")
    s.configure("TFrame", background= "#323232")
    s.configure("TLabel", background= "#454545", foreground= "white")
    s.configure("TCheckbutton", background= "#454545", foreground= "white")
    s.configure("TRadiobutton", background= "#454545", foreground= "white")

def get_line1():
    ln, col = txt_edit.index("insert").split(".")
    coll= int(float(col) + 1)
    global txpos
    global chash
    global filepath
    global unsaved
    if data["shwlc"] == True:
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
            root.title(f"*{filepath} - UCH Notepad 1.1")
            unsaved= True
        else:
            root.title(f"*UCH Notepad 1.1")
            unsaved= True
    else:
        if chash != "68b329da9893e34099c7d8ad5cb9c940":
            root.title(f"{filepath} - UCH Notepad 1.1")
            unsaved= False
        else:
            root.title(f"UCH Notepad 1.1")
            unsaved= False
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
root.title("UCH Notepad 1.1")
root.geometry(data["wm"])
root.minsize(200,270)
root.state(data["state"])
root.iconbitmap(os.path.join(sys.path[0], 'icon.ico'))
root.rowconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.protocol("WM_DELETE_WINDOW", winquit)

s = ttk.Style()
s.theme_use("vista")
s.configure("TButton", font= data["ufnt"])

scroll = ttk.Scrollbar(root, orient="vertical")
xascroll = ttk.Scrollbar(root, orient="horizontal")
txt_edit = tk.Text(root, padx=4, undo=True, autoseparators=True, maxundo=25, font= data["fnt"], wrap="none", xscrollcommand= xascroll.set, yscrollcommand=scroll.set)
scroll.config(command=y_scroll)
xascroll.config(command=x_scroll)

fr_buttons = tk.Frame(root)
btn_open = ttk.Button(fr_buttons, text="Open Level", command=open_file)
btn_orul = ttk.Button(fr_buttons, text="Open Ruleset", command=open_rule)
btn_nsav = ttk.Button(fr_buttons, text="Save", command=nsave)
btn_save = ttk.Button(fr_buttons, text="Save As...", command=save_file)
btn_open.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
btn_orul.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
btn_nsav.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
fr_buttons.grid(row=0, column=0, sticky="ns")

txt_edit.grid(row=0, column=1, sticky="nsew")

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

wmcol = (root, fr_buttons, sepfr, txpos, statusbar, btn_conf)
uif = (txpos, statusbar)
buttons = (btn_open, btn_orul, btn_nsav, btn_save)
if data["theme"] == "dark": tdark()
else: tlight()
root.after(5, get_line1)

root.mainloop()
