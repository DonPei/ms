@echo off

rem #####################################################################
rem
rem Script that starts the launching pad for MARIANA Software Suites.
rem
rem     Script name:  mariana.bat
rem     Purpose:      This shell script starts a launcher
rem     Arguments:    None
rem
rem Copyright (C) 2023-2024 HaoYanGroup.com
rem All Rights Reserved.
rem
rem #####################################################################

rem SETLOCAL ENABLEEXTENSIONS
rem SETLOCAL ENABLEDELAYEDEXPANSION
rem echo.Current User is '%USERNAME%'
rem echo.%date% %time%

SET LAUNCH_HOME=%~dp0
cd %LAUNCH_HOME% 
rem echo %LAUNCH_HOME% 

SET CLASSPATH=%LAUNCH_HOME%
SET LIBRARYPATH=%LAUNCH_HOME%lib
SET RESOURCESPATH=%LAUNCH_HOME%resources
SET HISTORYPATH=%LAUNCH_HOME%history

rem echo %CLASSPATH%
SET /A tool_id=%1
SET INPUTFILE=%~f2
IF "%1%"=="" goto GUI
IF "%1%"=="0" goto QA

echo invalid argument.
goto Exit
:GUI
rem & C:/Python311/python.exe c:/Projects/books/sandbox/camera1.py
rem C:/Python311/python.exe %LAUNCH_HOME%camera1.py
python.exe %LAUNCH_HOME%src\MarianaGUI.py
PAUSE
goto Exit

:QA
SET DICTIONARYFILE=%~f2
SET /A project_id=%3
echo QA= %tool_id% %INPUTFILE% %DICTIONARYFILE% %project_id%
%LAUNCH_HOME%jre\bin\java -d64 -Xms512m -Xmx4096m -showversion -Drtb.dir=%LAUNCH_HOME% ^
	-Djava.library.path=%LIBRARYPATH% -Djava.resources.path=%RESOURCESPATH% -Djava.history.path=%HISTORYPATH% ^
	-cp %CLASSPATH% edu.uth.app.qac.QacApp %tool_id% %INPUTFILE% %DICTIONARYFILE% %project_id%
goto Exit

:Exit
