# MATLAB with Python Integration Project

This project demonstrates how to integrate MATLAB and Python, with a focus on calling Python from MATLAB. It is designed for educational purposes, especially for MATLAB users interested in leveraging Python libraries and code.

## Project Structure

- `matlab/` — MATLAB scripts demonstrating Python integration
- `python/` — Python scripts and modules for use with MATLAB

## Getting Started

### Prerequisites
- MATLAB R2014b or later (for Python integration)
- Python 3.x installed and accessible from MATLAB
- (Optional) An environment manager like Anaconda

### 1. Setting up Python for MATLAB

1. Ensure Python is installed and accessible from MATLAB:
   ```matlab
   pyenv('Version', 'C:/Path/To/python.exe')
   ```
2. Install required Python packages:
   ```powershell
   pip install -r python/requirements.txt
   ```

### 2. Running MATLAB Scripts that Use Python

- Open MATLAB and run scripts in the `matlab/` folder. These scripts demonstrate calling Python functions, using Python libraries, and exchanging data.

### 3. Calling MATLAB from Python (Bonus)

- See the `python/` folder for examples of calling MATLAB from Python using the MATLAB Engine API for Python.

## Example Topics
- Calling Python functions from MATLAB
- Using Python libraries (e.g., NumPy, matplotlib) in MATLAB
- Exchanging data between MATLAB and Python
- (Bonus) Calling MATLAB from Python

---

For more details, see the example scripts in each folder.
