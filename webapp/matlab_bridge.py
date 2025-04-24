import os
import sys
import base64
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
import tempfile
import glob
from PIL import Image

# Try to import MATLAB engine
try:
    import matlab.engine
    MATLAB_AVAILABLE = True
except ImportError:
    MATLAB_AVAILABLE = False
    print("MATLAB Engine for Python not available. Falling back to simulation mode.")

# Dictionary to store MATLAB functions with their Python fallback implementations
matlab_functions = {}

def matlab_function(func_name):
    """Decorator to register MATLAB functions with Python fallbacks"""
    def decorator(function):
        matlab_functions[func_name] = function
        return function
    return decorator

# Start MATLAB engine (if available)
_matlab_engine = None

def get_matlab_engine():
    """Get or start the MATLAB engine"""
    global _matlab_engine
    if MATLAB_AVAILABLE and _matlab_engine is None:
        try:
            _matlab_engine = matlab.engine.start_matlab()
            # Add path to MATLAB examples
            examples_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Examples')
            matlab_dir = os.path.join(examples_dir, 'matlab')
            _matlab_engine.addpath(matlab_dir)
            print("MATLAB Engine started successfully")
        except Exception as e:
            print(f"Error starting MATLAB engine: {e}")
            _matlab_engine = None
    return _matlab_engine

def get_matlab_source(function_name):
    """Get the source code of a MATLAB function"""
    examples_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Examples')
    matlab_dir = os.path.join(examples_dir, 'matlab')
    file_path = os.path.join(matlab_dir, f"{function_name}.m")
    
    if os.path.exists(file_path):
        try:
            # Try with utf-8 encoding first
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except UnicodeDecodeError:
            try:
                # Fall back to latin-1 which can read any byte
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.read()
            except Exception as e:
                print(f"Error reading source file: {e}")
                return f"% Could not read source code due to encoding error: {e}"
    return None

def call_matlab_function(function_name, params=None):
    """Call a MATLAB function or its Python fallback"""
    if params is None:
        params = {}
    
    # Try to use MATLAB if available
    eng = get_matlab_engine()
    if eng is not None:
        try:
            # Check if the function exists in MATLAB
            if eng.exist(function_name, nargout=1) >= 2:  # 2 means it's a file
                # Convert the params to MATLAB format and call the function
                if function_name == "simple_plot":
                    x_min = params.get('x_min', -10)
                    x_max = params.get('x_max', 10)
                    num_points = params.get('num_points', 100)
                    result = eng.simple_plot(float(x_min), float(x_max), float(num_points))
                elif function_name == "advanced_plot":
                    function_type = params.get('function_type', 'sin')
                    amplitude = params.get('amplitude', 1)
                    frequency = params.get('frequency', 1)
                    phase = params.get('phase', 0)
                    x_min = params.get('x_min', -10)
                    x_max = params.get('x_max', 10)
                    num_points = params.get('num_points', 100)
                    result = eng.advanced_plot(function_type, float(amplitude), float(frequency), 
                                              float(phase), float(x_min), float(x_max), float(num_points))
                elif function_name == "differential_equation":
                    eq_type = params.get('eq_type', 'spring')
                    t_max = params.get('t_max', 10)
                    num_points = params.get('num_points', 100)
                    result = eng.differential_equation(eq_type, float(t_max), float(num_points))
                elif function_name == "image_processing":
                    operation = params.get('operation', 'edge')
                    noise_level = params.get('noise_level', 0.2)
                    result = eng.image_processing(operation, float(noise_level))
                elif function_name == "animation":
                    animation_type = params.get('animation_type', 'pendulum')
                    num_frames = params.get('num_frames', 20)
                    print(f"Calling MATLAB animation: type={animation_type}, frames={num_frames}")
                    result = eng.animation(animation_type, float(num_frames))
                    
                    # Debug direct result to see structure
                    print(f"Direct MATLAB result type: {type(result)}")
                    print(f"Result attributes: {[attr for attr in dir(result) if not attr.startswith('_')]}")
                    
                    # Process animation result
                    frames_data = []
                    
                    try:
                        # Try to access frames from result
                        if hasattr(result, 'frames'):
                            frames_attr = result.frames
                            if isinstance(frames_attr, list):
                                frame_paths = frames_attr
                            else:
                                # Handle MATLAB cell array
                                frame_paths = [frames_attr[i] for i in range(len(frames_attr))]
                            
                            print(f"Processing {len(frame_paths)} frame paths")
                            
                            # Process each frame
                            for frame_path in frame_paths:
                                try:
                                    print(f"Reading frame: {frame_path}")
                                    with open(frame_path, 'rb') as f:
                                        frame_data = base64.b64encode(f.read()).decode('utf-8')
                                        frames_data.append(frame_data)
                                except Exception as e:
                                    print(f"Error reading frame at {frame_path}: {e}")
                            
                            # Get title and description
                            title = result.title if hasattr(result, 'title') else 'Animation'
                            description = result.description if hasattr(result, 'description') else ''
                            
                            # Read thumbnail
                            thumbnail = None
                            if hasattr(result, 'thumbnail') and result.thumbnail and os.path.exists(result.thumbnail):
                                with open(result.thumbnail, 'rb') as f:
                                    thumbnail = base64.b64encode(f.read()).decode('utf-8')
                            
                            if frames_data:
                                print(f"Successfully processed {len(frames_data)} frames")
                                return {
                                    'frames': frames_data,
                                    'thumbnail': thumbnail,
                                    'title': title,
                                    'description': description,
                                    'num_frames': len(frames_data)
                                }
                    except Exception as e:
                        print(f"Error in animation processing: {e}")
                        import traceback
                        traceback.print_exc()
                    
                    # If we didn't return frames data, continue with regular return
                    print("No frames found, returning standard result")
                else:
                    # For other functions, try keyword args as fallback
                    result = getattr(eng, function_name)(**params)
                
                # Handle capturing figures from MATLAB
                if function_name.endswith('_plot') or function_name in ["differential_equation", "image_processing"]:
                    # Get the current figure from MATLAB and save it
                    eng.eval("saveas(gcf, 'temp_plot.png')", nargout=0)
                    with open('temp_plot.png', 'rb') as f:
                        plot_data = base64.b64encode(f.read()).decode('utf-8')
                    os.remove('temp_plot.png')
                    
                    # Add source code if available
                    source_code = get_matlab_source(function_name)
                    
                    return {
                        'plot': plot_data,
                        'source_code': source_code,
                        'equation': result.equation if hasattr(result, 'equation') else None,
                        'equations': result.equations if hasattr(result, 'equations') else None,
                        'parameters': result.parameters if hasattr(result, 'parameters') else None,
                        'operation': result.operation if hasattr(result, 'operation') else None,
                        'methods': result.methods if hasattr(result, 'methods') else None
                    }
                
                return {'data': result}
        except Exception as e:
            print(f"Error calling MATLAB function: {e}")
            import traceback
            traceback.print_exc()
    
    # Fall back to Python implementation
    if function_name in matlab_functions:
        return matlab_functions[function_name](**params)
    
    raise ValueError(f"Function {function_name} not available in MATLAB or as a fallback")

