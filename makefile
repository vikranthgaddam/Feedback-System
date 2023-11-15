.PHONY: all setup clean

# Name of the virtual environment directory
VENV := venv

# Default target executed when no arguments are given to make
all: setup

# Target for setting up the project dependencies, including creating the virtual environment
setup:
	@test -d $(VENV) || python3 -m venv $(VENV)
	@$(VENV)/bin/pip install --upgrade pip
	@$(VENV)/bin/pip install contourpy==1.2.0
	@$(VENV)/bin/pip install cycler==0.12.1
	@$(VENV)/bin/pip install fonttools==4.44.0
	@$(VENV)/bin/pip install kiwisolver==1.4.5
	@$(VENV)/bin/pip install matplotlib==3.8.1
	@$(VENV)/bin/pip install numpy==1.26.1
	@$(VENV)/bin/pip install packaging==23.2
	@$(VENV)/bin/pip install Pillow==10.1.0
	@$(VENV)/bin/pip install pyparsing==3.1.1
	@$(VENV)/bin/pip install python-dateutil==2.8.2
	@$(VENV)/bin/pip install six==1.16.0

# Target for cleaning up the project
clean:
	rm -rf __pycache__
	rm -rf $(VENV)
