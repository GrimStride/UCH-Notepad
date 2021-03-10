package require Tk
package require archive
package require tdom
#package require extrafont
package require md5


#extrafont::load res/custom1.ttf
set filepath ""
set chash "68B329DA9893E34099C7D8AD5CB9C940"

# Settings - - - - - - - -

proc config {} {
    toplevel .cfg
    wm transient .cfg .
    wm title .cfg "Settings"
    wm iconbitmap .cfg icon.ico
    #wm transient .cfg .
    focus .cfg
    wm attributes . -disabled true
    wm protocol .cfg WM_DELETE_WINDOW "cfgclose"
    grid columnconfigure .cfg 1 -weight 1
    grid rowconfigure .cfg 0 -weight 1
    grid [ttk::frame .cfg.panel -relief "groove" -borderwidth 2] -column 0 -row 0 -sticky nsw -padx 8 -pady 8
    grid [label .cfg.panel.gen -text "  General" -width 114 -relief "flat" -anchor w -pady 2 -compound "left" -image [image create photo genshw -format GIF -data {R0lGODlhEgASANUAAP////7+/vv7+/r6+vn5+fj4+Pb29vX19e7u7urq6ufn597e3tra2tnZ2djY2NfX19PT08zMzLy8vKurq6qqqqmpqZ+fn52dnZycnJubm5aWlpGRkYKCgoGBgXV1dW5ubmxsbGVlZV5eXlxcXFhYWFRUVFNTU09PT01NTUdHR0FBQTg4ODExMSwsLCcnJyUlJSMjIxoaGhQUFBMTExISEgQEBAEBAQAAAP///wAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAADgALAAAAAASABIAAAaqQBwOQBwSaCyTJwIQOocDIuBxq94ozScg4boADhzrDZIVAgSqKoomvnmlxE973gEsLADDat62vaoMAAUhYiQSEy1zG0QOVidSCDJtKQABGVYVTUQjYjEgIDFiGnApVhgBAKViMApEEjVWDUQbczIiJbBWIQUADFUvNnxiKwYAFgsAHcJWH3BEF20zKFUqAmVDEGIcxRcuCddDFGIPUlFPZhEeJiw0BJpFOEEAOw==}]] -column 0 -row 0 -sticky ew -padx 3 -pady 3
    grid [label .cfg.panel.theme -text "  Appearance" -width 114 -relief "flat" -anchor w -pady 2 -compound "left" -image [image create photo them -format GIF -data {R0lGODlhEgASAOYAAP////7+/vz8/Pv7+/n5+fb29vX19fT09PHx8ezs7Ojo6OXl5ePj4+Dg4N/f39vb29TU1NDQ0M7Ozs3NzcnJycbGxsPDw8HBwcDAwL+/v7u7u7q6ura2trGxsbCwsKmpqaioqKSkpJiYmJaWlpSUlJCQkI2NjYiIiIeHh4aGhoWFhXp6enl5eXd3d3FxcXBwcGpqamhoaGZmZmRkZF1dXVxcXFtbW1dXV0pKSkZGRkVFRUBAQD09PS8vLy0tLSYmJiUlJSQkJCMjIxcXFxUVFRMTExISEg8PDwwMDAsLCwgICAcHBwYGBgUFBQQEBAMDAwICAgAAAP///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAFIALAAAAAASABIAAAergFKCg4SFhACIhopSAA4yFwCLhQAvUUUJkZKCABlRUTOZmow3UVAVkYihkwxIUT4DABs1HaqHJ54pNJ5NELWbBD9RT57CIL6IGELEUTpDK74FNstBGgAYTR6pqB/ESioEqShGJiEkFIgPTK4NqQUWASpOUUoiqCMsSxMABxICMD1HiLRYEAqRDCEICOTokQRICQOJDhXwsQMHFB4cAvgaBEBBDBcRImrSJikQADs=}]] -column 0 -row 2 -sticky ew -padx 3 -pady 3
    grid [label .cfg.panel.info -text "  About" -width 114 -relief "flat" -anchor w -pady 2 -compound "left" -image [image create photo inf -format GIF -data {R0lGODlhEgASAMQAAP////z8/Pn5+fj4+PDw8O3t7evr6+rq6qOjo5OTk5CQkI2NjWBgYFpaWllZWVhYWAYGBgUFBQAAAP///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAABMALAAAAAASABIAAAVz4CSOQGmOKGkOgwmkYnk8kSRFz1Gm5WL/P8UuBvD9Fkab8DUBHICSQACqawIeUAYD2nDVoGDICkwggFuAAVgKFpi+PzZQbMIC5b/uC2CA4m0GTCUKQAgIQAlDVoRgEolMKgYOEDYQDQWKKC4sLjCaLpAjIQA7}]] -column 0 -row 3 -sticky ew -padx 3 -pady 3
    grid [frame .cfg.cont -bg "white"] -column 1 -row 0 -sticky nsew -pady 7 -padx {0 8}
    grid [ttk::labelframe .cfg.cont.box1] -column 0 -row 0 -sticky nsew
    grid columnconfigure .cfg.cont 0 -weight 1
    # General Tab
    ttk::label .cfg.cont.box1.wmp -justify left
    ttk::label .cfg.cont.box1.wms -justify left
    entry .cfg.cont.box1.wmx -width 6
    entry .cfg.cont.box1.wmy -width 6
    .cfg.cont.box1.wmx insert 10 [winfo x .]
    .cfg.cont.box1.wmy insert 10 [winfo y .]
    entry .cfg.cont.box1.wmw -width 6
    entry .cfg.cont.box1.wmh -width 6
    .cfg.cont.box1.wmw insert 10 [winfo width .]
    .cfg.cont.box1.wmh insert 10 [winfo height .]
    ##
    
    #Load first tab
    change_tab1
}

proc cfgclose {} {
    wm attributes . -disabled false
    destroy .cfg
}

proc change_tab1 {} {
    .cfg.cont.box1 configure -text " Window"
    .cfg.cont.box1.wmp configure -text "Window position (X,Y):"
    grid .cfg.cont.box1.wmp -column 0 -row 0 -sticky w  -padx {12 0}
    grid .cfg.cont.box1.wmx -column 1 -row 0 -padx 8
    grid .cfg.cont.box1.wmy -column 2 -row 0 -padx {0 8}
    .cfg.cont.box1.wms configure -text "Window size (W, H):"
    grid .cfg.cont.box1.wms -column 0 -row 1 -sticky w -padx {12 0} -pady 8
    grid .cfg.cont.box1.wmw -column 1 -row 1 -pady 8
    grid .cfg.cont.box1.wmh -column 2 -row 1 -sticky w -pady 8
}

# File Handling - - - - - -

proc open_file {mode} {
    #global env
    if { $mode != 2 } {
        if { $mode == 1 } {
            set stype "rules"
            set ftype {
                {{UCH Compressed Ruleset} {.ruleset}}
                {{All Files} *}
            }
        } else {
            set stype "snapshots"
            set ftype {
                {{UCH Compressed Level} {.v.snapshot .c.snapshot}}
                {{UCH Compressed Party Level} {.v.snapshot}}
                {{UCH Compressed Challenge Level} {.c.snapshot}}
                {{UCH Uncompressed Party Level} {.v}}
                {{UCH Uncompressed Challenge Level} {.c}}
                {{All Files} *}
            }
        }
        set filename [tk_getOpenFile -initialdir "$::env(USERPROFILE)\\AppData\\LocalLow\\Clever Endeavour Games\\Ultimate Chicken Horse\\$stype" -filetypes $ftype]
    } else {
        if { [file exists [lindex $argv 0]] == 1 } { set filename [lindex $argv 0] }
    }
    if { $filename == "" } { return }
    .base.txt_edit delete 1.0 end
    set extension [file extension $filename]
    if { $extension ==  ".snapshot" || $extension == ".ruleset"} { 
        set result [exec xz -d -c $filename]
        set result2 [xmlpretty $result]
        .base.txt_edit insert 0.0 $result2
    } else {
        set opn [open $filename r]
        set text [read $opn]
        .base.txt_edit insert 0.0 $text
        close $opn
    }
    .base.txt_edit mark set "insert" 1.0
    global filepath
    global chash
    set filepath $filename
    set chash [::md5::md5 -hex [.base.txt_edit get 1.0 end]]
    checkmod
    wm title . "$filepath - UCH Notepad TCL beta"
}

proc nsave {} {
    global filepath
    global chash
    if { $filepath != "" } {
        set check 0
        set extension [file extension $filepath]
        set savename [file rootname [file tail $filepath]]
        set dummy [file nativename [file dirname $filepath]]
        if { $extension == ".ruleset" || $extension == ".snapshot" || $extension == ".lzma" } {
            if { [file exists "$dummy\\$savename"] == 1 } {
                file rename "$dummy\\$savename" "$dummy\\${savename}bak"
                set check 1
            }
            set opn [open "$dummy\\$savename" w]
            puts $opn [.base.txt_edit get 1.0 end]
            close $opn
            exec xz -z -f --format=lzma --suffix=$extension "$dummy\\$savename"
            file delete "$dummy\\$savename"
            if { $check == 1 } {
                file rename "$dummy\\${savename}bak" "$dummy\\$savename"
            }
        } else {
            set opn [open $filepath w]
            puts $opn [.base.txt_edit get 1.0 end]
            close $opn
        }
        set chash [::md5::md5 -hex [.base.txt_edit get 1.0 end]]
        checkmod
    } else { save_file }
    #wm title . "$filepath - UCH Notepad TCL beta"
}

proc save_file {} {
    global filepath
    #set known {.snapshot .ruleset .lzma}
    set itlvl [.base.txt_edit search "<scene" 1.0 1.7]
    set itrul [.base.txt_edit search "<Ruleset" 1.0 1.9]
    if { $itlvl == 1.0 } {
        set ext "v.snapshot"
        set ftype {
            {{UCH Compressed Party Level} {.v.snapshot}}
            {{UCH Compressed Challenge Level} {.c.snapshot}}
            {{UCH Uncompressed Party Level} {.v}}
            {{UCH Uncompressed Challenge Level} {.c}}
            {{All Files} *}
        }
    } elseif { $itrul == 1.0 } {
        set ext "ruleset"
        set ftype {
            {{UCH Compressed Ruleset} {.ruleset}}
            {{All Files} *}
        }
    } else {
        set ext "lzma"
        set ftype {
            {{LZMA Encoded File} {.lzma}}
            {{Text File} {.txt}}
            {{All Files} *}
        }
    }
    set filename [tk_getSaveFile -initialdir [file nativename [file dirname $filepath]] -defaultextension $ext -filetypes $ftype]
    if { $filename == "" } { return }
    set filepath [file nativename $filename]
    nsave
    wm title . "$filepath - UCH Notepad TCL beta"
}

# text procedures - - - -

proc xmlpretty xml { [[dom parse $xml doc] documentElement] asXML -indent 2}

proc checkmod {} {
    #puts "asdf"
    if { [.base.txt_edit edit modified] == 0 } { return }
    global chash
    global unsaved
    set current [::md5::md5 -hex [.base.txt_edit get 1.0 end]]
    #if { $current != $chash} {
    #    wm title . "*[string trim "[wm title .]" "*"]"
    #    set unsaved true
    #} else {
    #    wm title . [string trim "[wm title .]" "*"]
    #    set unsaved false
    #}
    #puts $chash
    if { $current == $chash} {
        wm title . [string trim "[wm title .]" "*"]
        .base.txt_edit edit modified 0
    }
}

proc getline:set var {
    #.sepfr.txpos configure -text [.base.txt_edit index "insert"]
    #if {![winfo exists .base.txt_edit]} { return }
    global $var
    set x [split [.base.txt_edit index "insert"] .]
    set a [lindex $x 0]
    set b [expr [lindex $x 1]+1]
    set $var "Ln: ${a} Col: ${b}"
    #.sepfr.txpos configure -text [.base.txt_edit index "insert"]
    after 33 [list getline:set $var]
}

# Main UI - - -

wm title . "UCH Notepad TCL beta"
wm iconbitmap . icon.ico
wm minsize . 200 270

grid [frame .fr_buttons] -column 0 -row 0 -sticky ns
grid [ttk::button .fr_buttons.btn_open -text "Open Level" -command "open_file {0}"] -column 0 -row 1 -sticky ew -padx 5 -pady 5
grid [ttk::button .fr_buttons.btn_orul -text "Open Ruleset" -command "open_file {1}"] -column 0 -row 2 -sticky ew -padx 5 -pady 5
grid [ttk::button .fr_buttons.btn_nsav -text "Save" -command "nsave"] -column 0 -row 3 -sticky ew -padx 5 -pady 5
grid [ttk::button .fr_buttons.btn_save -text "Save As..." -command "save_file"] -column 0 -row 4 -sticky ew -padx 5 -pady 5

grid [frame .base] -column 1 -row 0 -sticky nsew
grid [text .base.txt_edit -padx 4 -undo true -autoseparators true -wrap "none"] -column 0 -row 0 -sticky nsew -columnspan 2
grid columnconfigure . 1 -weight 1; grid rowconfigure . 0 -weight 1
grid columnconfigure .base 0 -weight 1; grid rowconfigure .base 0 -weight 1

grid [ttk::scrollbar .scroll -orient "vertical" -command ".base.txt_edit yview"] -column 2 -row 0 -sticky nse
grid [ttk::scrollbar .xascroll -orient "horizontal" -command ".base.txt_edit xview"] -column 1 -row 1 -sticky we

.base.txt_edit configure -xscrollcommand ".xascroll set" -yscrollcommand ".scroll set"

grid [ttk::separator .sep -orient "horizontal"] -column 0 -row 2 -sticky ew -columnspan 3
grid [frame .sepfr] -column 0 -row 3 -sticky ew -columnspan 3
grid [label .sepfr.statusbar -text " By Grim Stride" -anchor w -bd 0 -relief "solid"] -column 0 -row 0 -sticky sew -pady 4
grid columnconfigure .sepfr 0 -weight 2; grid rowconfigure .sepfr 0 -weight 1
grid [label .sepfr.txpos -textvariable asdf -anchor e -bd 0 -relief "solid"] -column 1 -row 0 -sticky sew -pady 4 -padx 8
grid [button .sepfr.btn_conf -relief "flat" -command "config" -image [image create photo ::img::new -format GIF -data {R0lGODlhEAASANUAAP////7+/v39/fj4+PT09PHx8ZKSkomJiX9/f319fXt7e3BwcG5ubmJiYmFhYWBgYF9fX1JSUlFRUUVFRUNDQyYmJiIiIhoaGhcXFxQUFBEREQ0NDQoKCgkJCQgICAAAAP///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAACAALAAAAAAQABIAAAZxQJAQBCgOj8OiAOKhFIpQIwDxqVqvVUTRYLlYM5aw2AAgFhOVxiAKRbaRcPg7yQYQJBhGQHrQ+P8cVhsaB0V9f36BVYOFZmwEERgLe2VxQnNuRpaOChUPa3VEXF5VYGJhZFNYqx9aZgIOHRNPoUeYSEEAOw==}] -compound "center" -bd 0] -column 2 -row 0 -sticky ew
grid columnconfigure .sepfr 1 -weight 1

#bind .base.txt_edit <KeyPress> {checkmod
bind .base.txt_edit <KeyRelease> {checkmod}
bind .base.txt_edit <<Modified>> { if { [.base.txt_edit edit modified] == 1 } { wm title . "*[string trim "[wm title .]" "*"]" } }
#bind .base.txt_edit <ButtonRelease-1> {getline}
#set tidx [.base.txt_edit index "insert"]
#trace add variable tidx write getline
#puts [::md5::md5 -hex [.base.txt_edit get 1.0 end]]
getline:set asdf

vwait forever
