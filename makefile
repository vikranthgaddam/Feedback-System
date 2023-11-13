.PHONY: all env setup run clean

# Name of the virtual environment directory
VENV := venv

# Default target executed when no arguments are given to make
all: run

# Target for creating a virtual environment
env:
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install --upgrade pip

# Target for setting up the project dependencies
setup: env
	$(VENV)/bin/pip install -r requirements.txt

# Target for running the Python script
run: setup
	$(VENV)/bin/python server.py

# Target for cleaning up the project
clean:
	rm -rf __pycache__
	rm -rf $(VENV)


