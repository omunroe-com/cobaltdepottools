@echo off
setlocal
:: This is required with cygwin only.
PATH=%~dp0;%PATH%
"%~dp0ninja-win.exe" %*
