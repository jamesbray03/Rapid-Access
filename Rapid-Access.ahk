;-------------------------------------------------------------------------------
;;; INIT ;;;
;	Include and run necessary scripts
;-------------------------------------------------------------------------------

#NoEnv
#SingleInstance force

SendMode Input
SetWorkingDir %A_ScriptDir%

gui_options := "xm w220 " . "cD2D4D3" . " -E0x200"
gui_state := closed

;-------------------------------------------------------------------------------
;;; LAUNCH GUI ;;;
;	Function used to launch and close gui when capslock is pressed
;-------------------------------------------------------------------------------

CapsLock::
	if (gui_state != "closed") 
	{
	   gui_destroy()
	   return
	}
	gui_state := "main"
	Gui, Margin, 16, 16
	Gui, Color, 1D1D21, 2C2F33
	Gui, +AlwaysOnTop -SysMenu +ToolWindow -Caption +Border
	Gui, Font, s11, Segoe UI
	Gui, Add, Text, %gui_options% vgui_main_title, Rapid Access
	Gui, Font, s10, Segoe UI
	Gui, Add, Edit, %gui_options% vshortcut gon_edit
	Gui, Show, , myGUI
	return

;-------------------------------------------------------------------------------
;;; LINK SEARCH ;;;
;   Generates a search bar after initial prompt
;-------------------------------------------------------------------------------

; Global function called from command scripts
gui_search(url) 
{
    global
    if gui_state != search
    {
        gui_state = search
        Gosub, gui_add_search
    }
    search_url := url
}

; Add second search bar (and title)
gui_add_search:
    Gui, Add, Text, %gui_options% , %gui_search_title%
    Gui, Add, Edit, %gui_options% vgui_search_content -WantReturn
    Gui, Add, Button, x-10 y-10 w1 h1 +default ggui_search_enter
    GuiControl, Disable, shortcut
    Gui, Show, AutoSize
    return

; Determines what happens after submission
gui_search_enter:
    Gui, Submit
    gui_destroy()
    StringReplace, search_final_url, search_url, REPLACEME, % validate_url(gui_search_content)
    run %search_final_url%
    return

;-------------------------------------------------------------------------------
;;; FUNCTIONS ;;;
;   Miscellaneous functions
;-------------------------------------------------------------------------------

; Let escape exit gui also
GuiEscape:
    gui_destroy()
    return

; The callback function when the text changes in the input field.
on_edit:
    Gui, Submit, NoHide
    #Include %A_ScriptDir%\Hotkeys\BuiltinHotkeys.ahk
    return

#WinActivateForce
gui_destroy() {
    global gui_state
    global gui_search_title

    gui_state = closed
    gui_search_title =

    ToolTip
    Gui, Destroy
    WinActivate
}

validate_url(str) {
    f = %A_FormatInteger%
    SetFormat, Integer, Hex
    If RegExMatch(str, "^\w+:/{0,2}", pr)
        StringTrimLeft, str, str, StrLen(pr)
    StringReplace, str, str, `%, `%25, All
    Loop
        If RegExMatch(str, "i)[^\w\.~%/:]", char)
           StringReplace, str, str, %char%, % "%" . SubStr(Asc(char),3), All
        Else Break
    SetFormat, Integer, %f%
    Return, pr . str
}
