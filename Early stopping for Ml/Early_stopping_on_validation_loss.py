import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
from sklearn.model_selection import train_test_split

class EarlyStoppingController:
    def __init__(
        self,
        patience=100,
        stagnation_fraction=0.1,
        max_iterations=1000,
        min_delta=1e-4,
        rolling_window=20,
        warmup=0,
        use_ema=True,
        ema_beta=0.9,
        verbose=False
    ):
        self.patience = patience
        self.stagnation_threshold = int(stagnation_fraction * max_iterations)
        self.max_iterations = max_iterations
        self.min_delta = min_delta
        self.rolling_window = rolling_window
        self.warmup = warmup
        self.use_ema = use_ema
        self.ema_beta = ema_beta
        self.verbose = verbose

        self.iteration = 0
        self.best_loss = float('inf')
        self.best_state = None
        self.last_improvement_iter = 0
        self.loss_history = deque(maxlen=rolling_window)
        self.ema_loss = None
        self.same_loss_counter = 0
        self.last_loss = None

    def update(self, loss, model_state=None):
        self.iteration += 1

        # Smooth loss with EMA if enabled
        if self.use_ema:
            self.ema_loss = loss if self.ema_loss is None else self.ema_beta * self.ema_loss + (1 - self.ema_beta) * loss
            smoothed_loss = self.ema_loss
        else:
            smoothed_loss = loss

        self.loss_history.append(smoothed_loss)

        # Update best loss and save state
        if smoothed_loss + self.min_delta < self.best_loss:
            self.best_loss = smoothed_loss
            self.best_state = model_state
            self.last_improvement_iter = self.iteration
            self.same_loss_counter = 0
            if self.verbose:
                print(f"[Iteration {self.iteration}] New best loss: {smoothed_loss:.6f}")
        else:
            # No improvement
            if self.last_loss is not None and abs(smoothed_loss - self.last_loss) < self.min_delta:
                self.same_loss_counter += 1
            else:
                self.same_loss_counter = 0

        self.last_loss = smoothed_loss

    def should_stop(self):
        if self.iteration < self.warmup:
            return False

        # Check convergence over recent history
        if len(self.loss_history) == self.rolling_window:
            variation = np.std(self.loss_history)
            if variation < self.min_delta:
                if self.verbose:
                    print(f"[Stop] Loss plateaued. Std dev: {variation:.6f}")
                return True

        # Check stagnation
        if (self.iteration - self.last_improvement_iter) > self.stagnation_threshold:
            if self.verbose:
                print(f"[Stop] No improvement for {self.stagnation_threshold} iterations.")
            return True

        # Check redundant flat values
        if self.same_loss_counter >= self.patience:
            if self.verbose:
                print(f"[Stop] Same loss for {self.patience} steps.")
            return True

        # Max iterations
        if self.iteration >= self.max_iterations:
            if self.verbose:
                print(f"[Stop] Max iterations reached: {self.max_iterations}")
            return True

        return False

    def get_best_state(self):
        return self.best_state

# --- Create synthetic dataset ---
torch.manual_seed(0)
x_all = torch.unsqueeze(torch.linspace(-1, 1, 100), dim=1)
y_all = 3 * x_all + 1 + 0.2 * torch.randn(x_all.size())

# Split into training and validation sets
x_train, x_val, y_train, y_val = train_test_split(x_all.numpy(), y_all.numpy(), test_size=0.2, random_state=42)
x_train = torch.tensor(x_train, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.float32)
x_val = torch.tensor(x_val, dtype=torch.float32)
y_val = torch.tensor(y_val, dtype=torch.float32)

# Model, loss, optimizer
model = nn.Linear(1, 1)
criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.1)

# Early stopping controller (using validation loss)
early_stopper = EarlyStoppingController(
    patience=25,
    stagnation_fraction=0.2,
    max_iterations=500,
    min_delta=1e-5,
    rolling_window=10,
    warmup=10,
    verbose=True
)

train_losses = []
val_losses = []

for epoch in range(1000):
    model.train()
    optimizer.zero_grad()
    pred_train = model(x_train)
    train_loss = criterion(pred_train, y_train)
    train_loss.backward()
    optimizer.step()

    model.eval()
    with torch.no_grad():
        pred_val = model(x_val)
        val_loss = criterion(pred_val, y_val)

    train_losses.append(train_loss.item())
    val_losses.append(val_loss.item())

    # Update early stopper using validation loss
    early_stopper.update(val_loss.item(), model.state_dict())

    if early_stopper.should_stop():
        print(f"Early stopping at epoch {epoch}")
        break

# Restore best model
model.load_state_dict(early_stopper.get_best_state())

# --- Plotting ---
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.plot(train_losses, label='Train Loss')
plt.plot(val_losses, label='Val Loss')
plt.axvline(x=early_stopper.iteration, color='red', linestyle='--', label='Stopped Here')
plt.title('Loss Curves')
plt.xlabel('Epoch')
plt.ylabel('MSE Loss')
plt.legend()

plt.subplot(1, 2, 2)
plt.scatter(x_all.numpy(), y_all.numpy(), label='All Data')
plt.plot(x_all.numpy(), model(x_all).detach().numpy(), color='red', label='Model Fit')
plt.title('Model Prediction vs Data')
plt.legend()

plt.tight_layout()
plt.show()
