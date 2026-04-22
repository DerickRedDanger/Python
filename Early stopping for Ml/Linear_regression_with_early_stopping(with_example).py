import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt
import numpy as np
from collections import deque

import numpy as np
from collections import deque

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

# Create a synthetic dataset: y = 3x + 1 + noise
torch.manual_seed(0)
x = torch.unsqueeze(torch.linspace(-1, 1, 100), dim=1)
y = 3 * x + 1 + 0.2 * torch.randn(x.size())

# Define a simple linear regression model
model = nn.Linear(1, 1)
criterion = nn.MSELoss()
optimizer = optim.SGD(model.parameters(), lr=0.1)

# Initialize the early stopping controller
early_stopper = EarlyStoppingController(
    patience=30,
    stagnation_fraction=0.2,
    max_iterations=500,
    min_delta=1e-5,
    rolling_window=15,
    warmup=10,
    verbose=True
)

# Training loop
losses = []
for epoch in range(1000):
    model.train()
    optimizer.zero_grad()
    output = model(x)
    loss = criterion(output, y)
    loss.backward()
    optimizer.step()

    losses.append(loss.item())

    # Update early stopping with current loss and model state
    early_stopper.update(loss.item(), model.state_dict())

    if early_stopper.should_stop():
        print(f"Early stopping at epoch {epoch}")
        break

# Restore best model
model.load_state_dict(early_stopper.get_best_state())

# Plot results
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.plot(losses, label='Training Loss')
plt.axvline(x=early_stopper.iteration, color='red', linestyle='--', label='Stopped Here')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Loss Curve')
plt.legend()

plt.subplot(1, 2, 2)
plt.scatter(x.numpy(), y.numpy(), label='Data')
plt.plot(x.numpy(), model(x).detach().numpy(), color='red', label='Fitted Line')
plt.title('Model Fit')
plt.legend()

plt.tight_layout()
plt.show()
