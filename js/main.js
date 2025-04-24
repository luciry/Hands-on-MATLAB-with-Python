// MATLAB with Python Integration - Main JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize syntax highlighting
    document.querySelectorAll('pre code').forEach((block) => {
        hljs.highlightBlock(block);
    });

    // Setup tabs for result/code views
    setupTabSwitching();
    
    // Initialize all examples
    initSimplePlot();
    initAdvancedPlot();
    initDifferentialEquation();
    initImageProcessing();
    initAnimation();
});

// Tab switching between results and code
function setupTabSwitching() {
    document.querySelectorAll('.nav-link').forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('data-bs-target');
            
            // Hide all tab content
            document.querySelectorAll('.tab-pane').forEach(pane => {
                pane.classList.remove('show', 'active');
            });
            
            // Show target tab content
            document.querySelector(targetId).classList.add('show', 'active');
            
            // Update active tab
            document.querySelectorAll('.nav-link').forEach(t => {
                t.classList.remove('active');
            });
            this.classList.add('active');
        });
    });
}

// Error handling for API calls
function handleApiError(error, elementId) {
    const resultElement = document.getElementById(elementId);
    resultElement.innerHTML = `<div class="alert alert-danger">
        <strong>Error:</strong> ${error.message || 'An error occurred while processing your request.'}
    </div>`;
    console.error('API Error:', error);
}

// Simple Plot Example
function initSimplePlot() {
    const runButton = document.getElementById('runSimplePlot');
    if (!runButton) return;
    
    runButton.addEventListener('click', function() {
        const resultElement = document.getElementById('simplePlotResult');
        resultElement.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>';
        
        fetch('/api/simple_plot')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                resultElement.innerHTML = `<img src="data:image/png;base64,${data.plot}" class="img-fluid" alt="Simple Plot">`;
            })
            .catch(error => handleApiError(error, 'simplePlotResult'));
    });
}

// Advanced Plot Example
function initAdvancedPlot() {
    const runButton = document.getElementById('runAdvancedPlot');
    if (!runButton) return;
    
    runButton.addEventListener('click', function() {
        const resultElement = document.getElementById('advancedPlotResult');
        resultElement.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>';
        
        fetch('/api/advanced_plot')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                resultElement.innerHTML = `<img src="data:image/png;base64,${data.plot}" class="img-fluid" alt="Advanced Plot">`;
            })
            .catch(error => handleApiError(error, 'advancedPlotResult'));
    });
}

// Differential Equation Example
function initDifferentialEquation() {
    const runButton = document.getElementById('runDifferentialEq');
    if (!runButton) return;
    
    runButton.addEventListener('click', function() {
        const resultElement = document.getElementById('differentialEqResult');
        resultElement.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>';
        
        fetch('/api/differential_equation')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                resultElement.innerHTML = `<img src="data:image/png;base64,${data.plot}" class="img-fluid" alt="Differential Equation Solution">`;
            })
            .catch(error => handleApiError(error, 'differentialEqResult'));
    });
}

// Image Processing Example
function initImageProcessing() {
    const runButton = document.getElementById('runImageProcessing');
    const noiseLevel = document.getElementById('noiseLevel');
    if (!runButton || !noiseLevel) return;
    
    runButton.addEventListener('click', function() {
        const resultElement = document.getElementById('imageProcessingResult');
        resultElement.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>';
        
        fetch(`/api/image_processing?noise_level=${noiseLevel.value}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                resultElement.innerHTML = `
                    <div class="row">
                        <div class="col-md-6">
                            <h5>Original Image with Noise</h5>
                            <img src="data:image/png;base64,${data.noisy_image}" class="img-fluid" alt="Noisy Image">
                        </div>
                        <div class="col-md-6">
                            <h5>Filtered Image</h5>
                            <img src="data:image/png;base64,${data.filtered_image}" class="img-fluid" alt="Filtered Image">
                        </div>
                    </div>`;
            })
            .catch(error => handleApiError(error, 'imageProcessingResult'));
    });
}

// Animation Example
function initAnimation() {
    const runButton = document.getElementById('runAnimation');
    const numFrames = document.getElementById('numFrames');
    const animationSpeed = document.getElementById('animationSpeed');
    if (!runButton || !numFrames || !animationSpeed) return;
    
    runButton.addEventListener('click', function() {
        const resultElement = document.getElementById('animationResult');
        resultElement.innerHTML = '<div class="text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>';
        
        fetch(`/api/animation?num_frames=${numFrames.value}&speed=${animationSpeed.value}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log("Animation data received:", data);
                
                if (data.frames && data.frames.length > 0) {
                    // Create an animated display of frames
                    const frameContainer = document.createElement('div');
                    frameContainer.className = 'animation-container';
                    
                    // Add title and description
                    const infoDiv = document.createElement('div');
                    infoDiv.className = 'animation-info text-center mb-2';
                    infoDiv.innerHTML = `<h5>${data.title || 'Animation'}</h5>
                                        <p>${data.description || ''}</p>`;
                    frameContainer.appendChild(infoDiv);
                    
                    // Create img element for the animation
                    const img = document.createElement('img');
                    img.className = 'img-fluid animation-frame';
                    img.alt = 'MATLAB Animation';
                    
                    // Set the first frame as initial display
                    img.src = `data:image/png;base64,${data.frames[0]}`;
                    frameContainer.appendChild(img);
                    
                    // Add controls for playback
                    const controlsDiv = document.createElement('div');
                    controlsDiv.className = 'animation-controls mt-2';
                    controlsDiv.innerHTML = `
                        <div class="d-flex justify-content-center align-items-center">
                            <button id="animPlay" class="btn btn-sm btn-primary me-2">
                                <i class="fas fa-play"></i>
                            </button>
                            <button id="animPause" class="btn btn-sm btn-secondary me-2">
                                <i class="fas fa-pause"></i>
                            </button>
                            <span id="frameCounter" class="mx-2">Frame 1/${data.frames.length}</span>
                        </div>
                    `;
                    frameContainer.appendChild(controlsDiv);
                    
                    // Replace the result element with our animation display
                    resultElement.innerHTML = '';
                    resultElement.appendChild(frameContainer);
                    
                    // Setup animation playback
                    let currentFrame = 0;
                    let animInterval = null;
                    const speed = parseFloat(animationSpeed.value) || 1;
                    const frameDelay = 1000 / Math.max(1, Math.min(10, speed)); // Limit between 1-10 fps
                    
                    function updateFrame() {
                        currentFrame = (currentFrame + 1) % data.frames.length;
                        img.src = `data:image/png;base64,${data.frames[currentFrame]}`;
                        document.getElementById('frameCounter').textContent = `Frame ${currentFrame + 1}/${data.frames.length}`;
                    }
                    
                    document.getElementById('animPlay').addEventListener('click', function() {
                        if (animInterval) clearInterval(animInterval);
                        animInterval = setInterval(updateFrame, frameDelay);
                    });
                    
                    document.getElementById('animPause').addEventListener('click', function() {
                        if (animInterval) {
                            clearInterval(animInterval);
                            animInterval = null;
                        }
                    });
                    
                    // Auto-start the animation
                    setTimeout(() => {
                        document.getElementById('animPlay').click();
                    }, 500);
                } else if (data.animation) {
                    // Fallback to single image if no frames
                    resultElement.innerHTML = `<img src="data:image/png;base64,${data.animation}" class="img-fluid" alt="MATLAB Animation">`;
                } else {
                    throw new Error('No animation data received');
                }
            })
            .catch(error => {
                console.error('Animation error:', error);
                handleApiError(error, 'animationResult');
            });
    });
} 