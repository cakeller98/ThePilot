REM This script will create a zip file of the addon in the same folder as the script

REM display the current directory so we know where we are starting from:
echo Current directory:
echo %cd%

REM switch to the directory whwere THIS batch file is located:
cd /d %~dp0

python pack_plugin.py 