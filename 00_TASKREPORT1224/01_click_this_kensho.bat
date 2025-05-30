@echo off
cd /d %~dp0

for /F "tokens=2" %%i in ("date /t") do set mydate=%%i
set mydate=%mydate:/=%
set mydate=%date:/=%
REM set mytime=%time::=-%
set mytime=%time: =0%
set mytime=%mytime::=%
set filename=error_%mydate%_%mytime%.txt
SET output=%filename%
REM SET output=kageyama.txt

@echo on
python ./00_MAIN/taskreport.py 2> ./error_log/%output%
REM python ./00_MAIN/00_CraeteTaskreport.py 1>%output% 2>&1
REM python bugreport.py
parse
exit 0
