# MLOps Pipeline for Machine Learning Experiments

### Assignment 4 -- CI Enabled ML Workflow

![CI](https://img.shields.io/badge/CI-GitHub%20Actions-success)
![Python](https://img.shields.io/badge/Python-3.10-blue)
![MLOps](https://img.shields.io/badge/MLOps-Pipeline-orange)
![MLflow](https://img.shields.io/badge/Experiment%20Tracking-MLflow-purple)

------------------------------------------------------------------------

# Project Overview

This project implements a **Machine Learning Operations (MLOps)
pipeline** that extends the work developed in **Assignment 3**.

The goal of this assignment is to transform an experimental ML workflow
into a **reproducible, automated machine learning pipeline** using
modern **MLOps practices**.

The pipeline supports:

-   Automated model training
-   Experiment tracking
-   Artifact management
-   Automated report generation
-   Continuous Integration (CI)

The entire pipeline is validated automatically using **GitHub Actions**,
ensuring reproducibility and reliability across runs.

------------------------------------------------------------------------

# Objectives

The main objectives of this assignment are:

• Convert notebook-based ML experiments into structured Python scripts\
• Implement experiment tracking using MLflow\
• Automate experiment reporting\
• Create a reproducible ML workflow\
• Integrate CI to validate the ML pipeline automatically

------------------------------------------------------------------------

# Project Architecture

The system follows a simple **MLOps pipeline architecture**:

Data → Training Script → Experiment Tracking → Artifact Generation →
Report Generation → CI Validation

Each stage is automated and integrated into the CI pipeline.

------------------------------------------------------------------------

# Project Structure

    .
    ├── train.py
    │   Model training script
    │
    ├── run_experiments.py
    │   Runs multiple ML experiments
    │
    ├── generate_report.py
    │   Generates experiment summary reports
    │
    ├── assemble_report.py
    │   CI-safe script that assembles reports and prevents CI failures
    │
    ├── create_pdf.py
    │   Converts generated reports into PDF format
    │
    ├── generate_pdf_simple.py
    │   Alternative simplified PDF generation script
    │
    ├── report.md
    │   Automatically generated experiment report
    │
    ├── artifacts/
    │   Stored experiment artifacts and outputs
    │
    ├── report_artifacts/
    │   Files used during report generation
    │
    ├── mlruns/
    │   MLflow experiment tracking directory
    │
    ├── requirements.txt
    │   Project dependencies
    │
    ├── .github/workflows/
    │   CI pipeline configuration
    │
    └── Assignment3_notebook.ipynb
        Original experimentation notebook from Assignment 3

------------------------------------------------------------------------

# Machine Learning Pipeline

The pipeline executes the following steps:

### 1 Data Loading

Load dataset and preprocess it for training.

### 2 Model Training

Train the machine learning model using `train.py`.

### 3 Experiment Execution

Run multiple experiments:

``` bash
python run_experiments.py
```

### 4 Experiment Tracking

All runs are tracked using **MLflow**, storing:

-   hyperparameters
-   training metrics
-   artifacts
-   model outputs

Results are stored in:

    mlruns/

### 5 Artifact Generation

The pipeline generates experiment artifacts such as:

-   trained models
-   experiment outputs
-   result files

Artifacts are stored in:

    artifacts/

### 6 Report Generation

Experiment results are summarized into a structured report:

    report.md

Reports include:

-   experiment runs
-   metrics
-   model information
-   generated artifacts

------------------------------------------------------------------------

# Automated Report Assembly

The script:

    assemble_report.py

was designed specifically for **CI stability**.

Responsibilities:

• Collect experiment results\
• Generate a default report if no results exist\
• Prevent pipeline failure if artifacts are missing\
• Ensure the CI pipeline always completes successfully

If no experiment results are found, the report generator safely outputs:

    No results available

------------------------------------------------------------------------

# Continuous Integration Pipeline

The project integrates **Continuous Integration (CI)** using **GitHub
Actions**.

The CI workflow performs the following steps automatically:

1.  Checkout repository\
2.  Setup Python environment\
3.  Install dependencies\
4.  Run linter checks\
5.  Validate ML pipeline scripts\
6.  Assemble experiment reports

This guarantees that the pipeline runs successfully for every commit.

------------------------------------------------------------------------

# Running the Project Locally

### Clone the Repository

``` bash
git clone <repository-url>
cd mlops-assignment
```

### Install Dependencies

``` bash
pip install -r requirements.txt
```

### Run Experiments

``` bash
python run_experiments.py
```

### Generate Reports

``` bash
python generate_report.py
```

or

``` bash
python assemble_report.py
```

------------------------------------------------------------------------

# Generated Outputs

  Output          Description
  --------------- -----------------------------
  `mlruns/`       Experiment tracking data
  `artifacts/`    Model outputs and artifacts
  `report.md`     Experiment summary report
  `PDF reports`   Optional generated reports

------------------------------------------------------------------------

# Assignment Context

This repository builds upon **Assignment 3**, where the machine learning
workflow was initially implemented using a notebook.

In **Assignment 4**, the focus shifts toward **MLOps best practices**,
including:

• Code modularization\
• Experiment tracking\
• Automated reporting\
• Continuous Integration\
• Reproducible ML pipelines

------------------------------------------------------------------------

# Future Improvements

Potential enhancements for the pipeline include:

• Model deployment pipeline\
• Automated model evaluation dashboards\
• Data validation pipelines\
• Containerization using Docker\
• Integration with cloud experiment tracking

------------------------------------------------------------------------

# Key MLOps Concepts Demonstrated

This project demonstrates several important **MLOps practices**:

-   ML experiment tracking
-   CI for ML pipelines
-   artifact management
-   automated reporting
-   reproducible training workflows

------------------------------------------------------------------------

# Author
Jilan Ismail
MLOps Assignment Project\
Assignment 4 -- Machine Learning Operations Pipeline
