# Makefile for common development tasks

.PHONY: help install test lint format clean run docker-build docker-run

help:
	@echo "Available commands:"
	@echo "  make install       - Install dependencies"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Run linters"
	@echo "  make format        - Format code"
	@echo "  make clean         - Clean generated files"
	@echo "  make run           - Run the application"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-run    - Run Docker container"

install:
	pip install -r requirements.txt
	playwright install chromium

test:
	pytest -v

test-coverage:
	pytest --cov=. --cov-report=html --cov-report=term

lint:
	@echo "Running ruff..."
	ruff check .
	@echo "Running mypy..."
	mypy .

format:
	black .
	ruff check --fix .

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf htmlcov .coverage
	rm -rf logs/*.log
	rm -rf screenshots/*.png

run:
	python main.py

docker-build:
	docker build -t web-automation .

docker-run:
	docker run --env-file .env web-automation
