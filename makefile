#Add any comments on this here

#Ensure the script is run as bash
SHELL:=/bin/bash

#Set help as the default for this makefile.
.DEFAULT: help

.PHONY: clean help venv su static migrations run run-debug test cov-html black flake8 isort run-dock build-dock

help:
	@echo ""
	@echo "PROJECT HELP:"
	@echo "make               		- this prints out the help for this makefile."
	@echo "make help          		- this prints out the help for this makefile."
	@echo "Clean:"
	@echo "make clean	    		- DANGER - remove .py files, venv, coverage etc."
	@echo "Setup:"
	@echo "make venv	    		- Make the virtual environment."
	@echo "Code Formatting:"
	@echo "make isort	    		- Apply isort"
	@echo "make flake8	    		- Apply flake8"
	@echo "make doc		    		- Apply pydocstring"
	@echo ""

clean:
	@echo ""
	@echo "*** clean ***"
	@echo ""
	(rm -rf venv; rem -rf *.ics; rm -rf *.pyc; find . -type d -name  "__pycache__" -exec rm -r {} +; )
	@echo ""

venv:
	@echo ""
	@echo "*** make virtual env ***"
	@echo ""
	(rm -rf venv; python3 -m venv venv; source venv/bin/activate; pip3 install -r requirements.txt; )
	@echo ""

isort:
	@echo ""
	@echo "*** isort ***"
	@echo ""
	( isort . )
	@echo ""

flake8:
	@echo ""
	@echo "*** make virtual env ***"
	@echo ""
	(flake8 . )
	@echo ""

doc:
	@echo ""
	@echo "*** make virtual env ***"
	@echo ""
	( pydocstyle . )
	@echo ""