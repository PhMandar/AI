@echo off
if exist "venv\" (
    echo Virtual environment folder 'venv' exists, activating it.
) else (
    echo 'venv' folder does not exist. Creating new Virtual environment.
	python -m venv venv	
)

REM Activating virtual environment.
venv\Scripts\activate