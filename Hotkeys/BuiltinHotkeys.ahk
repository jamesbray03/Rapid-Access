;-------------------------------------------------------------------------------
;;; BUILT-IN ;;;
;	shortcuts the user can't delete
;-------------------------------------------------------------------------------

if shortcut = ? ; Open Settings
{
    gui_destroy()
    Run %A_ScriptDir%\Settings\Settings.pyw
}
else if shortcut = %A_Space% ; Google search
{
    gui_search_title = Google search
    gui_search("https://www.google.com/search?&q=REPLACEME")
}
else if shortcut = q ; Close active window
{
    gui_destroy()
	WinClose, A
}
else if shortcut = rel ; Reload Application
{
    gui_destroy()
	Reload
}
else if shortcut = zzz ; Sleep
{
    gui_destroy()
    DllCall("PowrProf\SetSuspendState", "int", 0, "int", 0, "int", 0)
}
else
{
    #Include %A_ScriptDir%\Hotkeys\CustomHotkeys.ahk
}
