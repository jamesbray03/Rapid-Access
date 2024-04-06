;-------------------------------------------------------------------------------
;;; BUILT-IN ;;;
;	shortcuts the user can't delete
;-------------------------------------------------------------------------------

if shortcut = ? ; Open Settings
{
    gui_destroy()
    Run %A_ScriptDir%\Settings\Settings.pyw
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
else if shortcut = %A_Space% ; Search Brave
{
    gui_search_title = Search Brave
    gui_search("https://search.brave.com/search?q=REPLACEME&source=desktop")
}
else if shortcut = g%A_Space% ; Google Apps
{
    gui_search_title = Google Service:
    gui_search("https://REPLACEME.google.com")
}
else if shortcut = i%A_Space% ; iOS Web Apps
{
    gui_search_title = Search iOS services
    gui_search("https://www.icloud.com/REPLACEME/")
}
else if shortcut = p%A_Space% ; Proton Web Apps
{
    gui_search_title = Search Proton services
    gui_search("https://proton.me/REPLACEME")
}
else if shortcut = yt%A_Space% ; Search YouTube
{
    gui_search_title = Search YouTube
    gui_search("https://www.youtube.com/results?search_query=REPLACEME")
}
else
{
    #Include %A_ScriptDir%\Hotkeys\CustomHotkeys.ahk
}
