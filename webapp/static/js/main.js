document.addEventListener('DOMContentLoaded', function() {
    // Initialize syntax highlighting
    hljs.highlightAll();
    
    // Check if we're on the symbolic page or main page
    const isSymbolicPage = window.location.pathname.includes('/symbolic');
    
    if (!isSymbolicPage) {
        // Main page initialization
        setupSimplePlot();
        setupAdvancedPlot();
        setupDifferentialEquations();
        setupImageProcessing();
        setupResultCodeToggles();
    } else {
        // Symbolic page initialization
        setupSymbolicMath();
    }
});

// Function to handle API errors
function handleApiError(error) {
    console.error('API Error:', error);
    alert('Error: ' + error.message || 'Unknown error occurred');
}

// Function to escape HTML content
function escapeHtml(unsafe) {
    if (!unsafe) return '';
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Function to toggle between result and code views
function setupResultCodeToggles() {
    // Simple Plot
    document.getElementById('simpleResultBtn').addEventListener('click', function() {
        document.getElementById('simplePlotContainer').style.display = 'flex';
        document.getElementById('simpleCodeContainer').style.display = 'none';
        document.getElementById('simpleResultBtn').classList.add('active');
        document.getElementById('simpleCodeBtn').classList.remove('active');
    });
    
    document.getElementById('simpleCodeBtn').addEventListener('click', function() {
        document.getElementById('simplePlotContainer').style.display = 'none';
        document.getElementById('simpleCodeContainer').style.display = 'block';
        document.getElementById('simpleResultBtn').classList.remove('active');
        document.getElementById('simpleCodeBtn').classList.add('active');
        
        // Load MATLAB source code if not already loaded
        if (!document.getElementById('simpleCode').textContent.trim()) {
            loadMatlabSourceCode('simple_plot', 'simpleCode');
        }
    });
    
    // Advanced Plot
    document.getElementById('advancedResultBtn').addEventListener('click', function() {
        document.getElementById('advancedPlotContainer').style.display = 'flex';
        document.getElementById('advancedCodeContainer').style.display = 'none';
        document.getElementById('advancedResultBtn').classList.add('active');
        document.getElementById('advancedCodeBtn').classList.remove('active');
    });
    
    document.getElementById('advancedCodeBtn').addEventListener('click', function() {
        document.getElementById('advancedPlotContainer').style.display = 'none';
        document.getElementById('advancedCodeContainer').style.display = 'block';
        document.getElementById('advancedResultBtn').classList.remove('active');
        document.getElementById('advancedCodeBtn').classList.add('active');
        
        // Load MATLAB source code if not already loaded
        if (!document.getElementById('advancedCode').textContent.trim()) {
            loadMatlabSourceCode('advanced_plot', 'advancedCode');
        }
    });
    
    // Differential Equations
    document.getElementById('differentialResultBtn').addEventListener('click', function() {
        document.getElementById('differentialPlotContainer').style.display = 'flex';
        document.getElementById('differentialCodeContainer').style.display = 'none';
        document.getElementById('equationDisplay').style.display = 'block';
        document.getElementById('differentialResultBtn').classList.add('active');
        document.getElementById('differentialCodeBtn').classList.remove('active');
    });
    
    document.getElementById('differentialCodeBtn').addEventListener('click', function() {
        document.getElementById('differentialPlotContainer').style.display = 'none';
        document.getElementById('differentialCodeContainer').style.display = 'block';
        document.getElementById('equationDisplay').style.display = 'none';
        document.getElementById('differentialResultBtn').classList.remove('active');
        document.getElementById('differentialCodeBtn').classList.add('active');
        
        // Load MATLAB source code if not already loaded
        if (!document.getElementById('differentialCode').textContent.trim()) {
            loadMatlabSourceCode('differential_equation', 'differentialCode');
        }
    });
    
    // Image Processing
    document.getElementById('imageResultBtn').addEventListener('click', function() {
        document.getElementById('imagePlotContainer').style.display = 'flex';
        document.getElementById('imageCodeContainer').style.display = 'none';
        document.getElementById('imageInfo').style.display = 'block';
        document.getElementById('imageResultBtn').classList.add('active');
        document.getElementById('imageCodeBtn').classList.remove('active');
    });
    
    document.getElementById('imageCodeBtn').addEventListener('click', function() {
        document.getElementById('imagePlotContainer').style.display = 'none';
        document.getElementById('imageCodeContainer').style.display = 'block';
        document.getElementById('imageInfo').style.display = 'none';
        document.getElementById('imageResultBtn').classList.remove('active');
        document.getElementById('imageCodeBtn').classList.add('active');
        
        // Load MATLAB source code if not already loaded
        if (!document.getElementById('imageCode').textContent.trim()) {
            loadMatlabSourceCode('image_processing', 'imageCode');
        }
    });
    
    // Animation
    document.getElementById('animationResultBtn').addEventListener('click', function() {
        document.getElementById('animationContainer').style.display = 'block';
        document.getElementById('animationCodeContainer').style.display = 'none';
        document.getElementById('animationResultBtn').classList.add('active');
        document.getElementById('animationCodeBtn').classList.remove('active');
    });
    
    document.getElementById('animationCodeBtn').addEventListener('click', function() {
        document.getElementById('animationContainer').style.display = 'none';
        document.getElementById('animationCodeContainer').style.display = 'block';
        document.getElementById('animationResultBtn').classList.remove('active');
        document.getElementById('animationCodeBtn').classList.add('active');
        
        // Load MATLAB source code based on selected animation type
        const animationType = document.getElementById('animationType').value || 'pendulum';
        if (!document.getElementById('animationCode').textContent.trim()) {
            loadMatlabSourceCode('animation', 'animationCode');
        }
    });
    
    // Animation
    document.getElementById('animationResultBtn').addEventListener('click', function() {
        document.getElementById('animationContainer').style.display = 'flex';
        document.getElementById('animationCodeContainer').style.display = 'none';
        document.getElementById('animationInfo').style.display = 'block';
        document.getElementById('animationResultBtn').classList.add('active');
        document.getElementById('animationCodeBtn').classList.remove('active');
    });
    
    document.getElementById('animationCodeBtn').addEventListener('click', function() {
        document.getElementById('animationContainer').style.display = 'none';
        document.getElementById('animationCodeContainer').style.display = 'block';
        document.getElementById('animationInfo').style.display = 'none';
        document.getElementById('animationResultBtn').classList.remove('active');
        document.getElementById('animationCodeBtn').classList.add('active');
    });
}

// Setup Simple Plot
function setupSimplePlot() {
    document.getElementById('simplePlotBtn').addEventListener('click', function() {
        generateSimplePlot(false);
    });
    
    document.getElementById('matlabSimplePlotBtn').addEventListener('click', function() {
        generateSimplePlot(true);
    });
}

function generateSimplePlot(useMatlab) {
    // Show loading spinner
    document.getElementById('simplePlotLoading').style.display = 'block';
    document.getElementById('simplePlotImage').style.display = 'none';
    
    // Get parameters
    const params = {
        x_min: parseFloat(document.getElementById('xMinSimple').value),
        x_max: parseFloat(document.getElementById('xMaxSimple').value),
        num_points: parseInt(document.getElementById('numPointsSimple').value)
    };
    
    // Determine endpoint and request data
    let endpoint = useMatlab ? '/matlab_plot' : '/simple_plot';
    let requestData = useMatlab ? 
        { function: 'simple_plot', params: params } : 
        params;
    
    // Send request
    fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Hide loading indicator
            document.getElementById('simplePlotLoading').style.display = 'none';
            
            // Display plot
            if (data.plot) {
                const plotImage = document.getElementById('simplePlotImage');
                plotImage.src = 'data:image/png;base64,' + data.plot;
                plotImage.style.display = 'block';
            }
            
            // Update code if available
            if (data.source_code) {
                const codeElement = document.getElementById('simpleCode');
                codeElement.textContent = escapeHtml(data.source_code);
                hljs.highlightElement(codeElement);
            }
        } else {
            throw new Error(data.message || 'Unknown error');
        }
    })
    .catch(handleApiError);
}