# Define fallback functions for our standard examples
@matlab_function("simple_plot")
def simple_plot(x_min=-10, x_max=10, num_points=100):
    """Simple sine wave plot (Python fallback for MATLAB function)"""
    x = np.linspace(x_min, x_max, num_points)
    y = np.sin(x)
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y)
    plt.title('Simple Sine Wave (Python Implementation)')
    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    plt.grid(True)
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    # Get the source code (Python version since MATLAB is unavailable)
    source_code = """function result = simple_plot(x_min, x_max, num_points)
    % This is a Python fallback implementation
    % The original MATLAB code is not available
    
    % In Python:
    % x = np.linspace(x_min, x_max, num_points)
    % y = np.sin(x)
    % plt.plot(x, y)
end"""
    
    return {
        'plot': plot_data,
        'source_code': source_code
    }

@matlab_function("advanced_plot")
def advanced_plot(function_type="sin", amplitude=1, frequency=1, phase=0, x_min=-10, x_max=10, num_points=100):
    """Plot of various waveforms with adjustable parameters (Python fallback)"""
    x = np.linspace(x_min, x_max, num_points)
    
    if function_type == "sin":
        y = amplitude * np.sin(frequency * x + phase)
        title = f"Sine Wave: {amplitude}·sin({frequency}x + {phase})"
    elif function_type == "cos":
        y = amplitude * np.cos(frequency * x + phase)
        title = f"Cosine Wave: {amplitude}·cos({frequency}x + {phase})"
    elif function_type == "tan":
        y = amplitude * np.tan(frequency * x + phase)
        y = np.clip(y, -10, 10)  # Clip to prevent excessive values
        title = f"Tangent Wave: {amplitude}·tan({frequency}x + {phase})"
    elif function_type == "square":
        y = amplitude * np.sign(np.sin(frequency * x + phase))
        title = f"Square Wave: amplitude={amplitude}, freq={frequency}, phase={phase}"
    else:
        y = np.zeros_like(x)
        title = "Unknown function type"
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y)
    plt.title(title)
    plt.xlabel('X axis')
    plt.ylabel('Y axis')
    plt.grid(True)
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    # Get the source code (Python version since MATLAB is unavailable)
    source_code = """function result = advanced_plot(function_type, amplitude, frequency, phase, x_min, x_max, num_points)
    % This is a Python fallback implementation
    % The original MATLAB code is not available
    
    % In Python:
    % x = np.linspace(x_min, x_max, num_points)
    % if function_type == "sin":
    %     y = amplitude * np.sin(frequency * x + phase)
    % elif function_type == "cos":
    %     y = amplitude * np.cos(frequency * x + phase)
    % ...
end"""
    
    return {
        'plot': plot_data,
        'source_code': source_code
    }

