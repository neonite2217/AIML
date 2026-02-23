.PHONY: install test clean run help

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make test       - Run tests"
	@echo "  make run        - Run the clustering script"
	@echo "  make clean      - Clean generated files"

install:
	python3 -m venv venv
	./venv/bin/pip install -r requirements.txt

test:
	./venv/bin/python -m pytest tests/ -v

run:
	./venv/bin/python geospatial_clustering.py

clean:
	rm -f *.png *.html *.csv
	rm -rf __pycache__ .pytest_cache