// Setup Advanced Plot
function setupAdvancedPlot() {
    document.getElementById('advancedPlotBtn').addEventListener('click', function() {
        generateAdvancedPlot(false);
    });
    
    document.getElementById('matlabAdvancedPlotBtn').addEventListener('click', function() {
        generateAdvancedPlot(true);
    });
}

function generateAdvancedPlot(useMatlab) {
    // Show loading spinner
    document.getElementById('advancedPlotLoading').style.display = 'block';
    document.getElementById('advancedPlotImage').style.display = 'none';
    
    // Get parameters
    const params = {
        function_type: document.getElementById('functionType').value,
        amplitude: parseFloat(document.getElementById('amplitude').value),
        frequency: parseFloat(document.getElementById('frequency').value),
        phase: parseFloat(document.getElementById('phase').value)
    };
    
    // Determine endpoint and request data
    let endpoint = useMatlab ? '/matlab_plot' : '/advanced_plot';
    let requestData = useMatlab ? 
        { function: 'advanced_plot', params: params } : 
        params;
    
    // Send request
    fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Hide loading indicator
            document.getElementById('advancedPlotLoading').style.display = 'none';
            
            // Display plot
            if (data.plot) {
                const plotImage = document.getElementById('advancedPlotImage');
                plotImage.src = 'data:image/png;base64,' + data.plot;
                plotImage.style.display = 'block';
            }
            
            // Update code if available
            if (data.source_code) {
                const codeElement = document.getElementById('advancedCode');
                codeElement.textContent = escapeHtml(data.source_code);
                hljs.highlightElement(codeElement);
            }
        } else {
            throw new Error(data.message || 'Unknown error');
        }
    })
    .catch(handleApiError);
}

