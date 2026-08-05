@echo off
setlocal

set TOOL=tools\antlr-4.13.2-complete.jar
set GRAMMAR_DIR=grammar
set OUT=compiler\generated

rem Prefer JAVA_HOME (e.g. a JDK 17+ used by ANTLR), fall back to PATH.
set "JAVA=java"
if defined JAVA_HOME if exist "%JAVA_HOME%\bin\java.exe" set "JAVA=%JAVA_HOME%\bin\java.exe"

echo Generating parser from %GRAMMAR_DIR%\Linkora.g4 ...
if exist "%OUT%" rmdir /s /q "%OUT%"
mkdir "%OUT%"

pushd "%GRAMMAR_DIR%"
"%JAVA%" -jar "..\%TOOL%" -Dlanguage=Python3 -visitor -o "..\%OUT%" Linkora.g4
popd

if errorlevel 1 (
    echo.
    echo Error: parser generation failed.
    echo Tip: ANTLR 4.13.2 requires Java 11 or newer.
    exit /b 1
)

rem Mark the directory as a Python package.
type nul > "%OUT%\__init__.py"

echo.
echo Parser generated into %OUT%
endlocal
