import argparse
import os
import random
import mlflow
import mlflow.pytorch
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader


class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.net = nn.Sequential(
            nn.Conv2d(1, 32, 3, 1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, 3, 1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(64 * 5 * 5, 128),
            nn.ReLU(),
            nn.Linear(128, 10),
        )

    def forward(self, x):
        return self.net(x)


def set_seed(seed=42):
    random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def train_one_epoch(model, device, loader, criterion, optimizer):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    for data, target in loader:
        data, target = data.to(device), target.to(device)
        optimizer.zero_grad()
        out = model(data)
        loss = criterion(out, target)
        loss.backward()
        optimizer.step()
        running_loss += loss.item() * data.size(0)
        preds = out.argmax(dim=1)
        correct += (preds == target).sum().item()
        total += data.size(0)
    return running_loss / total, correct / total


def validate(model, device, loader, criterion):
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    with torch.no_grad():
        for data, target in loader:
            data, target = data.to(device), target.to(device)
            out = model(data)
            loss = criterion(out, target)
            running_loss += loss.item() * data.size(0)
            preds = out.argmax(dim=1)
            correct += (preds == target).sum().item()
            total += data.size(0)
    return running_loss / total, correct / total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--learning_rate", type=float, default=0.01)
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch_size", type=int, default=64)
    parser.add_argument("--student_id", type=str, default="202201997")
    parser.add_argument("--experiment_name", type=str, default="Assignment3_JilanIsmail_202201997")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    # Reproducibility
    set_seed(args.seed)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # MLflow experiment
    mlflow.set_experiment(args.experiment_name)
    with mlflow.start_run():
        # Log params and tag
        mlflow.log_param("learning_rate", args.learning_rate)
        mlflow.log_param("epochs", args.epochs)
        mlflow.log_param("batch_size", args.batch_size)
        mlflow.set_tag("student_id", args.student_id)

        # Datasets
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.1307,), (0.3081,)),
        ])
        train_ds = datasets.MNIST("./data", train=True, download=True, transform=transform)
        val_ds = datasets.MNIST("./data", train=False, download=True, transform=transform)

        train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True)
        val_loader = DataLoader(val_ds, batch_size=1000, shuffle=False)

        model = SimpleCNN().to(device)
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.SGD(model.parameters(), lr=args.learning_rate)

        for epoch in range(1, args.epochs + 1):
            train_loss, train_acc = train_one_epoch(model, device, train_loader, criterion, optimizer)
            val_loss, val_acc = validate(model, device, val_loader, criterion)

            # Log metrics (per epoch) for learning curves
            mlflow.log_metric("train_loss", train_loss, step=epoch)
            mlflow.log_metric("train_accuracy", train_acc, step=epoch)
            mlflow.log_metric("val_loss", val_loss, step=epoch)
            mlflow.log_metric("val_accuracy", val_acc, step=epoch)

            print(f"Epoch {epoch}/{args.epochs} - train_loss={train_loss:.4f} train_acc={train_acc:.4f} val_loss={val_loss:.4f} val_acc={val_acc:.4f}")

        # Save model using MLflow PyTorch flavor (artifacts + MLmodel metadata + env info)
        mlflow.pytorch.log_model(model, "model")
        # Optionally save the final state dict as an artifact
        os.makedirs("artifacts", exist_ok=True)
        torch.save(model.state_dict(), "artifacts/model_state.pth")
        mlflow.log_artifact("artifacts/model_state.pth")


if __name__ == "__main__":
    main()
