import argparse
import os
from mlflow.tracking import MlflowClient
import matplotlib.pyplot as plt
import pandas as pd


def fetch_runs(experiment_name, top_k=3):
    client = MlflowClient()
    exp = client.get_experiment_by_name(experiment_name)
    if exp is None:
        raise ValueError(f"Experiment '{experiment_name}' not found")
    runs = client.search_runs(exp.experiment_id)
    # compute best val_accuracy per run
    run_scores = []
    for r in runs:
        metrics = r.data.metrics
        if "val_accuracy" in metrics:
            run_scores.append((r.info.run_id, metrics.get("val_accuracy")))
        else:
            # fallback: 0
            run_scores.append((r.info.run_id, 0.0))
    run_scores.sort(key=lambda x: x[1], reverse=True)
    return [rid for rid, _ in run_scores[:top_k]]


def plot_metric(experiment_name, run_ids, metric_key="val_accuracy", out_path="report_accuracy.png"):
    client = MlflowClient()
    plt.figure(figsize=(8, 5))
    for rid in run_ids:
        hist = client.get_metric_history(rid, metric_key)
        if not hist:
            continue
        # sort by step
        df = pd.DataFrame([{"step": m.step, "value": m.value} for m in hist])
        df = df.sort_values("step")
        plt.plot(df["step"], df["value"], marker="o", label=rid[:8])

    plt.xlabel("Epoch")
    plt.ylabel(metric_key)
    plt.title(f"{metric_key} across runs")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    os.makedirs("report_artifacts", exist_ok=True)
    out_file = os.path.join("report_artifacts", out_path)
    plt.savefig(out_file)
    print(f"Saved plot to {out_file}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment", type=str, default="Assignment3_YourName")
    parser.add_argument("--top_k", type=int, default=3)
    args = parser.parse_args()

    run_ids = fetch_runs(args.experiment, top_k=args.top_k)
    if not run_ids:
        print("No runs found for experiment")
        return
    plot_metric(args.experiment, run_ids, metric_key="val_accuracy", out_path="report_val_accuracy.png")
    plot_metric(args.experiment, run_ids, metric_key="val_loss", out_path="report_val_loss.png")


if __name__ == "__main__":
    main()
