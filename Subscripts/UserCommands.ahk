;-------------------------------------------------------------------------------
;;; CLIPBOARD ;;;
;	Utilises text files to store multiple clipboards
;
;	To copy, press caps > c > [desired board 1-3]
;	To paste, press caps > [desired board 1-3]
;
;	(note: normally struggles with line breaks and tabs)
;-------------------------------------------------------------------------------

copy_to_clip(board)
{
	if clipboard != ""
	{
		file_path = % A_ScriptDir . "\clipboard_" . board . ".txt"
		SendInput, ^c
		Sleep 100
		ClipWait, 1
		FileDelete, %file_path%
		FileAppend, %clipboard%, %file_path%
		return
	}
}

if shortcut = c ; Copy to Clipboard
{
	gui_search_title = Select Clipboard
	gui_search("REPLACEME")
}
else if shortcut = 1 ; Paste Board 1
{
	gui_destroy()
    FileRead, file_content, % A_ScriptDir . "\clipboard_1.txt"
	Send, % file_content
}
else if shortcut = 2 ; Paste Board 2
{
	gui_destroy()
    FileRead, file_content, % A_ScriptDir . "\clipboard_2.txt"
	Send, % file_content
}
else if shortcut = 3 ; Paste Board 3
{
	gui_destroy()
    FileRead, file_content, % A_ScriptDir . "\clipboard_3.txt"
	Send, % file_content
}

;-------------------------------------------------------------------------------
;;; SEARCH ;;;
;	Uses a second search bar after initial prompt to search via links
;
;	If looking for an app, enter desired app you know exists e.g.:
;		Google > mail, maps, docs, slides, sheets, photos etc.
;		iCloud > mail, photos, calendar, reminders, notes etc.
;		Proton > mail, pass, drive, calendar
;
;	(note: proton vpn has a different link)
;-------------------------------------------------------------------------------

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
    gui_search_title = Search iOS services
    gui_search("https://proton.me/REPLACEME")
}
else if shortcut = yt%A_Space% ; Search YouTube
{
    gui_search_title = Search YouTube
    gui_search("https://www.youtube.com/results?search_query=REPLACEME")
}

;-------------------------------------------------------------------------------
;;; SITES ;;;
;	Launches desired sites on default browser
;-------------------------------------------------------------------------------

else if shortcut = gpt ; Open Chat GPT
{
    gui_destroy()
    run https://chat.openai.com/chat
}
else if shortcut = net ; Open Netflix
{
    gui_destroy()
    Run https://www.netflix.com
}

;-------------------------------------------------------------------------------
;;; APPS ;;;
;	Opens desirsed apps using shortcuts in the 'Apps' folder
;-------------------------------------------------------------------------------

else if shortcut = spo ; Open Spotify
{
    gui_destroy()
    Run %A_ScriptDir%\Apps\Spotify
}
else if shortcut = vs ; Open VS Code
{
    gui_destroy()
    Run %A_ScriptDir%\Apps\VScode
}
else if shortcut = task ; Open Task Manager
{
    gui_destroy()
    Run %A_ScriptDir%\Apps\Task
}
else if shortcut = mat ; Open MATLAB
{
    gui_destroy()
    Run %A_ScriptDir%\Apps\Matlab
}
else if shortcut = note ; Open Notepad
{
    gui_destroy()
    Run %A_ScriptDir%\Apps\Notepad
}

;-------------------------------------------------------------------------------
;;; SOCIALS ;;;
;	Collection of my most used social sites and apps
;-------------------------------------------------------------------------------

else if shortcut = red ; Open Reddit
{
    gui_destroy()
    run https://www.reddit.com
}
else if shortcut = dc ; Open Discord
{
    gui_destroy()
    Run %A_ScriptDir%\Apps\Discord
}

;-------------------------------------------------------------------------------
;;; FOLDERS ;;;
;	Opens desired file directory
;
;	(note: may need adjusting based on your system)
;-------------------------------------------------------------------------------

else if shortcut = doc ; Documents
{
    gui_destroy()
    run C:\Users\%A_Username%\OneDrive\Documents
}
else if shortcut = down ; Downloads
{
    gui_destroy()
    run C:\Users\%A_Username%\Downloads
}
else if shortcut = ss ; Open saved screenshots
{
    gui_destroy()
	run C:\Users\%A_Username%\OneDrive\Pictures\Screenshots
}
else if shortcut = pic ; Open pictures
{
    gui_destroy()
	run C:\Users\%A_Username%\OneDrive\Pictures
}
else if shortcut = dir ; Open script directory
{
    gui_destroy()
    Run, %A_ScriptDir%
}

;-------------------------------------------------------------------------------
;;; MISC ;;;
;	Other useful shortcuts
;-------------------------------------------------------------------------------

else if shortcut = zzz ; Sleep
{
    gui_destroy()
    DllCall("PowrProf\SetSuspendState", "int", 0, "int", 0, "int", 0)
}
else if shortcut = save ; Save image in clipboard
{
    gui_destroy()
	run %A_ScriptDir%\Subscripts\SaveClip.py
}
else if shortcut = q ; Close window
{
    gui_destroy()
	WinClose, A
}
else if shortcut = rel ; Reload script
{
    gui_destroy() ; removes the GUI even when the reload fails
    Reload
}
else if shortcut = edit ; Edit commands
{
    gui_destroy()
    run, notepad++.exe "%A_ScriptDir%\GUI\UserCommands.ahk"
}
else if shortcut = ? ; Command list
{
    GuiControl,, shortcut, ; Clear the input box
    Gosub, gui_tooltip
}