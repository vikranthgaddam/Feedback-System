.PHONY: all setup clean

# Name of the virtual environment directory
VENV := venv

# Default target executed when no arguments are given to make
all: setup

# Target for setting up the project dependencies, including creating the virtual environment
setup:
	@test -d $(VENV) || python3 -m venv $(VENV)
	@$(VENV)/bin/pip install --upgrade pip
	@$(VENV)/bin/pip install -r requirements.txt

# Target for cleaning up the project
clean:
	rm -rf __pycache__
	rm -rf $(VENV)