// Setup Differential Equations
function setupDifferentialEquations() {
    document.getElementById('differentialBtn').addEventListener('click', function() {
        generateDifferentialEquation();
    });
}

function generateDifferentialEquation() {
    // Show loading spinner
    document.getElementById('differentialLoading').style.display = 'block';
    document.getElementById('differentialImage').style.display = 'none';
    document.getElementById('equationDisplay').style.display = 'none';
    
    // Get parameters
    const params = {
        eq_type: document.getElementById('eqType').value,
        t_max: parseFloat(document.getElementById('tMax').value),
        num_points: parseInt(document.getElementById('numPointsDE').value)
    };
    
    // Make request
    fetch('/differential_equation', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(params)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Hide loading indicator
            document.getElementById('differentialLoading').style.display = 'none';
            
            // Display plot
            if (data.plot) {
                const plotImage = document.getElementById('differentialImage');
                plotImage.src = 'data:image/png;base64,' + data.plot;
                plotImage.style.display = 'block';
            }
            
            // Display equation information
            if (data.equation || data.equations) {
                document.getElementById('equationText').textContent = data.equation || data.equations || '';
                document.getElementById('parametersText').textContent = data.parameters || '';
                document.getElementById('equationDisplay').style.display = 'block';
            }
            
            // Update code if available
            if (data.source_code) {
                const codeElement = document.getElementById('differentialCode');
                codeElement.textContent = escapeHtml(data.source_code);
                hljs.highlightElement(codeElement);
            }
        } else {
            throw new Error(data.message || 'Unknown error');
        }
    })
    .catch(handleApiError);
}

// Setup Image Processing
function setupImageProcessing() {
    document.getElementById('imageProcessingBtn').addEventListener('click', function() {
        generateImageProcessing();
    });
}

function generateImageProcessing() {
    // Show loading spinner
    document.getElementById('imageLoading').style.display = 'block';
    document.getElementById('imageResult').style.display = 'none';
    document.getElementById('imageInfo').style.display = 'none';
    
    // Get parameters
    const params = {
        operation: document.getElementById('imageOperation').value,
        noise_level: parseFloat(document.getElementById('noiseLevel').value)
    };
    
    // Make request
    fetch('/image_processing', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(params)
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Hide loading indicator
            document.getElementById('imageLoading').style.display = 'none';
            
            // Display result
            if (data.plot) {
                const resultImage = document.getElementById('imageResult');
                resultImage.src = 'data:image/png;base64,' + data.plot;
                resultImage.style.display = 'block';
            }
            
            // Display image information
            if (data.operation) {
                document.getElementById('imageOperationTitle').textContent = data.operation;
                document.getElementById('imageMethodsText').textContent = data.methods || '';
                document.getElementById('imageInfo').style.display = 'block';
            }
            
            // Update code if available
            if (data.source_code) {
                const codeElement = document.getElementById('imageCode');
                codeElement.textContent = escapeHtml(data.source_code);
                hljs.highlightElement(codeElement);
            }
        } else {
            throw new Error(data.message || 'Unknown error');
        }
    })
    .catch(handleApiError);
}

