Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c mariana.bat"
oShell.Run strArgs, 0, false
