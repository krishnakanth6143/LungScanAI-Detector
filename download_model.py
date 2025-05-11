"""
This script downloads the lung cancer model from a remote source.
Run this after cloning the repository to set up the model.
"""
import os
import requests
from tqdm import tqdm

def download_model(url, destination):
    """Download a file from a URL to a local destination with progress bar."""
    if os.path.exists(destination):
        print(f"Model file already exists at {destination}")
        return

    print(f"Downloading model from {url}...")
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 KB
    
    with open(destination, 'wb') as file, tqdm(
        desc=destination,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(block_size):
            size = file.write(data)
            bar.update(size)
            
    print(f"Model downloaded successfully to {destination}")

if __name__ == "__main__":
    # Replace this URL with the actual URL where you host your model file
    MODEL_URL = "YOUR_MODEL_HOST_URL/lung_cancer_model.h5"
    MODEL_PATH = "lung_cancer_model.h5"
    
    download_model(MODEL_URL, MODEL_PATH)
    print("\nTo use this model for the LungScanAI-Detector, simply run 'python app.py'")
