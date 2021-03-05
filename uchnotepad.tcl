package require Tk
package require archive
package require tdom
package require extrafont

extrafont::load res/custom1.ttf

proc open_file {mode} {
    set filename [tk_getOpenFile]
    if { $filename == "" } {
        return
    }
    if { $mode == 0 } { 
        set opn [open $filename r]
        set text [read $opn]
        .base.txt_edit insert 0.0 $text
        close $opn
    } else {
        set result [exec lzmadec $filename]
        set result2 [xmlpretty $result]
        .base.txt_edit insert 0.0 $result2
    }
}

proc nsav {} {
    set filename [tk_getOpenFile]
    if { $filename == "" } {
        return
    }
    set opn [open $filename r]
    set text [read $opn]
    set conv [lzdec $text]
    set conv1 [encoding convertto unicode $conv]
}

 proc xmlpretty xml { [[dom parse $xml doc] documentElement] asXML -indent 2}

wm title . "UCH Notepad TCL beta"
wm iconbitmap . icon.ico
wm minsize . 200 270

grid [frame .fr_buttons] -column 0 -row 0 -sticky ns
grid [ttk::button .fr_buttons.btn_open -text "Open Level" -command "open_file {0}"] -column 0 -row 1 -sticky ew -padx 5 -pady 5
grid [ttk::button .fr_buttons.btn_orul -text "Open Ruleset" -command "open_file {1}"] -column 0 -row 2 -sticky ew -padx 5 -pady 5
grid [ttk::button .fr_buttons.btn_nsav -text "Save" -command "gg {3}"] -column 0 -row 3 -sticky ew -padx 5 -pady 5
grid [ttk::button .fr_buttons.btn_save -text "Save As..."] -column 0 -row 4 -sticky ew -padx 5 -pady 5

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
grid [label .sepfr.txpos -text "Ln: 1 Col: 1" -anchor e -bd 0 -relief "solid"] -column 1 -row 0 -sticky sew -pady 4 -padx 8
grid [button .sepfr.btn_conf -relief "flat" -image [image create photo ::img::new -format GIF -data {R0lGODlhEAASANUAAP////7+/v39/fj4+PT09PHx8ZKSkomJiX9/f319fXt7e3BwcG5ubmJiYmFhYWBgYF9fX1JSUlFRUUVFRUNDQyYmJiIiIhoaGhcXFxQUFBEREQ0NDQoKCgkJCQgICAAAAP///wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAACAALAAAAAAQABIAAAZxQJAQBCgOj8OiAOKhFIpQIwDxqVqvVUTRYLlYM5aw2AAgFhOVxiAKRbaRcPg7yQYQJBhGQHrQ+P8cVhsaB0V9f36BVYOFZmwEERgLe2VxQnNuRpaOChUPa3VEXF5VYGJhZFNYqx9aZgIOHRNPoUeYSEEAOw==}] -compound "center" -bd 0] -column 2 -row 0 -sticky ew
grid columnconfigure .sepfr 1 -weight 1


vwait forever
