# CI/CD and Code Quality Fix Instructions

## Overview
This PR addresses issues with the CI/CD workflow and code quality in this repository. Due to GitHub security restrictions, workflow files (`.github/workflows/*`) require special permissions to be modified via API.

## Issues Identified

### 1. Pylint Workflow Failure
**Problem**: The pylint workflow fails because it doesn't install project dependencies before running pylint.

**Current Issue**:
- Only installs `pip` and `pylint`
- Missing project dependencies from `requirements.txt`
- Causes import errors during linting

### 2. Code Quality
Applied `autopep8` formatting for better code quality and PEP 8 compliance.

## Changes Required

### Workflow File to UPDATE:

#### `.github/workflows/pylint.yml`

Current problematic step:
```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install pylint
```

**Replace with:**
```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install pylint
    # Install project dependencies
    if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
```

### Complete Fixed Workflow File:
```yaml
name: Pylint

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.8", "3.9", "3.10"]
    steps:
    - uses: actions/checkout@v4
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pylint
        # Install project dependencies
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    - name: Analysing the code with pylint
      run: |
        pylint $(git ls-files '*.py')
```

## How to Apply These Changes

### Option 1: Via GitHub Web UI (Recommended)
1. Navigate to `.github/workflows/pylint.yml`
2. Click "Edit" button
3. Update the "Install dependencies" step as shown above
4. Commit changes to the `fix/ci-quality-api` branch

### Option 2: Via Git Command Line
```bash
git checkout fix/ci-quality-api
# Edit .github/workflows/pylint.yml with the changes above
git add .github/workflows/pylint.yml
git commit -m "Fix pylint workflow: install project dependencies"
git push origin fix/ci-quality-api
```

## Code Quality Improvements Applied

The following Python files have been reformatted with `autopep8` for PEP 8 compliance:
- ✅ `main.py` - Improved function definitions and spacing
- ✅ `train.py` - Better argument formatting
- ✅ `infer.py` - Enhanced readability
- ✅ `prepare_data.py` - Cleaner code structure

## Expected Results

After applying these changes:
- ✅ Pylint workflow will pass successfully
- ✅ Dependencies will be installed before linting
- ✅ Import errors will be resolved
- ✅ Code quality checks will run on every push/PR
- ✅ Better code maintainability

## Need Help?

If you need the AbacusAI bot to automatically apply these changes, please:
1. Go to https://github.com/apps/abacusai/installations/select_target
2. Add "Workflows: Read and write" permission
3. Re-run the automation

## Benefits

✅ **Working CI/CD**: Pylint workflow will execute successfully  
✅ **Improved Code Quality**: PEP 8 compliant formatting  
✅ **Better Readability**: Consistent code style  
✅ **Professional Standards**: Following Python best practices
