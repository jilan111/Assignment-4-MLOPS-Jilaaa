# GitHub Actions Pipeline - Bug Report and Fixes

**Date:** March 17, 2026  
**Assignment:** ML Model CI Pipeline

---

## Executive Summary

This report documents all bugs found in the initial GitHub Actions workflow YAML file and provides detailed solutions for each issue. The corrected workflow file ensures proper CI/CD automation for the ML model training pipeline.

---

## Bugs Identified and Fixed

### Bug #1: Missing Repository Checkout Step

**Severity:** CRITICAL ✗

**Original Issue:**
The workflow lacks the essential `actions/checkout@v4` step. Without checking out the repository code, the subsequent steps cannot access the source files needed for linting, testing, or dependency installation.

**Original Code (Missing):**
```yaml
# Step was completely absent from the workflow
```

**Fixed Code:**
```yaml
- name: Checkout Repository
  uses: actions/checkout@v4
```

**Explanation:**
The `actions/checkout@v4` action is mandatory as the first step in any CI/CD workflow that needs access to repository files. It clones the repository code into the runner's working directory.

---

### Bug #2: Improper YAML Indentation in `on:` Trigger Block

**Severity:** HIGH ✗

**Original Issue:**
The `on:` section has incorrect indentation, which breaks YAML syntax:
```yaml
on:
push:           # ❌ Should be indented under 'on:'
branches: main  # ❌ Should be indented under 'push:'
pull_request:   # ❌ Incorrectly formatted
```

**Fixed Code:**
```yaml
on:
  push:
    branches:
      - '**'
      - '!main'
  pull_request:
```

**Explanation:**
YAML requires proper indentation to denote hierarchical structure. The `push:` and `pull_request:` should be indented under `on:`. The `branches:` field is a list in YAML and must use proper list syntax with `-` markers.

---

### Bug #3: Incomplete "Linter Check" Step

**Severity:** HIGH ✗

**Original Issue:**
```yaml
- name: Linter Check
# ❌ Missing 'run:' command - step does nothing
```

The step has a name but no actual command to execute. This violates GitHub Actions syntax where each step must have either a `uses:` or `run:` field.

**Fixed Code:**
```yaml
- name: Linter Check
  run: python -m py_compile train.py run_experiments.py generate_report.py assemble_report.py
```

**Explanation:**
The fixed version uses Python's built-in `py_compile` module to check for syntax errors in all Python scripts. This ensures code quality before proceeding with more expensive operations.

---

### Bug #4: Incorrect Branch Trigger Logic

**Severity:** MEDIUM ✗

**Original Issue:**
```yaml
on:
  push:
    branches: main  # ❌ Only triggers on main branch
```

The requirement was to run on every push for ALL branches EXCEPT `main`, but the original only triggers on `main`.

**Fixed Code:**
```yaml
on:
  push:
    branches:
      - '**'        # Include all branches
      - '!main'     # Exclude main
  pull_request:     # Also run on PRs
```

**Explanation:**
Using `'**'` matches all branches, and `'!main'` excludes the main branch. This ensures the pipeline runs on development/feature branches for early validation while protecting the main branch with its own specific rules.

---

### Bug #5: Missing Artifact Upload Step

**Severity:** MEDIUM ✗

**Original Issue:**
The workflow lacks the final step to upload documentation as an artifact. Project documentation wasn't being preserved across workflow runs.

**Original Code (Missing):**
```yaml
# No artifact upload step present
```

**Fixed Code:**
```yaml
- name: Upload Project Documentation
  uses: actions/upload-artifact@v3
  with:
    name: project-doc
    path: README.md
```

**Explanation:**
The `actions/upload-artifact@v3` action stores the README.md file as a workflow artifact named `project-doc`. This preserves documentation and makes it available for download from the GitHub Actions tab.

---

### Bug #6: Inconsistent Step Indentation and Structure

**Severity:** MEDIUM ✗

**Original Issue:**
The workflow has inconsistent step structure. Some steps lack proper naming or use:
```yaml
- name: Set up Python
uses: actions/setup-python@v5  # ❌ Wrong indentation
with:
python-version: '3.10'         # ❌ Wrong indentation
```

**Fixed Code:**
```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.10'
```

**Explanation:**
All fields under a step must be properly indented. The `uses:` and `with:` keys need consistent indentation relative to the step, using two spaces per indentation level.

---

## Summary of Changes

| Bug # | Issue | Fix Type | Status |
|-------|-------|----------|--------|
| 1 | Missing checkout action | Addition | ✅ Fixed |
| 2 | YAML indentation errors in `on:` | Syntax correction | ✅ Fixed |
| 3 | Incomplete linter check | Addition | ✅ Fixed |
| 4 | Wrong branch trigger logic | Logic correction | ✅ Fixed |
| 5 | Missing artifact upload | Addition | ✅ Fixed |
| 6 | Inconsistent step indentation | Syntax correction | ✅ Fixed |

---

## Corrected Workflow Features

The final corrected workflow includes:

✅ **Automated repository checkout** for code access  
✅ **Python 3.10 setup** for consistent environment  
✅ **Dependency installation** from requirements.txt  
✅ **Linter checks** using Python's py_compile  
✅ **Environment validation** with PyTorch import test  
✅ **Documentation artifact upload** for project-doc  
✅ **Smart branch triggering** (all branches except main)  
✅ **Pull request support** for code review workflows  

---

## Corrected Workflow Code

```yaml
# .github/workflows/ml-pipeline.yml
name: ML Model CI

on:
  push:
    branches:
      - '**'
      - '!main'
  pull_request:

jobs:
  validate-and-test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Install Dependencies
        run: pip install -r requirements.txt

      - name: Linter Check
        run: python -m py_compile train.py run_experiments.py generate_report.py assemble_report.py

      - name: Model Dry Test
        run: |
          python -c "import torch; print('Model environment ready!')"

      - name: Upload Project Documentation
        uses: actions/upload-artifact@v3
        with:
          name: project-doc
          path: README.md
```

---

## Testing Recommendations

1. **Initialize Git Repository**: Run `git init` and add your remote
2. **Push to a Feature Branch**: Create and push to a branch other than main to verify the trigger works
3. **Check the Actions Tab**: Monitor the GitHub Actions tab for successful Green checkmarks
4. **Verify Artifacts**: Confirm that the `project-doc` artifact appears in workflow run details
5. **Test Pull Request Trigger**: Create a test PR to verify PR trigger works

---

## Key Improvements Over Original

| Aspect | Original | Corrected |
|--------|----------|-----------|
| **Code Checkout** | ❌ Missing | ✅ Present with `actions/checkout@v4` |
| **YAML Syntax** | ❌ Broken indentation | ✅ Proper 2-space indentation |
| **Linter Check** | ❌ Incomplete (no run command) | ✅ Complete with py_compile validation |
| **Branch Trigger** | ❌ Only main branch | ✅ All branches except main |
| **Artifact Upload** | ❌ Missing | ✅ Uploads README.md as project-doc |
| **Step Structure** | ❌ Inconsistent | ✅ Consistent indentation throughout |

---

## References

- [GitHub Actions Checkout Documentation](https://github.com/actions/checkout)
- [GitHub Actions Setup Python Documentation](https://github.com/actions/setup-python)
- [GitHub Actions Upload Artifact Documentation](https://github.com/actions/upload-artifact)
- [YAML Syntax Guide](https://yaml.org/spec/1.2/spec.html)
- [GitHub Actions Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)

---

*Report Generated: March 17, 2026*  
*Status: All Bugs Fixed and Documented* ✅
