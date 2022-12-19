#############################################################################
# Generated by PAGE version 7.6
#  in conjunction with Tcl version 8.6
#  Dec 19, 2022 04:38:15 PM GMT  platform: Windows NT
set vTcl(timestamp) ""
if {![info exists vTcl(borrow)]} {
    ::vTcl::MessageBox -title Error -message  "You must open project files from within PAGE."
    exit}


set image_list { 
}
vTcl:create_project_images $image_list   ;# In image.tcl

if {!$vTcl(borrow) && !$vTcl(template)} {

set vTcl(actual_gui_font_dft_desc)  TkDefaultFont
set vTcl(actual_gui_font_dft_name)  TkDefaultFont
set vTcl(actual_gui_font_text_desc)  TkTextFont
set vTcl(actual_gui_font_text_name)  TkTextFont
set vTcl(actual_gui_font_fixed_desc)  TkFixedFont
set vTcl(actual_gui_font_fixed_name)  TkFixedFont
set vTcl(actual_gui_font_menu_desc)  TkMenuFont
set vTcl(actual_gui_font_menu_name)  TkMenuFont
set vTcl(actual_gui_font_tooltip_desc)  TkDefaultFont
set vTcl(actual_gui_font_tooltip_name)  TkDefaultFont
set vTcl(actual_gui_font_treeview_desc)  TkDefaultFont
set vTcl(actual_gui_font_treeview_name)  TkDefaultFont
########################################### 
set vTcl(actual_gui_bg) #d9d9d9
set vTcl(actual_gui_fg) #000000
set vTcl(actual_gui_analog) #ececec
set vTcl(actual_gui_menu_analog) #ececec
set vTcl(actual_gui_menu_bg) #d9d9d9
set vTcl(actual_gui_menu_fg) #000000
set vTcl(complement_color) gray40
set vTcl(analog_color_p) #c3c3c3
set vTcl(analog_color_m) beige
set vTcl(tabfg1) black
set vTcl(tabfg2) black
set vTcl(actual_gui_menu_active_bg)  #ececec
set vTcl(actual_gui_menu_active_fg)  #000000
########################################### 
set vTcl(pr,autoalias) 1
set vTcl(pr,relative_placement) 1
set vTcl(mode) Relative
}




