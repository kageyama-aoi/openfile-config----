@echo on
cd /d %~dp0
set FOLDER=%~dp0
move *.log %FOLDER%old
move error*.txt %FOLDER%old
exit 0