# Define fallbacks for our new functions
@matlab_function("differential_equation")
def differential_equation(eq_type="spring", t_max=10, num_points=100):
    """Differential equation solver (Python fallback)"""
    # This is a simplified version that doesn't solve real DEs
    # Just show a placeholder image
    
    plt.figure(figsize=(10, 6))
    plt.text(0.5, 0.5, f"Differential Equation ({eq_type})\nThis requires MATLAB", 
             horizontalalignment='center', fontsize=16)
    plt.axis('off')
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    # Get the source code (Python version since MATLAB is unavailable)
    source_code = """function result = differential_equation(eq_type, t_max, num_points)
    % This requires MATLAB's differential equation solvers
    % Please install MATLAB to see the actual implementation
end"""
    
    return {
        'plot': plot_data,
        'source_code': source_code,
        'equation': "Requires MATLAB",
        'parameters': "Requires MATLAB"
    }

@matlab_function("image_processing")
def image_processing(operation="edge", noise_level=0.2):
    """Image processing (Python fallback)"""
    # This is a simplified version that doesn't do real image processing
    
    plt.figure(figsize=(10, 6))
    plt.text(0.5, 0.5, f"Image Processing ({operation})\nThis requires MATLAB", 
             horizontalalignment='center', fontsize=16)
    plt.axis('off')
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    # Get the source code (Python version since MATLAB is unavailable)
    source_code = """function result = image_processing(operation, noise_level)
    % This requires MATLAB's Image Processing Toolbox
    % Please install MATLAB to see the actual implementation
end"""
    
    return {
        'plot': plot_data,
        'source_code': source_code,
        'operation': "Requires MATLAB",
        'methods': "Requires MATLAB"
    }

@matlab_function("animation")
def animation(animation_type="pendulum", num_frames=20):
    """Animation creation (Python fallback)"""
    # Create a very simple animation with matplotlib
    
    frames = []
    
    # Create a temp directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Generate a simple pendulum animation (very simplified)
        for i in range(num_frames):
            fig = plt.figure(figsize=(6, 6))
            angle = np.pi/4 * np.cos(i/num_frames * 2 * np.pi)
            x = np.sin(angle)
            y = -np.cos(angle)
            
            plt.plot([0, x], [0, y], 'k-', linewidth=2)
            plt.plot(x, y, 'ro', markersize=15)
            plt.xlim(-1.2, 1.2)
            plt.ylim(-1.2, 1.2)
            plt.axis('equal')
            plt.title(f"Simple Pendulum Animation (Python)\nFrame {i+1}/{num_frames}")
            plt.grid(True)
            
            # Save the frame
            frame_path = os.path.join(temp_dir, f"frame_{i:03d}.png")
            plt.savefig(frame_path)
            plt.close(fig)
            
            # Read and encode the frame
            with open(frame_path, 'rb') as f:
                frame_data = base64.b64encode(f.read()).decode('utf-8')
                frames.append(frame_data)
        
        # Create a thumbnail
        fig = plt.figure(figsize=(6, 6))
        plt.text(0.5, 0.5, "Pendulum Animation\n(Python Implementation)", 
                horizontalalignment='center', fontsize=16)
        plt.axis('off')
        thumbnail_path = os.path.join(temp_dir, "thumbnail.png")
        plt.savefig(thumbnail_path)
        plt.close(fig)
        
        with open(thumbnail_path, 'rb') as f:
            thumbnail = base64.b64encode(f.read()).decode('utf-8')
    
    # Get the source code (Python version since MATLAB is unavailable)
    source_code = """function result = animation(animation_type, num_frames)
    % This requires MATLAB's animation capabilities
    % Please install MATLAB to see the actual implementation
end"""
    
    return {
        'frames': frames,
        'thumbnail': thumbnail,
        'title': 'Simple Pendulum (Python Fallback)',
        'description': 'Python implementation of a simple pendulum animation. Install MATLAB for the full version.',
        'num_frames': len(frames),
        'source_code': source_code
    } 