// Setup Animation
function setupAnimation() {
    const animationBtn = document.getElementById('animationBtn');
    if (!animationBtn) return;
    
    animationBtn.addEventListener('click', function() {
        const animType = document.getElementById('animationType').value;
        const numFrames = document.getElementById('numFrames').value;
        const speed = document.getElementById('animationSpeed').value;
        
        // Show loading indicator
        const wrapper = document.getElementById('animationWrapper');
        const loadingEl = document.getElementById('animationLoading');
        const framesContainer = document.getElementById('animationFrames');
        
        if (wrapper) wrapper.style.display = 'none';
        if (loadingEl) loadingEl.style.display = 'block';
        if (framesContainer) framesContainer.innerHTML = '';
        
        // Make the API request
        fetch(`/api/animation?animation_type=${animType}&num_frames=${numFrames}&speed=${speed}`)
            .then(response => response.json())
            .then(data => {
                console.log("Animation data received:", data);
                
                if (loadingEl) loadingEl.style.display = 'none';
                
                if (data.frames && data.frames.length > 0) {
                    // We have frames, let's display them
                    const frames = data.frames;
                    console.log(`Received ${frames.length} frames`);
                    
                    // Create frame elements
                    frames.forEach((frameData, index) => {
                        const frameEl = document.createElement('img');
                        frameEl.className = 'animation-frame';
                        frameEl.src = `data:image/png;base64,${frameData}`;
                        frameEl.style.display = index === 0 ? 'block' : 'none';
                        frameEl.dataset.frameIndex = index;
                        framesContainer.appendChild(frameEl);
                    });
                    
                    // Show animation container
                    if (wrapper) wrapper.style.display = 'block';
                    
                    // Add animation info
                    const infoEl = document.getElementById('animationInfo');
                    if (infoEl) {
                        infoEl.innerHTML = `
                            <h5>${data.title || 'Animation'}</h5>
                            <p>${data.description || ''}</p>
                            <p>Total Frames: ${frames.length}</p>
                        `;
                        infoEl.style.display = 'block';
                    }
                    
                    // Set up simple animation controls
                    const playBtn = document.getElementById('animationPlay');
                    const pauseBtn = document.getElementById('animationPause');
                    const progressEl = document.getElementById('animationProgress');
                    const currentFrameEl = document.getElementById('currentFrame');
                    
                    // Initialize progress bar
                    if (progressEl) {
                        progressEl.min = 0;
                        progressEl.max = frames.length - 1;
                        progressEl.value = 0;
                    }
                    
                    let currentFrameIndex = 0;
                    let animInterval = null;
                    
                    function updateFrameDisplay() {
                        // Hide all frames
                        const frameImgs = framesContainer.querySelectorAll('.animation-frame');
                        frameImgs.forEach(img => img.style.display = 'none');
                        
                        // Show current frame
                        frameImgs[currentFrameIndex].style.display = 'block';
                        
                        // Update progress and counter
                        if (progressEl) progressEl.value = currentFrameIndex;
                        if (currentFrameEl) {
                            currentFrameEl.textContent = `Frame: ${currentFrameIndex + 1}/${frames.length}`;
                        }
                    }
                    
                    function nextFrame() {
                        currentFrameIndex = (currentFrameIndex + 1) % frames.length;
                        updateFrameDisplay();
                    }
                    
                    // Play button
                    if (playBtn) {
                        playBtn.addEventListener('click', function() {
                            if (animInterval) clearInterval(animInterval);
                            const frameDelay = 1000 / Math.max(1, Math.min(10, parseFloat(speed) || 1));
                            animInterval = setInterval(nextFrame, frameDelay);
                        });
                    }
                    
                    // Pause button
                    if (pauseBtn) {
                        pauseBtn.addEventListener('click', function() {
                            if (animInterval) {
                                clearInterval(animInterval);
                                animInterval = null;
                            }
                        });
                    }
                    
                    // Progress slider
                    if (progressEl) {
                        progressEl.addEventListener('input', function() {
                            if (animInterval) {
                                clearInterval(animInterval);
                                animInterval = null;
                            }
                            currentFrameIndex = parseInt(this.value);
                            updateFrameDisplay();
                        });
                    }
                    
                    // Start the animation automatically
                    setTimeout(() => {
                        if (playBtn) playBtn.click();
                    }, 500);
                } else {
                    // No frames, show error
                    const resultElement = document.getElementById('animationResult');
                    if (resultElement) {
                        resultElement.innerHTML = `
                            <div class="alert alert-warning">
                                <strong>Note:</strong> No animation frames received. 
                                ${data.message || 'Try a different animation type or check console for errors.'}
                            </div>
                        `;
                    }
                }
            })
            .catch(error => {
                console.error('Animation error:', error);
                const resultElement = document.getElementById('animationResult');
                if (resultElement) {
                    resultElement.innerHTML = `
                        <div class="alert alert-danger">
                            <strong>Error:</strong> ${error.message || 'An error occurred while processing your request.'}
                        </div>
                    `;
                }
                if (loadingEl) loadingEl.style.display = 'none';
            });
    });
}