proc vTclWindow.top1 {base} {
    global vTcl
    if {$base == ""} {
        set base .top1
    }
    if {[winfo exists $base]} {
        wm deiconify $base; return
    }
    set top $base
    set target $base
    ###################
    # CREATING WIDGETS
    ###################
    vTcl::widgets::core::toplevel::createCmd $top -class Toplevel \
        -background $vTcl(actual_gui_bg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black 
    wm focusmodel $top passive
    wm geometry $top 600x450+505+135
    update
    # set in toplevel.wgt.
    global vTcl
    global img_list
    set vTcl(save,dflt,origin) 0
    wm maxsize $top 3844 1061
    wm minsize $top 120 1
    wm overrideredirect $top 0
    wm resizable $top 1 1
    wm deiconify $top
    set toptitle "Badenoch Gardening Club"
    wm title $top $toptitle
    namespace eval ::widgets::${top}::ClassOption {}
    set ::widgets::${top}::ClassOption(-toptitle) $toptitle
    vTcl:DefineAlias "$top" "Toplevel1" vTcl:Toplevel:WidgetProc "" 1
    set vTcl(real_top) {}
    ttk::style configure TLabel -background $vTcl(actual_gui_bg)
    ttk::style configure TLabel -foreground $vTcl(actual_gui_fg)
    ttk::style configure TLabel -font "$vTcl(actual_gui_font_dft_desc)"
    ttk::label "$top.tLa47" \
        -background $vTcl(actual_gui_bg) -foreground $vTcl(actual_gui_fg) \
        -font "-family {Segoe UI} -size 12 -weight normal -slant roman -underline 0 -overstrike 0" \
        -relief raised -anchor w -justify center -text "Entry Form" \
        -compound left 
    vTcl:DefineAlias "$top.tLa47" "Title" vTcl:WidgetProc "Toplevel1" 1
### SPOT dump_widget_opt A
    ttk::style configure TEntry -background $vTcl(actual_gui_bg)
    ttk::style configure TEntry -foreground $vTcl(actual_gui_fg)
    ttk::style configure TEntry -font "$vTcl(actual_gui_font_dft_desc)"
    ttk::entry "$top.tEn48" \
        -font "TkTextFont" -foreground {} -background {} -takefocus {} \
        -cursor ibeam 
    vTcl:DefineAlias "$top.tEn48" "NameEntry" vTcl:WidgetProc "Toplevel1" 1
### SPOT dump_widget_opt A
    ttk::style configure TLabel -background $vTcl(actual_gui_bg)
    ttk::style configure TLabel -foreground $vTcl(actual_gui_fg)
    ttk::style configure TLabel -font "$vTcl(actual_gui_font_dft_desc)"
    ttk::label "$top.tLa49" \
        -background $vTcl(actual_gui_bg) -foreground $vTcl(actual_gui_fg) \
        -font "TkDefaultFont" -relief flat -anchor w -justify left \
        -text "Name:" -compound left 
    vTcl:DefineAlias "$top.tLa49" "NameLabel" vTcl:WidgetProc "Toplevel1" 1
### SPOT dump_widget_opt A
    ttk::style configure TCheckbutton -background $vTcl(actual_gui_bg)
    ttk::style configure TCheckbutton -foreground $vTcl(actual_gui_fg)
    ttk::style configure TCheckbutton -font "$vTcl(actual_gui_font_dft_desc)"
    ttk::style configure TCheckbutton -background $vTcl(actual_gui_bg)
    ttk::style configure TCheckbutton -foreground $vTcl(actual_gui_fg)
    ttk::style configure TCheckbutton -font "$vTcl(actual_gui_font_dft_desc)"
    ttk::checkbutton "$top.tCh51" \
        -variable "tch51" -takefocus {} -text "member?" -compound left 
    vTcl:DefineAlias "$top.tCh51" "MemberCheck" vTcl:WidgetProc "Toplevel1" 1
### SPOT dump_widget_opt A
    ttk::style configure Entry -background $vTcl(actual_gui_bg)
    ttk::style configure Entry -foreground $vTcl(actual_gui_fg)
    ttk::style configure Entry -font "$vTcl(actual_gui_font_dft_desc)"
    entry "$top.ent52" \
        -background white -disabledforeground #a3a3a3 -font "TkFixedFont" \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -insertbackground black -selectbackground #c4c4c4 \
        -selectforeground black -textvariable "class_var" -width 44 
    vTcl:DefineAlias "$top.ent52" "ClassEntry" vTcl:WidgetProc "Toplevel1" 1
### SPOT dump_widget_opt A
    ttk::style configure TCombobox -background $vTcl(actual_gui_bg)
    ttk::style configure TCombobox -foreground $vTcl(actual_gui_fg)
    ttk::style configure TCombobox -font "$vTcl(actual_gui_font_dft_desc)"
    ttk::combobox "$top.tCo54" \
        -values "1 2" -font "TkTextFont" -textvariable "countVar" \
        -foreground {} -background {} -takefocus {} 
    vTcl:DefineAlias "$top.tCo54" "entryCount" vTcl:WidgetProc "Toplevel1" 1
### SPOT dump_widget_opt A
    ttk::style configure TLabel -background $vTcl(actual_gui_bg)
    ttk::style configure TLabel -foreground $vTcl(actual_gui_fg)
    ttk::style configure TLabel -font "$vTcl(actual_gui_font_dft_desc)"
    ttk::label "$top.tLa55" \
        -background $vTcl(actual_gui_bg) -foreground $vTcl(actual_gui_fg) \
        -font "TkDefaultFont" -relief sunken -anchor w -justify left \
        -textvariable "::description_var" -compound left 
    vTcl:DefineAlias "$top.tLa55" "description" vTcl:WidgetProc "Toplevel1" 1
### SPOT dump_widget_opt A
    set ::description_var {}
    ttk::style configure Label -background $vTcl(actual_gui_bg)
    ttk::style configure Label -foreground $vTcl(actual_gui_fg)
    ttk::style configure Label -font "$vTcl(actual_gui_font_dft_desc)"
    label "$top.lab56" \
        -activebackground #f9f9f9 -activeforeground SystemButtonText \
        -anchor w -background $vTcl(actual_gui_bg) -compound left \
        -disabledforeground #a3a3a3 \
        -font "-family {Segoe UI} -size 10 -weight normal -slant roman -underline 0 -overstrike 0" \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text "Class" 
    vTcl:DefineAlias "$top.lab56" "ClassLabel" vTcl:WidgetProc "Toplevel1" 1
### SPOT dump_widget_opt A
    ttk::style configure Label -background $vTcl(actual_gui_bg)
    ttk::style configure Label -foreground $vTcl(actual_gui_fg)
    ttk::style configure Label -font "$vTcl(actual_gui_font_dft_desc)"
    label "$top.lab57" \
        -activebackground #f9f9f9 -activeforeground SystemButtonText \
        -anchor w -background $vTcl(actual_gui_bg) -compound left \
        -disabledforeground #a3a3a3 \
        -font "-family {Segoe UI} -size 10 -weight normal -slant roman -underline 0 -overstrike 0" \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text "Description" 
    vTcl:DefineAlias "$top.lab57" "DescriptionLabel" vTcl:WidgetProc "Toplevel1" 1
### SPOT dump_widget_opt A
    ttk::style configure Label -background $vTcl(actual_gui_bg)
    ttk::style configure Label -foreground $vTcl(actual_gui_fg)
    ttk::style configure Label -font "$vTcl(actual_gui_font_dft_desc)"
    label "$top.lab58" \
        -activebackground #f9f9f9 -activeforeground SystemButtonText \
        -anchor w -background $vTcl(actual_gui_bg) -compound left \
        -disabledforeground #a3a3a3 \
        -font "-family {Segoe UI} -size 10 -weight normal -slant roman -underline 0 -overstrike 0" \
        -foreground $vTcl(actual_gui_fg) \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -text "Count" 
    vTcl:DefineAlias "$top.lab58" "CountLabel" vTcl:WidgetProc "Toplevel1" 1
### SPOT dump_widget_opt A
    ttk::style configure Scrolledlistbox -background $vTcl(actual_gui_bg)
    ttk::style configure Scrolledlistbox -foreground $vTcl(actual_gui_fg)
    ttk::style configure Scrolledlistbox -font "$vTcl(actual_gui_font_dft_desc)"
    vTcl::widgets::ttk::scrolledlistbox::CreateCmd "$top.scr47" \
        -background $vTcl(actual_gui_bg) -height 75 \
        -highlightbackground $vTcl(actual_gui_bg) -highlightcolor black \
        -width 125 
    vTcl:DefineAlias "$top.scr47" "Scrolledlistbox" vTcl:WidgetProc "Toplevel1" 1
### SPOT dump_widget_opt A

    $top.scr47.01 configure -background white \
        -cursor xterm \
        -disabledforeground #a3a3a3 \
        -font TkFixedFont \
        -foreground black \
        -height 3 \
        -highlightbackground #d9d9d9 \
        -highlightcolor #d9d9d9 \
        -selectbackground #c4c4c4 \
        -selectforeground black \
        -selectmode single \
        -width 10 \
        -listvariable entriesVar
    ttk::style configure TButton -background $vTcl(actual_gui_bg)
    ttk::style configure TButton -foreground $vTcl(actual_gui_fg)
    ttk::style configure TButton -font "$vTcl(actual_gui_font_dft_desc)"
    ttk::style configure TButton -background $vTcl(actual_gui_bg)
    ttk::style configure TButton -foreground $vTcl(actual_gui_fg)
    ttk::style configure TButton -font "$vTcl(actual_gui_font_dft_desc)"
    ttk::button "$top.tBu47" \
        -takefocus {} -text "Edit" -compound left -state disabled 
    vTcl:DefineAlias "$top.tBu47" "EditButton" vTcl:WidgetProc "Toplevel1" 1
### SPOT dump_widget_opt A
    ttk::style configure TButton -background $vTcl(actual_gui_bg)
    ttk::style configure TButton -foreground $vTcl(actual_gui_fg)
    ttk::style configure TButton -font "$vTcl(actual_gui_font_dft_desc)"
    ttk::style configure TButton -background $vTcl(actual_gui_bg)
    ttk::style configure TButton -foreground $vTcl(actual_gui_fg)
    ttk::style configure TButton -font "$vTcl(actual_gui_font_dft_desc)"
    ttk::button "$top.tBu48" \
        -takefocus {} -text "Delete" -compound left -state disabled 
    vTcl:DefineAlias "$top.tBu48" "DeleteButton" vTcl:WidgetProc "Toplevel1" 1
### SPOT dump_widget_opt A
    ttk::style configure TButton -background $vTcl(actual_gui_bg)
    ttk::style configure TButton -foreground $vTcl(actual_gui_fg)
    ttk::style configure TButton -font "$vTcl(actual_gui_font_dft_desc)"
    ttk::style configure TButton -background $vTcl(actual_gui_bg)
    ttk::style configure TButton -foreground $vTcl(actual_gui_fg)
    ttk::style configure TButton -font "$vTcl(actual_gui_font_dft_desc)"
    ttk::button "$top.tBu49" \
        -takefocus {} -text "Cancel" -compound left 
    vTcl:DefineAlias "$top.tBu49" "CancelButton" vTcl:WidgetProc "Toplevel1" 1
### SPOT dump_widget_opt A
    ttk::style configure TButton -background $vTcl(actual_gui_bg)
    ttk::style configure TButton -foreground $vTcl(actual_gui_fg)
    ttk::style configure TButton -font "$vTcl(actual_gui_font_dft_desc)"
    ttk::style configure TButton -background $vTcl(actual_gui_bg)
    ttk::style configure TButton -foreground $vTcl(actual_gui_fg)
    ttk::style configure TButton -font "$vTcl(actual_gui_font_dft_desc)"
    ttk::button "$top.tBu50" \
        -takefocus {} -text "Save" -compound left 
    vTcl:DefineAlias "$top.tBu50" "SaveButton" vTcl:WidgetProc "Toplevel1" 1
### SPOT dump_widget_opt A
    ttk::style configure TLabel -background $vTcl(actual_gui_bg)
    ttk::style configure TLabel -foreground $vTcl(actual_gui_fg)
    ttk::style configure TLabel -font "$vTcl(actual_gui_font_dft_desc)"
    ttk::label "$top.tLa48" \
        -background $vTcl(actual_gui_bg) -foreground $vTcl(actual_gui_fg) \
        -font "TkDefaultFont" -relief flat -anchor w -justify left \
        -text "Total Entries:" -compound left 
    vTcl:DefineAlias "$top.tLa48" "TotalsLabel" vTcl:WidgetProc "Toplevel1" 1
### SPOT dump_widget_opt A
    ttk::style configure TLabel -background $vTcl(actual_gui_bg)
    ttk::style configure TLabel -foreground $vTcl(actual_gui_fg)
    ttk::style configure TLabel -font "$vTcl(actual_gui_font_dft_desc)"
    ttk::label "$top.tLa50" \
        -background $vTcl(actual_gui_bg) -foreground $vTcl(actual_gui_fg) \
        -font "TkDefaultFont" -relief sunken -anchor w -justify left \
        -textvariable "::totalsVar" -compound left 
    vTcl:DefineAlias "$top.tLa50" "Totals" vTcl:WidgetProc "Toplevel1" 1
### SPOT dump_widget_opt A
    set ::totalsVar {}
    ###################
    # SETTING GEOMETRY
    ###################
    place $top.tLa47 \
        -in $top -x 0 -y 0 -width 0 -relwidth 1.008 -height 0 \
        -relheight 0.064 -anchor nw -bordermode ignore 
    place $top.tEn48 \
        -in $top -x 0 -relx 0.133 -y 0 -rely 0.133 -width 396 -relwidth 0 \
        -height 21 -relheight 0 -anchor nw -bordermode ignore 
    place $top.tLa49 \
        -in $top -x 0 -relx 0.033 -y 0 -rely 0.133 -width 0 -relwidth 0.108 \
        -height 0 -relheight 0.042 -anchor nw -bordermode ignore 
    place $top.tCh51 \
        -in $top -x 0 -relx 0.833 -y 0 -rely 0.111 -width 0 -relwidth 0.133 \
        -height 0 -relheight 0.091 -anchor nw -bordermode ignore 
    place $top.ent52 \
        -in $top -x 0 -relx 0.033 -y 0 -rely 0.267 -width 44 -relwidth 0 \
        -height 20 -relheight 0 -anchor nw -bordermode ignore 
    place $top.tCo54 \
        -in $top -x 0 -relx 0.867 -y 0 -rely 0.267 -width 0 -relwidth 0.072 \
        -height 0 -relheight 0.047 -anchor nw -bordermode ignore 
    place $top.tLa55 \
        -in $top -x 0 -relx 0.15 -y 0 -rely 0.267 -width 0 -relwidth 0.642 \
        -height 0 -relheight 0.042 -anchor nw -bordermode ignore 
    place $top.lab56 \
        -in $top -x 0 -relx 0.033 -y 0 -rely 0.222 -width 0 -relwidth 0.073 \
        -height 0 -relheight 0.047 -anchor nw -bordermode ignore 
    place $top.lab57 \
        -in $top -x 0 -relx 0.15 -y 0 -rely 0.222 -width 0 -relwidth 0.157 \
        -height 0 -relheight 0.047 -anchor nw -bordermode ignore 
    place $top.lab58 \
        -in $top -x 0 -relx 0.867 -y 0 -rely 0.222 -width 0 -relwidth 0.073 \
        -height 0 -relheight 0.047 -anchor nw -bordermode ignore 
    place $top.scr47 \
        -in $top -x 0 -relx 0.033 -y 0 -rely 0.356 -width 0 -relwidth 0.752 \
        -height 0 -relheight 0.478 -anchor nw -bordermode ignore 
    place $top.tBu47 \
        -in $top -x 0 -relx 0.833 -y 0 -rely 0.356 -width 66 -relwidth 0 \
        -height 25 -relheight 0 -anchor nw -bordermode ignore 
    place $top.tBu48 \
        -in $top -x 0 -relx 0.833 -y 0 -rely 0.444 -width 66 -relwidth 0 \
        -height 25 -relheight 0 -anchor nw -bordermode ignore 
    place $top.tBu49 \
        -in $top -x 0 -relx 0.7 -y 0 -rely 0.889 -width 76 -relwidth 0 \
        -height 25 -relheight 0 -anchor nw -bordermode ignore 
    place $top.tBu50 \
        -in $top -x 0 -relx 0.85 -y 0 -rely 0.889 -width 76 -relwidth 0 \
        -height 25 -relheight 0 -anchor nw -bordermode ignore 
    place $top.tLa48 \
        -in $top -x 0 -relx 0.033 -y 0 -rely 0.889 -width 0 -relwidth 0.125 \
        -height 0 -relheight 0.064 -anchor nw -bordermode ignore 
    place $top.tLa50 \
        -in $top -x 0 -relx 0.167 -y 0 -rely 0.889 -width 0 -relwidth 0.058 \
        -height 0 -relheight 0.064 -anchor nw -bordermode ignore 

    vTcl:FireEvent $base <<Ready>>
}

proc 36 {args} {return 1}


Window show .
set btop1 ""
if {$vTcl(borrow)} {
    set btop1 .bor[expr int([expr rand() * 100])]
    while {[lsearch $btop1 $vTcl(tops)] != -1} {
        set btop1 .bor[expr int([expr rand() * 100])]
    }
}
set vTcl(btop) $btop1
Window show .top1 $btop1
if {$vTcl(borrow)} {
    $btop1 configure -background plum
}

