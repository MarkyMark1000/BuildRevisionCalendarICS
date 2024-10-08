#Add any comments on this here

#Ensure the script is run as bash
SHELL:=/bin/bash

#Set help as the default for this makefile.
.DEFAULT: help

.PHONY: help
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
	@echo "make doc		    	- Apply pydocstring"
	@echo "make mypy		    	- Apply mypy"
	@echo "Tests:"
	@echo "make test	    		- Unittest"
	@echo "Coverage:"
	@echo "make cov-clean		- Remove coverage directory"
	@echo "make cov	    		- Run coverage"
	@echo "make html	    		- Build html report"
	@echo "Run:"
	@echo "make run	    		- Run create_calendar.py"
	@echo ""

.PHONY: clean
clean:
	@echo ""
	@echo "*** clean ***"
	@echo ""
	(rm -rf venv; rem -rf *.ics; rm -rf *.pyc; find . -type d -name  "__pycache__" -exec rm -r {} +; rm -rf ./htmlcov;)
	@echo ""

.PHONY: venv
venv:
	@echo ""
	@echo "*** make virtual env ***"
	@echo ""
	(rm -rf venv; python3 -m venv venv; source venv/bin/activate; pip3 install -r requirements.txt; )
	@echo ""

.PHONY: isort
isort:
	@echo ""
	@echo "*** isort ***"
	@echo ""
	( isort . )
	@echo ""

.PHONY: flake8
flake8:
	@echo ""
	@echo "*** flake8 ***"
	@echo ""
	(flake8 . )
	@echo ""

.PHONY: doc
doc:
	@echo ""
	@echo "*** pydocstyle ***"
	@echo ""
	( pydocstyle . )
	@echo ""

.PHONY: mypy
mypy:
	@echo ""
	@echo "*** apply mypy ***"
	@echo ""
	( mypy . )
	@echo ""

.PHONY: test
test:
	@echo ""
	@echo "*** unittest ***"
	@echo ""
	( pytest ./tests/ )
	@echo ""

.PHONY: cov-clean
cov-clean:
	@echo ""
	@echo "*** coverage-clean ***"
	@echo ""
	( rm -rf ./htmlcov )
	@echo ""

.PHONY: cov
cov:
	@echo ""
	@echo "*** coverage ***"
	@echo ""
	( coverage run -m pytest ./tests/ )
	@echo ""

.PHONY: html
html:
	@echo ""
	@echo "*** html report ***"
	@echo ""
	( coverage html )
	@echo ""

.PHONY: run
run:
	@echo ""
	@echo "*** run create_calendar.py ***"
	@echo ""
	( python3 create_calendar.py )
	@echo ""
