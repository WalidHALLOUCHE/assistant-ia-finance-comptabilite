# Makefile for Enterprise AI Accounting & Finance Assistant

.PHONY: help install install-dev run test clean lint format

help:
	@echo "📋 Available Commands:"
	@echo ""
	@echo "  make install       - Install dependencies"
	@echo "  make install-dev   - Install with dev tools"
	@echo "  make run           - Run Streamlit app"
	@echo "  make test          - Run tests"
	@echo "  make test-cov      - Tests with coverage"
	@echo "  make generate-data - Generate demo financial data"
	@echo "  make build-rag     - Build RAG vector store"
	@echo "  make lint          - Run linting checks"
	@echo "  make format        - Format code with black"
	@echo "  make clean         - Clean cache/build files"
	@echo ""

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

run:
	streamlit run app.py

test:
	pytest tests/ -v

test-cov:
	pytest tests/ -v --cov=src --cov-report=html

generate-data:
	python scripts/generate_demo_data.py

build-rag:
	python scripts/build_vector_store.py

lint:
	flake8 src/ tests/ app.py --max-line-length=120
	black --check src/ tests/ app.py

format:
	black src/ tests/ app.py

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/ .coverage htmlcov/
	rm -rf chroma_db/ .chroma/

setup-venv:
	python -m venv venv
	@echo "✅ Virtual environment created!"
	@echo "Activate it with: source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)"
