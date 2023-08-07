;-------------------------------------------------------------------------------
;;; INIT ;;;
;   Called from master to initialise gui parameters
;-------------------------------------------------------------------------------

gui_init:
    gui_options := "xm w220 " . "cc5c8c6" . " -E0x200"
    gui_state = closed
    return

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
	Gui, Color, 1d1f21, 282a2e
	Gui, +AlwaysOnTop -SysMenu +ToolWindow -Caption +Border
	Gui, Font, s11, Segoe UI
	Gui, Add, Text, %gui_options% vgui_main_title, Rapid Access
	Gui, Font, s10, Segoe UI
	Gui, Add, Edit, %gui_options% vshortcut gFindus
	Gui, Show, , myGUI
	return

;-------------------------------------------------------------------------------
;;; LINK SEARCH ;;;
;   Generates a search bar after initial prompt
;-------------------------------------------------------------------------------

; Global function called from 'UserCommands.ahk'
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
	
    ; Check if its a clipboard call or a search
    if (RegExMatch(gui_search_content, "^\d+$"))
    {
        copy_to_clip(gui_search_content)
    }
    else
    {
		StringReplace, search_final_url, search_url, REPLACEME, % validate_url(gui_search_content)
		run %search_final_url%
    }
    return

;-------------------------------------------------------------------------------
;;; TOOLTIP ;;;
;   Generates a tooltip displaying all shortcuts
;-------------------------------------------------------------------------------

gui_tooltip:
    tooltiptext =
	tooltiptextpadded =
    maxpadding = 0
	
	; Find each shortcut using script text
    Loop, read, %A_ScriptDir%/Subscripts/UserCommands.ahk
    {
		if InStr(A_LoopReadLine, "if shortcut =")
		{
			; Format command for tooltip
			StringGetPos, setpos, A_LoopReadLine, =
			StringTrimLeft, trimmed, A_LoopReadLine, setpos+1 ;
			StringReplace, trimmed, trimmed, `%A_Space`%, _, All ;
			tooltiptext .= trimmed
			tooltiptext .= "`n"
			
			; Correct padding
			StringGetPos, commentpos, trimmed, `;
			if (maxpadding < commentpos)
				maxpadding := commentpos
		}
		else if (SubStr(A_LoopReadLine, 1, 3) = ";;;")
		{
			tooltiptext .= "`n" . StrReplace(A_LoopReadLine, ";;;", "###") . "`n"
			tooltiptext .= 
		}
    }
	tooltiptext := SubStr(tooltiptext, 3)
	
	; Align the comments
    Loop, Parse, tooltiptext,`n
    {
        line = %A_LoopField%
        StringGetPos, commentpos, line, `;
        spaces_to_insert := maxpadding - commentpos
        Loop, %spaces_to_insert%
        {
            StringReplace, line, line,`;,%A_Space%`;
        }
        tooltiptextpadded .= line . "`n"
    }
	
	; Instantiate tooltip
	CoordMode, Tooltip, Screen
	ToolTip, %tooltiptextpadded%, 3, 3, 1
	
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
Findus:
    Gui, Submit, NoHide
    #Include %A_ScriptDir%\Subscripts\UserCommands.ahk
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