.PHONY: install build test site-build site-dev pipeline

install:
	python -m pip install -e .[dev]
	cd site && npm install

build: pipeline site-build

pipeline:
	python -m pipeline.index

site-build:
	cd site && npm run build

site-dev:
	cd site && npm run dev -- --host 0.0.0.0

test:
	python -m pytest
	cd site && npm run check
