"""
tqdm Module - Progress Bars for Loops

Introduction:
The 'tqdm' module provides fast and extensible progress bars for Python loops, useful for tracking the progress of long-running operations.

Installation:
To install tqdm, run:
    pip install tqdm

Basic Usage:
"""

from tqdm import tqdm
import time

# 1. Simple progress bar for a loop
for i in tqdm(range(100)):
    time.sleep(0.01)  # Simulating some task

"""
Advanced Usage:
"""

# 1. Progress bar for functions or list comprehension
data = [i for i in tqdm(range(1000), desc="Loading")]

# 2. Nested progress bars
for i in tqdm(range(10), desc="Outer Loop"):
    for j in tqdm(range(100), desc="Inner Loop", leave=False):
        time.sleep(0.01)

# 3. Progress bar inside a loop
pbar = tqdm(total=100)
for i in range(100):
    time.sleep(0.1)  # Simulating work
    pbar.update()  # Manually update the progress bar

pbar.close()  # Close the progress bar when done, not nescessary but good practice

"""
Real-World Example:
"""
# 1. Tracking file download progress
import requests

url = 'https://example.com/largefile.zip'
response = requests.get(url, stream=True)

total_size = int(response.headers.get('content-length', 0))
block_size = 1024

with open('largefile.zip', 'wb') as file, tqdm(total=total_size, unit='iB', unit_scale=True) as progress_bar:
    for data in response.iter_content(block_size):
        progress_bar.update(len(data))
        file.write(data)
