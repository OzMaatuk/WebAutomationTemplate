# Project Structure Explained

## Configuration Files - What's What?

### 1. `setup.py` (Python Packaging) ✅
**Purpose**: Package metadata and installation configuration

**Contains**:
- Project metadata (name, version, description)
- Dependencies (from requirements.txt)
- Entry points
- Package discovery

**Why we use it**:
- ✅ Simple and familiar
- ✅ Works everywhere
- ✅ Easy to understand
- ✅ Industry standard

**Example**:
```python
setup(
    name="web-automation-template",
    version="1.0.0",
    install_requires=requirements,
)
```

---

### 2. `pyproject.toml` (Tool Configurations) ✅
**Purpose**: Configuration for development tools (black, ruff, mypy)

**Contains**:
- Black formatter settings
- Ruff linter settings
- Mypy type checker settings

**Why separate from setup.py**:
- ✅ Modern tools expect it
- ✅ Cleaner than putting in setup.cfg
- ✅ Standard location for tool configs

**Example**:
```toml
[tool.black]
line-length = 100

[tool.ruff]
select = ["E", "F", "I"]
```

---

### 3. `pytest.ini` (Pytest Configuration) ✅
**Purpose**: Pytest-specific configuration

**Contains**:
- Test discovery patterns
- Command-line options
- Test markers
- Pytest-specific settings

**Why separate file**:
- ✅ Clearer separation of concerns
- ✅ Easier to find pytest config
- ✅ Traditional pytest convention
- ✅ Could be in pyproject.toml but cleaner here

**Example**:
```ini
[pytest]
testpaths = tests
addopts = --verbose --tb=short
```

**Alternative**: Could move to `pyproject.toml` as `[tool.pytest.ini_options]`

---

### 3. `requirements.txt` (Dependency List) ✅
**Purpose**: Simple list of dependencies for pip install

**Contains**:
- Direct dependencies with versions
- Used by: `pip install -r requirements.txt`

**Why we keep it**:
- ✅ Simple and familiar
- ✅ Works everywhere (Docker, CI/CD)
- ✅ Easy to read
- ✅ Can be generated from pyproject.toml

**Note**: Technically redundant with pyproject.toml, but useful for:
- Docker builds
- Quick installs
- CI/CD pipelines
- Developers who prefer it

---

### 4. `config.ini` (Application Configuration) ✅
**Purpose**: Runtime application settings

**Contains**:
- Base URL
- Browser settings
- Timeouts
- Directories

**Why separate**:
- ✅ Runtime config, not build config
- ✅ Can be different per environment
- ✅ Easy to modify without code changes

---

### 5. `.env` (Secrets & Environment Variables) ✅
**Purpose**: Sensitive configuration and environment-specific values

**Contains**:
- Credentials (username, password)
- API keys
- Environment-specific URLs

**Why separate**:
- ✅ Never committed to git
- ✅ Different per environment
- ✅ Security best practice

---

## What We Removed

### ❌ `setup.py` (Deleted - Redundant)
**Was**: Legacy Python packaging file  
**Why removed**: Completely replaced by `pyproject.toml`

**Old way** (setup.py):
```python
setup(
    name="web-automation-template",
    version="1.0.0",
    install_requires=["playwright>=1.48.0"],
)
```

**New way** (pyproject.toml):
```toml
[project]
name = "web-automation-template"
version = "1.0.0"
dependencies = ["playwright>=1.48.0"]
```

---

## File Hierarchy & Purpose

```
Configuration Files:
├── pyproject.toml       → Project metadata + tool configs (BUILD TIME)
├── pytest.ini           → Pytest configuration (TEST TIME)
├── requirements.txt     → Dependency list (INSTALL TIME)
├── config.ini           → Application settings (RUN TIME)
└── .env                 → Secrets & environment vars (RUN TIME)

Code Files:
├── main.py              → Entry point
├── driver.py            → Browser driver
├── logger.py            → Logging setup
├── pages/               → Page objects
├── controller/          → Workflow logic
├── constants/           → Configuration & selectors
├── utils/               → Utilities
└── tests/               → Test suite
```

---

## When to Use What?

### Adding a Python Dependency
```bash
# 1. Add to pyproject.toml
[project]
dependencies = ["requests>=2.31.0"]

# 2. Update requirements.txt
echo "requests>=2.31.0" >> requirements.txt

# 3. Install
pip install -e .
# or
pip install -r requirements.txt
```

### Configuring a Tool (black, ruff, mypy)
```toml
# Add to pyproject.toml
[tool.black]
line-length = 100
```

### Configuring Pytest
```ini
# Add to pytest.ini
[pytest]
addopts = --verbose
```

### Application Settings
```ini
# Add to config.ini
[Settings]
timeout = 30000
```

### Secrets
```bash
# Add to .env (never commit!)
APP_USERNAME=myuser
APP_PASSWORD=mypass
```

---

## Modern Python Best Practices (2024)

### ✅ DO:
- Use `pyproject.toml` for project metadata
- Use `pyproject.toml` for tool configurations
- Keep `pytest.ini` separate (optional but cleaner)
- Keep `requirements.txt` for compatibility
- Use `.env` for secrets

### ❌ DON'T:
- Don't use `setup.py` (unless you need backward compatibility)
- Don't duplicate config between files
- Don't commit `.env` to git
- Don't put secrets in `config.ini`

---

## Installation Methods

### Method 1: Development Install (Recommended)
```bash
pip install -e .
```
Uses `pyproject.toml` to install package in editable mode.

### Method 2: Requirements File
```bash
pip install -r requirements.txt
```
Simple dependency installation.

### Method 3: With Optional Dependencies
```bash
pip install -e ".[dev]"      # Install with dev tools
pip install -e ".[test]"     # Install with test tools
```

---

## Summary

| File | Purpose | When to Edit |
|------|---------|--------------|
| `pyproject.toml` | Project metadata, dependencies, tool configs | Adding dependencies, configuring tools |
| `pytest.ini` | Pytest configuration | Changing test behavior |
| `requirements.txt` | Dependency list | Adding/updating dependencies |
| `config.ini` | Application settings | Changing runtime behavior |
| `.env` | Secrets | Setting credentials |

**Key Point**: We removed `setup.py` because `pyproject.toml` does everything it did, but better and more modern.
