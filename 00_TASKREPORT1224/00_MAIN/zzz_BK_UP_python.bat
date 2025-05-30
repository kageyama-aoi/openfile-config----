@echo on
cd /d %~dp0
REM/* カレントディレクトリ */
set FOLDER=%~dp0
REM/* YYMMDD形式で日付を取得 */
set TODAY=%DATE:~0,4%%DATE:~5,2%%DATE:~8,2%_%TIME:~0,2%%TIME:~3,2%
REM/* バックアップ */
mkdir %FOLDER%\"BK_UP"\%TODAY%

set filename=error_.txt
SET output=%filename%
REM/*　ワイルドカードだとうまくいかず：対応策copy→xcopy*/
xcopy *.py %FOLDER%\"BK_UP"\%TODAY% 2> ./error_log/%output%
exit 0
