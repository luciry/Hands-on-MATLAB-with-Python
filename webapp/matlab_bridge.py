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
    print("MATLAB Engine for Python not available. Falling back to Python implementations.")

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

# Global flag to track MATLAB engine status
_matlab_engine_tried = False

# Initialize MATLAB engine once at startup
def initialize_matlab_engine():
    """Initialize the MATLAB engine once when the module is loaded"""
    global _matlab_engine, _matlab_engine_tried
    
    if not MATLAB_AVAILABLE:
        return
    
    try:
        print("Initializing MATLAB engine...")
        _matlab_engine = matlab.engine.start_matlab()
        # Add path to MATLAB examples
        examples_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Examples')
        matlab_dir = os.path.join(examples_dir, 'matlab')
        if os.path.exists(matlab_dir):
            _matlab_engine.addpath(matlab_dir)
        else:
            print(f"Warning: MATLAB examples directory not found at {matlab_dir}")
        
        print("MATLAB Engine initialized successfully")
    except Exception as e:
        print(f"Error initializing MATLAB engine: {str(e)}")
        print("Falling back to Python implementations")
        _matlab_engine = None
    finally:
        _matlab_engine_tried = True

# Initialize MATLAB engine when module is loaded
initialize_matlab_engine()

def get_matlab_engine():
    """Get the MATLAB engine (already initialized)"""
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
                print(f"Calling MATLAB function: {function_name} with params: {params}")
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
                elif function_name == "symbolic_math":
                    # Extract parameters with proper defaults
                    expression = params.get('arg1', 'x^2')
                    operation = params.get('arg2', 'simplify')
                    plot_path = params.get('arg3', None)
                    print(f"Calling MATLAB symbolic_math: expression={expression}, operation={operation}")
                    
                    # Create a MATLAB struct for parameters - symbolic_math.m expects a single struct parameter
                    matlab_params = {}
                    matlab_params['expression'] = expression
                    matlab_params['operation'] = operation
                    if plot_path:
                        matlab_params['plot_path'] = plot_path
                    
                    # Convert Python dict to MATLAB struct
                    matlab_struct = eng.struct(matlab_params)
                    
                    # Call MATLAB function with the struct parameter
                    result = eng.symbolic_math(matlab_struct)
                    
                    # Debug direct result to see structure
                    print(f"Direct MATLAB result type: {type(result)}")
                    print(f"Result attributes: {[attr for attr in dir(result) if not attr.startswith('_')]}")
                    print(f"Raw animation result keys: {dict(result).keys() if isinstance(result, dict) else 'Not a dict'}")
                    
                    # Process animation result
                    if isinstance(result, dict):
                        # This is a Python fallback result or a dict from MATLAB
                        frames = result.get('frames', [])
                        # Prepare static animation directory
                        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'animation')
                        if os.path.exists(static_dir):
                            # Remove old frames
                            for f in os.listdir(static_dir):
                                if f.endswith('.png'):
                                    try:
                                        os.remove(os.path.join(static_dir, f))
                                    except Exception as e:
                                        print(f"Failed to remove old frame {f}: {e}")
                        else:
                            os.makedirs(static_dir, exist_ok=True)
                            
                        # Copy frames to static directory and build URLs
                        frames_data = []
                        for i, frame in enumerate(frames):
                            # If frame is a file path
                            if isinstance(frame, str) and (os.path.exists(frame) or frame.startswith('C:\\')):
                                try:
                                    # Define the destination path in static/animation
                                    dest_path = os.path.join(static_dir, f"frame_{i:03d}.png")
                                    print(f"[MATLAB] Copying frame from {frame} to {dest_path}")
                                    
                                    # Copy the frame
                                    import shutil
                                    shutil.copy2(frame, dest_path)
                                    
                                    # Add URL to frames_data
                                    frames_data.append(f"/static/animation/frame_{i:03d}.png")
                                except Exception as e:
                                    print(f"Error copying frame at {frame}: {e}")
                            else:
                                # Not a file path, just append it
                                frames_data.append(frame)
                        thumbnail = result.get('thumbnail')
                        # If thumbnail is a file path, encode it
                        if thumbnail and isinstance(thumbnail, str) and os.path.exists(thumbnail):
                            with open(thumbnail, 'rb') as f:
                                thumbnail = base64.b64encode(f.read()).decode('utf-8')
                        title = result.get('title', 'Animation')
                        description = result.get('description', '')
                        num_frames = result.get('num_frames', len(frames_data))
                        if frames_data:
                            print(f"Successfully processed {len(frames_data)} frames from dict result")
                            return {
                                'frames': frames_data,
                                'thumbnail': thumbnail,
                                'title': title,
                                'description': description,
                                'num_frames': num_frames
                            }
                    else:
                        # Try to process as MATLAB result (object)
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
                                # Prepare static animation directory
                                static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'animation')
                                if os.path.exists(static_dir):
                                    # Remove old frames
                                    for f in os.listdir(static_dir):
                                        if f.endswith('.png'):
                                            try:
                                                os.remove(os.path.join(static_dir, f))
                                            except Exception as e:
                                                print(f"Failed to remove old frame {f}: {e}")
                                else:
                                    os.makedirs(static_dir, exist_ok=True)
                                    
                                # Process each frame
                                for i, frame_path in enumerate(frame_paths):
                                    try:
                                        # Define the destination path in static/animation
                                        dest_path = os.path.join(static_dir, f"frame_{i:03d}.png")
                                        print(f"[MATLAB] Copying frame from {frame_path} to {dest_path}")
                                        
                                        # Copy the frame
                                        import shutil
                                        shutil.copy2(frame_path, dest_path)
                                        
                                        # Add URL to frames_data
                                        frames_data.append(f"/static/animation/frame_{i:03d}.png")
                                    except Exception as e:
                                        print(f"Error copying frame at {frame_path}: {e}")
                                # Get title and description
                                title = result.title if hasattr(result, 'title') else 'Animation'
                                description = result.description if hasattr(result, 'description') else ''
                                # Read thumbnail
                                thumbnail = None
                                if hasattr(result, 'thumbnail') and result.thumbnail and os.path.exists(result.thumbnail):
                                    with open(result.thumbnail, 'rb') as f:
                                        thumbnail = base64.b64encode(f.read()).decode('utf-8')
                                if frames_data:
                                    print(f"Successfully processed {len(frames_data)} frames from MATLAB result")
                                    print(f"[DEBUG] Final frame URLs from MATLAB: {frames_data}")
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

