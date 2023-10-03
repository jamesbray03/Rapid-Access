;-------------------------------------------------------------------------------
;;; INIT ;;;
;	Include and run necessary scripts
;-------------------------------------------------------------------------------

#Include %A_ScriptDir%\Subscripts\GUI.ahk

#NoEnv
#SingleInstance

SendMode Input
SetWorkingDir %A_ScriptDir%

Gosub, gui_init
return

;-------------------------------------------------------------------------------
;;; FUNCTIONS ;;;
;   Functions that are called by raw keyboard input outside of the UI
;-------------------------------------------------------------------------------

; Locks a window to the top of the screen
^SPACE:: 
	Winset, Alwaysontop, , A
	return