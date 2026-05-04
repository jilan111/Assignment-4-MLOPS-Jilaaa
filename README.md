# MLOps Pipeline with MLflow

Converts notebook-based ML experiments into a **structured, reproducible Python pipeline** with experiment tracking, automated reporting, and CI validation.

![Python](https://img.shields.io/badge/python-3.10+-blue)
![MLflow](https://img.shields.io/badge/tracking-MLflow-orange)
![GitHub Actions](https://img.shields.io/badge/CI-GitHub_Actions-blue)

---

## Pipeline

```
Data ──▶ Training ──▶ MLflow tracking ──▶ Artifacts ──▶ Report ──▶ CI validation
```

---

## What it does

- **Modular training scripts** — `train.py` and `run_experiments.py` replace exploratory notebooks
- **Experiment tracking** — every run logs hyperparameters, metrics, and artifacts to MLflow (`mlruns/`)
- **Artifact management** — outputs land in dedicated directories (`mlruns/`, `artifacts/`)
- **Automated reports** — structured summaries generated from experiment metadata
- **CI validation** — GitHub Actions runs the pipeline on every commit to catch regressions

---

## Quick start

```bash
git clone https://github.com/jilan111/mlops-pipeline-mlflow.git
cd mlops-pipeline-mlflow
pip install -r requirements.txt

# Single training run
python train.py

# Sweep multiple configurations
python run_experiments.py

# Inspect runs
mlflow ui
```

---

## Project structure

```
.
├── train.py                 # Single-run training script
├── run_experiments.py       # Multi-run experiment driver
├── artifacts/               # Generated reports & outputs
├── mlruns/                  # MLflow tracking store
└── .github/workflows/       # CI validation
```

---

## Tech stack

- Python 3.10+
- scikit-learn
- MLflow
- GitHub Actions

---

## Author

Built by **Jilan Ismail** — [GitHub](https://github.com/jilan111) · [LinkedIn](https://www.linkedin.com/in/jilan-ismail-596b2b2b2/)
