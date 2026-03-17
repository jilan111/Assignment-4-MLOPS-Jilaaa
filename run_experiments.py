"""
Run a series of training runs with different hyperparameters.
This script calls `train.py` multiple times (does not run MLflow UI).
"""
import subprocess
import sys

experiments = [
    {"learning_rate": 0.1, "batch_size": 64},
    {"learning_rate": 0.01, "batch_size": 64},
    {"learning_rate": 0.001, "batch_size": 64},
    {"learning_rate": 0.01, "batch_size": 128},
    {"learning_rate": 0.005, "batch_size": 32},
]

EXPERIMENT_NAME = "Assignment3_JilanIsmail_202201997"
STUDENT_ID = "202201997"

for i, cfg in enumerate(experiments, 1):
    cmd = [
        sys.executable,
        "train.py",
        "--learning_rate",
        str(cfg["learning_rate"]),
        "--batch_size",
        str(cfg["batch_size"]),
        "--epochs",
        "8",
        "--experiment_name",
        EXPERIMENT_NAME,
        "--student_id",
        STUDENT_ID,
    ]
    print(f"Running experiment {i}: lr={cfg['learning_rate']} bs={cfg['batch_size']}")
    subprocess.run(cmd)
