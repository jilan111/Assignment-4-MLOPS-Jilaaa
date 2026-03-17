# Assignment 3 — Observable ML with MLflow

Steps to reproduce and run experiments:

1. Create a reproducible environment (conda or venv) and install dependencies:

```bash
pip install -r requirements.txt
```

2. Launch the MLflow UI in a separate terminal:

```bash
mlflow ui --port 5000
# then open http://localhost:5000
```

3. Run experiments (this will execute `train.py` multiple times):

```bash
python run_experiments.py
```

4. In the MLflow UI:
-- Set experiment name: `Assignment3_JilanIsmail_202201997` (the scripts now default to your name/ID)
- Compare runs, view learning curves, and open the Artifacts tab to inspect saved `model` and `MLmodel` files.

Notes:
- Update `student_id` parameter in `train.py` or pass `--student_id` via command line to tag runs with your ID.
- The training script uses MNIST and logs `train_loss`, `train_accuracy`, `val_loss`, and `val_accuracy` per epoch.