@matlab_function('symbolic_math')
def symbolic_math(expression='x^2', operation='simplify', plot_path=None):
    """Symbolic math operations with a Python fallback using SymPy"""
    try:
        import sympy as sp
        from sympy.parsing.sympy_parser import parse_expr
        import matplotlib.pyplot as plt
        import numpy as np
        import base64
        from io import BytesIO
        
        # Initialize result
        result = {
            'status': 'success',
            'result': '',
            'latex': '',
            'plot': None
        }
        
        # Parse the expression
        x = sp.Symbol('x')
        try:
            expr = parse_expr(expression)
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Error parsing expression: {str(e)}'
            }
        
        # Perform the operation
        if operation == 'simplify':
            res = sp.simplify(expr)
            result['result'] = str(res)
            result['latex'] = sp.latex(res)
        
        elif operation == 'differentiate':
            res = sp.diff(expr, x)
            result['result'] = str(res)
            result['latex'] = sp.latex(res)
        
        elif operation == 'integrate':
            res = sp.integrate(expr, x)
            result['result'] = str(res)
            result['latex'] = sp.latex(res)
        
        elif operation == 'solve':
            res = sp.solve(expr, x)
            result['result'] = str(res)
            result['latex'] = sp.latex(res)
        
        elif operation == 'plot':
            # Create plot using matplotlib
            plt.figure(figsize=(8, 6))
            
            # Convert sympy expression to numpy function
            f = sp.lambdify(x, expr, 'numpy')
            
            # Generate x values
            x_vals = np.linspace(-10, 10, 1000)
            
            # Calculate y values, handling potential errors
            try:
                y_vals = f(x_vals)
                plt.plot(x_vals, y_vals)
                plt.title(f'Plot of {expression}')
                plt.xlabel('x')
                plt.ylabel('y')
                plt.grid(True)
                
                # Save to buffer
                buffer = BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)
                
                # Convert to base64
                plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
                plt.close()
                
                result['result'] = f'Plot created for {expression}'
                result['latex'] = result['result']
                result['plot'] = plot_data
                
                # Save to file if path is provided
                if plot_path:
                    plt.savefig(plot_path)
            
            except Exception as e:
                return {
                    'status': 'error',
                    'message': f'Error plotting expression: {str(e)}'
                }
        
        else:
            return {
                'status': 'error',
                'message': f'Unknown operation: {operation}'
            }
        
        return result
    
    except ImportError as e:
        return {
            'status': 'error',
            'message': f'Python fallback failed: {str(e)}. SymPy package is required for symbolic math operations.'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Error in symbolic math operation: {str(e)}'
        }
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
    """Animation creation with support for multiple animation types"""
    # Create a temp directory for frames
    temp_dir = tempfile.mkdtemp(prefix="matlab_animation_")
    print(f"Using temp directory: {temp_dir}")
    
    try:
        # Validate animation type
        animation_type = str(animation_type).lower()
        valid_types = ['pendulum', 'wave', 'lissajous', 'spiral', 'orbit']

        # Prepare static animation directory
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'animation')
        if os.path.exists(static_dir):
            # Remove old frames
            for f in os.listdir(static_dir):
                if f.endswith('.png'):
                    try:
                        os.remove(os.path.join(static_dir, f))
                    except Exception as e:
                        print(f"Failed to remove old frame {f}: {e}")
        else:
            os.makedirs(static_dir, exist_ok=True)

        if animation_type not in valid_types:
            print(f"Warning: Unknown animation type '{animation_type}'. Falling back to pendulum.")
            animation_type = 'pendulum'
        
        print(f"Starting animation generation: {animation_type} with {num_frames} frames")
        frames = []
        
        for i in range(int(num_frames)):
            # Create frame path
            frame_path = os.path.join(temp_dir, f"frame_{i:03d}.png")
            # Destination path in static/animation
            dest_path = os.path.join(static_dir, f"frame_{i:03d}.png")
            print(f"[DEBUG] Frame {i}: src={frame_path}, dest={dest_path}")
            
            # Create frame based on animation type
            fig = plt.figure(figsize=(6, 6))
            
            if animation_type == 'pendulum':
                # Simple pendulum simulation
                angle = np.pi/4 * np.cos(i/num_frames * 2 * np.pi)
                x = np.sin(angle)
                y = -np.cos(angle)
                
                plt.plot([0, x], [0, y], 'k-', linewidth=2)
                plt.plot(x, y, 'ro', markersize=15)
                plt.xlim(-1.2, 1.2)
                plt.ylim(-1.2, 1.2)
                plt.title(f"Pendulum Simulation (t = {i/num_frames:.2f} s)")
                
            elif animation_type == 'wave':
                # Wave propagation
                x = np.linspace(0, 10, 1000)
                t = i / num_frames  # Time variable
                y = np.sin(x - 6*t) * np.exp(-0.1*x)
                
                plt.plot(x, y, 'b-', linewidth=2)
                plt.xlim(0, 10)
                plt.ylim(-1.2, 1.2)
                plt.title(f"Wave Propagation (t = {t:.2f} s)")
                
            elif animation_type == 'lissajous':
                # Lissajous curve
                t = np.linspace(0, 2*np.pi, 1000)
                a, b = 3, 4  # Frequency ratio
                delta = i/int(num_frames) * np.pi  # Phase difference varies with frame
                
                x = np.sin(a * t + delta)
                y = np.sin(b * t)
                
                plt.plot(x, y, 'g-', linewidth=2)
                plt.xlim(-1.2, 1.2)
                plt.ylim(-1.2, 1.2)
                plt.title(f"Lissajous Curve (Phase = {delta:.2f} rad)")
                
            elif animation_type == 'spiral':
                # Spiral formation
                t = np.linspace(0, 15, 1000)
                max_t = (i+1)/int(num_frames) * 15  # Grow the spiral with each frame
                t_visible = t[t <= max_t]
                
                r = 0.1 * t_visible
                x = r * np.cos(t_visible)
                y = r * np.sin(t_visible)
                
                plt.plot(x, y, 'm-', linewidth=2)
                plt.xlim(-1.2, 1.2)
                plt.ylim(-1.2, 1.2)
                plt.title(f"Spiral Formation (t = {max_t:.2f})")
            
            elif animation_type == 'orbit':
                # Planetary orbit simulation
                # Parameters
                a = 0.5  # Semi-major axis
                e = 0.5  # Eccentricity
                b = a * np.sqrt(1 - e**2)  # Semi-minor axis
                
                # Calculate position at this time step
                theta = 2 * np.pi * i / int(num_frames)
                r = a * (1 - e**2) / (1 + e * np.cos(theta))
                x = r * np.cos(theta)
                y = r * np.sin(theta)
                
                # Draw orbit path
                t = np.linspace(0, 2*np.pi, 100)
                orbit_x = a * np.cos(t)
                orbit_y = b * np.sin(t)
                plt.plot(orbit_x, orbit_y, 'b--', alpha=0.5)
                
                # Draw sun at focus
                plt.plot(0, 0, 'yo', markersize=15)  # Sun
                
                # Draw planet
                plt.plot(x, y, 'ro', markersize=10)  # Planet
                
                # Connect planet to sun with a line
                plt.plot([0, x], [0, y], 'k-', alpha=0.3)
                
                plt.xlim(-1.5, 1.5)
                plt.ylim(-1.5, 1.5)
                plt.title(f"Planetary Orbit (θ = {theta:.2f} rad)")
            
            # Common settings for all animation types
            plt.grid(True)
            plt.axis('equal')
            
            # Save frame
            plt.savefig(frame_path)
            plt.close(fig)
            # Copy frame to static/animation
            import shutil
            try:
                shutil.copy2(frame_path, dest_path)
                print(f"[DEBUG] Copied frame {i} to static/animation/")
            except Exception as copy_err:
                print(f"[ERROR] Failed to copy frame {i}: {copy_err}")
            # Append URL for frontend
            frames.append(f"/static/animation/frame_{i:03d}.png")
        print(f"[DEBUG] Final frame URLs: {frames}")

        # Create thumbnail
        print("Creating thumbnail...")
        fig = plt.figure(figsize=(6, 6))
        plt.text(0.5, 0.5, f"{animation_type.title()} Animation\n(Python Implementation)", 
                horizontalalignment='center', fontsize=16)
        plt.axis('off')
        thumbnail_path = os.path.join(temp_dir, "thumbnail.png")
        plt.savefig(thumbnail_path)
        plt.close(fig)
        
        with open(thumbnail_path, 'rb') as f:
            thumbnail = base64.b64encode(f.read()).decode('utf-8')
        
        # Prepare animation descriptions based on type
        descriptions = {
            'pendulum': 'Simple pendulum with length 1.0 m starting at angle 0.8 rad',
            'wave': 'Wave propagation with exponential damping',
            'lissajous': 'Lissajous curve with frequency ratio 3:4 and varying phase',
            'spiral': 'Spiral formation with linear growth rate',
            'orbit': 'Planetary orbit with eccentricity e=0.5'
        }
        
        print(f"Animation completed, generated {len(frames)} frames")
        
        return {
            'frames': frames,
            'thumbnail': thumbnail,
            'title': f'{animation_type.title()} Animation',
            'description': descriptions.get(animation_type, 'Animation created with Python'),
            'num_frames': len(frames),
            'source_code': None
        }
    
    except Exception as e:
        print(f"Error generating animation: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'status': 'error',
            'message': str(e)
        }
    finally:
        # Clean up temp directory
        print("Cleaning up temp directory...")
        import shutil
        shutil.rmtree(temp_dir, ignore_errors=True) 