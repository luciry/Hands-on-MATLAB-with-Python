# MATLAB-Python Integration Web Demo

This web application demonstrates the integration between MATLAB and Python in an educational context. It provides a simple interface for students to see how MATLAB functions can be called from a Python web application.

## Features

- Simple Bootstrap-based user interface
- Python (Flask) backend
- Integration with MATLAB through the MATLAB Engine for Python
- Python fallbacks when MATLAB is not available
- Interactive visualizations with adjustable parameters

## Setup Instructions

### Prerequisites

1. Python 3.6+ installed
2. MATLAB R2014b or later installed (optional, but recommended)
3. MATLAB Engine for Python installed (optional, but recommended)

### Installation

1. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

2. (Optional) Install MATLAB Engine for Python:
   ```
   cd "C:\Program Files\MATLAB\R2022b\extern\engines\python"
   python setup.py install
   ```
   (Replace the path with your MATLAB installation path)

### Running the Application

1. From the webapp directory, run:
   ```
   python app.py
   ```

2. Open a web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

The application provides three example operations:

1. **Simple Plot**: Generate a basic sine wave plot
2. **Advanced Plot**: Create customizable waveform plots (sine, cosine, tangent, square)
3. **Matrix Operations**: Perform matrix operations (eigenvalues, SVD, visualization)

For each operation, you can choose to use either:
- The Python implementation (works without MATLAB)
- The MATLAB implementation (requires MATLAB Engine for Python)

## Educational Value

This demo showcases:
- How to integrate MATLAB and Python
- How to use MATLAB's visualization capabilities in a web application
- How to provide fallbacks when MATLAB is not available
- Simple web application development with Flask and Bootstrap

## Troubleshooting

If you encounter issues with the MATLAB Engine:
1. Ensure MATLAB is properly installed and licensed
2. Make sure the MATLAB Engine for Python is installed
3. Check that the Python and MATLAB versions are compatible

If MATLAB is not available, the application will automatically fall back to using Python implementations. 