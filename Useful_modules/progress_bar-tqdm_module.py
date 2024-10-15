from tqdm import tqdm
import time

# Create a tqdm progress bar
print('Create a tqdm progress bar')
for i in tqdm(range(100)):
    time.sleep(0.1)  # Simulating work

# Using it inside a loop
pbar = tqdm(total=100)
print('Using it inside a loop')
for i in range(100):
    # Your code here
    time.sleep(0.1)  # Simulating work
    pbar.update()  # Manually update the progress bar

pbar.close()  # Close the progress bar when done, not nescessary but good practice

