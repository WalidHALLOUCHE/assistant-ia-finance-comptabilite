# Contributing to Enterprise AI Accounting & Finance Assistant

Thank you for your interest in contributing! This document provides guidelines and instructions.

## 🎯 Ways to Contribute

### 1. Report Bugs
- Search existing issues first
- Provide detailed reproduction steps
- Include Python version, OS, and error messages
- Attach relevant logs

### 2. Suggest Features
- Describe the use case
- Explain the benefit
- Provide examples if possible
- Check if similar feature exists

### 3. Code Contributions
- Fix bugs
- Add analyzers for new domains
- Improve documentation
- Add tests
- Optimize performance

### 4. Documentation
- Improve README clarity
- Add use case examples
- Translate to other languages
- Create tutorials

## 📋 Getting Started

### 1. Fork & Clone
```bash
git clone https://github.com/your-username/enterprise-ai-accounting-finance-assistant.git
cd enterprise-ai-accounting-finance-assistant
```

### 2. Create Branch
```bash
git checkout -b feature/amazing-feature
# or
git checkout -b fix/bug-description
```

### 3. Setup Development Environment
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### 4. Make Changes
- Write clean, readable code
- Follow PEP 8 style guide
- Add docstrings to functions
- Update related tests

### 5. Run Tests
```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=src

# Specific test file
pytest tests/test_accounting_analyzer.py -v
```

### 6. Code Quality
```bash
# Format code
black src/ tests/ app.py

# Check style
flake8 src/ tests/ app.py

# Type checking
mypy src/ --ignore-missing-imports
```

### 7. Commit & Push
```bash
git add .
git commit -m "Add feature: description"
git push origin feature/amazing-feature
```

### 8. Create Pull Request
- Describe changes clearly
- Reference related issues
- Include test results
- Update documentation

## 🏗️ Code Organization

```
src/
├── Core Modules
│   ├── config.py ............ Configuration
│   ├── llm_provider.py ...... LLM abstraction
│   ├── data_loader.py ....... Data loading
│   └── rag_pipeline.py ...... RAG pipeline
│
├── Analyzers
│   ├── accounting_analyzer.py
│   ├── finance_analyzer.py
│   ├── supplier_accounting.py
│   ├── treasury_analyzer.py
│   └── quality_checker.py
│
└── Utilities
    ├── security.py
    ├── management_commentary.py
    └── prompt_templates.py
```

## ✅ Guidelines

### Code Style
- Follow PEP 8
- Use type hints
- Write docstrings
- Keep functions focused
- Maximum 100 lines per function

### Testing
- Write tests for new features
- Update existing tests if you modify code
- Aim for >80% coverage
- Test edge cases and errors

### Documentation
- Update README if adding features
- Document public methods
- Add examples where useful
- Keep docs in sync with code

### Commits
- Write clear commit messages
- Use imperative mood ("Add feature" not "Added feature")
- Reference issues: "Fixes #123"
- Keep commits focused

### PR Review
- All tests must pass
- Code review required
- At least one approval before merge
- Address review comments

## 🔍 Code Review Checklist

Before submitting PR:
- [ ] Tests added/updated
- [ ] Code formatted with black
- [ ] No linting errors (flake8)
- [ ] Docstrings added
- [ ] README updated if needed
- [ ] CHANGELOG updated
- [ ] No debug prints or commented code
- [ ] No secrets or credentials in code

## 📚 Architecture Considerations

When adding new features:

### New Analyzer?
1. Inherit from base pattern
2. Add to `initialize_analyzers()`
3. Create corresponding page in `app.py`
4. Add unit tests in `tests/`
5. Document in Power BI if applicable

### New Data Source?
1. Add CSV loader to `data_loader.py`
2. Add dimension table if applicable
3. Update data dictionary
4. Extend analyzers to use new data

### New LLM Feature?
1. Add prompt to `prompt_templates.py`
2. Update `llm_provider.py` if needed
3. Handle API errors gracefully
4. Test with fallback provider

## 🚀 Deployment Contribution

For deployment improvements:
1. Update `Dockerfile` or docker-compose
2. Test locally with Docker
3. Update DEPLOYMENT.md
4. Verify in Streamlit Cloud

## 📝 Documentation Contribution

For doc improvements:
1. Fix typos and clarity
2. Add missing sections
3. Update examples
4. Check formatting

## 🙏 Contribution Process

1. **Pick an issue** or create one
2. **Discuss approach** (optional but recommended)
3. **Fork & develop** on your branch
4. **Test locally** (unit + manual)
5. **Submit PR** with clear description
6. **Respond to review** feedback
7. **Merge** after approval

## ⚖️ License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🆘 Need Help?

- Check existing issues/discussions
- Read the README and documentation
- Review similar code in the repository
- Ask in pull request comments

## 🎓 Learning Resources

- [PEP 8 Style Guide](https://pep8.org/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Git Documentation](https://git-scm.com/doc)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

## 🙌 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors graph

## 💡 Ideas Welcome!

Have ideas for improvements? 
- Open an issue with label "enhancement"
- Describe the problem and proposed solution
- Discuss tradeoffs and implementation approach

---

**Thank you for making this project better! ⭐**