// Function to load MATLAB source code
function loadMatlabSourceCode(functionName, elementId) {
    const targetElement = document.getElementById(elementId);
    if (!targetElement) {
        console.error(`Element with ID ${elementId} not found`);
        return;
    }
    
    // Add loading indicator
    targetElement.innerHTML = '<div class="spinner-border spinner-border-sm text-primary me-2" role="status"></div> Loading MATLAB code...';
    
    // Fetch source code from server
    fetch(`/source_code/${functionName}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success' && data.source_code) {
                // Display the source code with syntax highlighting
                targetElement.textContent = data.source_code;
                // Re-initialize syntax highlighting
                hljs.highlightElement(targetElement);
                console.log(`Loaded source code for ${functionName}`);
            } else {
                // Display error message
                targetElement.innerHTML = `<div class="alert alert-warning">
                    <strong>Note:</strong> Could not load MATLAB source code.
                    ${data.message || 'The source file may not exist.'}
                </div>`;
            }
        })
        .catch(error => {
            console.error(`Error loading source code: ${error}`);
            targetElement.innerHTML = `<div class="alert alert-danger">
                <strong>Error:</strong> Failed to load source code.
                ${error.message || 'Unknown error occurred.'}
            </div>`;
        });
}

// Setup Symbolic Math operations
function setupSymbolicMath() {
    const form = document.getElementById('symbolic-form');
    const loadingEl = document.getElementById('symbolic-loading');
    const resultEl = document.getElementById('symbolic-result');
    const resultTextEl = document.getElementById('symbolic-result-text');
    const plotContainer = document.getElementById('symbolic-plot-container');
    const plotImg = document.getElementById('symbolic-plot');
    
    if (!form) return;
    
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        // Get input values
        const expression = document.getElementById('symbolic-expression').value.trim();
        const operation = document.querySelector('input[name="operation"]:checked').value;
        
        if (!expression) {
            alert('Please enter a valid mathematical expression.');
            return;
        }
        
        // Show loading indicator
        loadingEl.style.display = 'block';
        resultEl.style.display = 'none';
        plotContainer.style.display = 'none';
        
        // Send request to backend
        fetch('/symbolic', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                expression: expression,
                operation: operation
            })
        })
        .then(response => response.json())
        .then(data => {
            // Hide loading indicator
            loadingEl.style.display = 'none';
            
            if (data.status === 'success') {
                // Show result
                resultEl.style.display = 'block';
                
                // Display LaTeX if available, otherwise plain text
                if (data.latex) {
                    resultTextEl.innerHTML = '\\[' + data.latex + '\\]';
                    // Render LaTeX if MathJax is available
                    if (window.MathJax) {
                        MathJax.typeset();
                    }
                } else {
                    resultTextEl.textContent = data.result;
                }
                
                // Display plot if available
                if (data.plot && operation === 'plot') {
                    plotContainer.style.display = 'flex';
                    plotImg.src = 'data:image/png;base64,' + data.plot;
                }
            } else {
                resultEl.style.display = 'block';
                resultTextEl.innerHTML = `<div class="alert alert-danger">\n                    <strong>Error:</strong> ${data.message || 'An error occurred while processing your request.'}\n                </div>`;
            }
        })
        .catch(error => {
            loadingEl.style.display = 'none';
            resultEl.style.display = 'block';
            resultTextEl.innerHTML = `<div class="alert alert-danger">\n                <strong>Error:</strong> ${error.message || 'An error occurred while processing your request.'}\n            </div>`;
            console.error('Symbolic math error:', error);
        });
    });
}

 