import argparse
import os
from mlflow.tracking import MlflowClient
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def collect_run_table(experiment_name):
    client = MlflowClient()
    exp = client.get_experiment_by_name(experiment_name)
    if exp is None:
        raise ValueError(f"Experiment '{experiment_name}' not found")
    runs = client.search_runs(exp.experiment_id)
    rows = []
    for r in runs:
        params = r.data.params
        metrics = r.data.metrics
        tags = r.data.tags
        # get best val_accuracy from metric history if available
        try:
            val_acc = metrics.get("val_accuracy", 0.0)
        except Exception:
            val_acc = 0.0
        rows.append({
            "run_id": r.info.run_id,
            "status": r.info.status,
            "start_time": r.info.start_time,
            "val_accuracy": val_acc,
            "learning_rate": params.get("learning_rate"),
            "batch_size": params.get("batch_size"),
            "epochs": params.get("epochs"),
            "student_id": tags.get("student_id"),
        })
    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values("val_accuracy", ascending=False)
    return df


def list_artifacts_for_runs(run_ids):
    client = MlflowClient()
    artifacts = {}
    for rid in run_ids:
        try:
            files = client.list_artifacts(rid, path="")
            artifacts[rid] = [f.path for f in files]
        except Exception:
            artifacts[rid] = []
    return artifacts


def make_table_page(df, pdf):
    fig, ax = plt.subplots(figsize=(11, 8.5))
    ax.axis('off')
    if df.empty:
        ax.text(0.5, 0.5, 'No runs found', ha='center', va='center')
    else:
        table = ax.table(cellText=df.head(20).values, colLabels=df.columns, loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(8)
        table.scale(1, 1.5)
    pdf.savefig(fig)
    plt.close(fig)


def make_text_page(title, lines, pdf):
    fig, ax = plt.subplots(figsize=(11, 8.5))
    ax.axis('off')
    ax.set_title(title, fontsize=16)
    y = 0.9
    for line in lines:
        ax.text(0.05, y, line, fontsize=11, va='top')
        y -= 0.05
    pdf.savefig(fig)
    plt.close(fig)


def add_image_page(img_path, pdf, title=None):
    fig, ax = plt.subplots(figsize=(11, 8.5))
    ax.axis('off')
    if title:
        ax.set_title(title)
    img = plt.imread(img_path)
    ax.imshow(img)
    pdf.savefig(fig)
    plt.close(fig)


def analyze_winner(df, experiment_name):
    if df.empty:
        return "No runs to analyze"
    winner = df.iloc[0]
    rid = winner.run_id
    client = MlflowClient()
    # fetch train/val accuracy histories
    try:
        train_hist = client.get_metric_history(rid, "train_accuracy")
        val_hist = client.get_metric_history(rid, "val_accuracy")
    except Exception:
        return f"Winner run: {rid[:8]} (val_accuracy={winner.val_accuracy})"

    train_vals = [m.value for m in train_hist]
    val_vals = [m.value for m in val_hist]
    if not train_vals or not val_vals:
        return f"Winner run: {rid[:8]} (val_accuracy={winner.val_accuracy})"

    final_train = train_vals[-1]
    final_val = val_vals[-1]
    gap = final_train - final_val
    analysis = [f"Winner run: {rid} (val_accuracy={winner.val_accuracy})",
                f"Final train_accuracy={final_train:.4f}",
                f"Final val_accuracy={final_val:.4f}",
                f"Train - Val gap={gap:.4f}"]
    if gap > 0.02:
        analysis.append("Evidence: small overfitting (train > val by > 0.02)")
    else:
        analysis.append("No strong overfitting detected")
    return "\n".join(analysis)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--experiment", type=str, default="Assignment3_YourName")
    parser.add_argument("--out", type=str, default="Assignment3_report.pdf")
    args = parser.parse_args()

    df = collect_run_table(args.experiment)
    top_runs = df.run_id.tolist()[:3] if not df.empty else []
    artifacts = list_artifacts_for_runs(top_runs)

    with PdfPages(args.out) as pdf:
        # Title page
        make_text_page("Assignment 3 — MLflow Experiment Report", [f"Experiment: {args.experiment}", ""], pdf)
        # Table of runs
        make_table_page(df, pdf)
        # Add generated comparison plots if they exist
        acc_img = os.path.join("report_artifacts", "report_val_accuracy.png")
        loss_img = os.path.join("report_artifacts", "report_val_loss.png")
        if os.path.exists(acc_img):
            add_image_page(acc_img, pdf, title="Validation Accuracy Comparison")
        if os.path.exists(loss_img):
            add_image_page(loss_img, pdf, title="Validation Loss Comparison")

        # Artifacts list
        lines = []
        for rid, files in artifacts.items():
            lines.append(f"Run {rid[:8]} artifacts:")
            if files:
                for f in files:
                    lines.append(f"  - {f}")
            else:
                lines.append("  (no artifacts found)")
            lines.append("")
        if not lines:
            lines = ["No artifacts available for top runs"]
        make_text_page("Artifacts", lines, pdf)

        # Analysis page
        analysis = analyze_winner(df, args.experiment)
        make_text_page("Short Analysis", analysis.splitlines(), pdf)

    print(f"Saved PDF report to {args.out}")


if __name__ == "__main__":
    main()
