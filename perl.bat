@echo off

setlocal
set PERL5LIB=/lib/perl5
"%~dp0git-1.9.0.chromium.6_bin\bin\perl.exe" %*
