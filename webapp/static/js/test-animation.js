// Simple Animation Test Script
document.addEventListener('DOMContentLoaded', function() {
    console.log("Animation test script loaded");
    
    // Get animation button
    const animBtn = document.getElementById('animationBtn');
    if (!animBtn) {
        console.error("Animation button not found!");
        return;
    }
    
    // Add click handler
    animBtn.addEventListener('click', function() {
        console.log("Animation button clicked");
        testAnimationLoad();
    });
    
    function testAnimationLoad() {
        const loadingEl = document.getElementById('animationLoading');
        const resultEl = document.getElementById('animationResult');
        const framesEl = document.getElementById('animationFrames');
        const controlsEl = document.getElementById('animationControls');
        
        if (!loadingEl || !resultEl || !framesEl) {
            console.error("Required animation elements not found", {
                loading: !!loadingEl,
                result: !!resultEl,
                frames: !!framesEl
            });
            return;
        }
        
        // Show loading, hide result
        loadingEl.style.display = 'block';
        resultEl.innerHTML = '';
        framesEl.innerHTML = '';
        
        // Log elements and their visibility
        console.log("Animation elements:", {
            loading: loadingEl,
            loadingVisible: loadingEl.style.display,
            frames: framesEl,
            controls: controlsEl,
            result: resultEl
        });
        
        // Get selected animation type and number of frames from the UI
        const animType = document.getElementById('animationType').value || 'pendulum';
        const numFrames = document.getElementById('numFrames').value || 10;
        
        console.log(`Using animation type: ${animType}, frames: ${numFrames}`);
        
        // Make a direct API request with the selected parameters
        console.log("Fetching animation data...");
        fetch(`/api/animation?animation_type=${animType}&num_frames=${numFrames}`)
            .then(response => {
                console.log("API response received", response);
                return response.json();
            })
            .then(data => {
                console.log("Animation data:", data);
                console.log("Data type:", typeof data);
                console.log("Data keys:", Object.keys(data));
                
                // Access frames directly from data.frames (not data.data.frames)
                if (data.frames) {
                    console.log("Frames type:", typeof data.frames);
                    console.log("Frames is array:", Array.isArray(data.frames));
                    console.log("Frames length:", data.frames.length);
                    if (data.frames.length > 0 && typeof data.frames[0] === 'string') {
                        console.log("First frame preview (first 100 chars):", data.frames[0].substring(0, 100) + "...");
                    } else if (data.frames.length === 0) {
                        console.log("Frames array is empty.");
                    } else {
                        console.log("First frame is not a string or frames array is empty.");
                    }
                    
                    // Debug: Log the first few frames
                    for (let i = 0; i < Math.min(5, data.frames.length); i++) {
                        console.log(`Frame ${i+1} data type: ${typeof data.frames[i]}, starts with: ${data.frames[i].substring(0, 30)}...`);
                    }
                }
                
                loadingEl.style.display = 'none';
                
                // Use data.frames for the main condition and processing
                if (data.frames && data.frames.length > 0) {
                    console.log(`Received ${data.frames.length} frames`);
                    
                    // Clear previous content
                    framesEl.innerHTML = '';
                    
                    // Create frame elements for all frames
                    data.frames.forEach((frameData, index) => {
                        const frameEl = document.createElement('img');
                        frameEl.className = 'animation-frame img-fluid';
                        // Add timestamp to prevent caching
                        const timestamp = new Date().getTime();
                        // Set the image source with cache-busting parameter
                        frameEl.src = frameData + '?t=' + timestamp + '-' + index;
                        console.log(`Frame ${index+1} data type: ${typeof frameData}, starts with: ${frameData.substring(0, 30)}...`);
                        frameEl.style.display = index === 0 ? 'block' : 'none';
                        frameEl.dataset.frameIndex = index;
                        framesEl.appendChild(frameEl);
                    });
                    
                    // Show the container and controls
                    document.getElementById('animationWrapper').style.display = 'block';
                    
                    // Make sure controls are visible - IMPORTANT: this line is critical
                    if (controlsEl) {
                        controlsEl.style.display = 'flex'; // Or 'block', depending on layout
                        console.log("Animation controls made visible");
                    } else {
                        console.error("Animation controls element not found!");
                    }

                    // Animation playback variables
                    let currentFrameIndex = 0;
                    let animInterval = null;
                    const frameDelay = 100; // ms, adjust as needed
                    const allFrames = Array.from(framesEl.querySelectorAll('.animation-frame'));
                    
                    const playBtn = document.getElementById('animationPlay');
                    const pauseBtn = document.getElementById('animationPause');
                    const progressSlider = document.getElementById('animationProgress');
                    const frameCounter = document.getElementById('currentFrame');
                    
                    // Update max value for the progress slider
                    if (progressSlider) {
                        progressSlider.min = 0;
                        progressSlider.max = data.frames.length - 1;
                        progressSlider.value = 0;
                    }
                    
                    // Function to update which frame is displayed
                    function updateFrameDisplay() {
                        // Hide all frames
                        allFrames.forEach(img => img.style.display = 'none');
                        // Show current frame
                        if (allFrames[currentFrameIndex]) {
                            allFrames[currentFrameIndex].style.display = 'block';
                        }
                        // Update counter and slider
                        if (progressSlider) progressSlider.value = currentFrameIndex;
                        if (frameCounter) {
                            frameCounter.textContent = `Frame: ${currentFrameIndex + 1}/${allFrames.length}`;
                        }
                    }
                    
                    // Function to advance to next frame
                    function nextFrame() {
                        currentFrameIndex = (currentFrameIndex + 1) % allFrames.length;
                        updateFrameDisplay();
                    }
                    
                    // Play button
                    if (playBtn) {
                        playBtn.addEventListener('click', function() {
                            if (animInterval) clearInterval(animInterval);
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
                    if (progressSlider) {
                        progressSlider.addEventListener('input', function() {
                            if (animInterval) {
                                clearInterval(animInterval);
                                animInterval = null;
                            }
                            currentFrameIndex = parseInt(this.value);
                            updateFrameDisplay();
                        });
                    }
                    
                    // Start playing automatically
                    setTimeout(() => {
                        if (playBtn) playBtn.click();
                    }, 500);
                } else {
                    console.error("No frames received in animation data (expected data.frames)");
                    resultEl.innerHTML = `
                        <div class="alert alert-danger">
                            <strong>Error:</strong> No animation frames received.
                            Check the console for details.
                        </div>
                    `;
                    console.log("Data received:", data);
                    if (data.frames) {
                        console.log("Frames array exists but may be empty. Length:", data.frames.length);
                    }
                }
            })
            .catch(error => {
                console.error("Animation fetch error:", error);
                loadingEl.style.display = 'none';
                resultEl.innerHTML = `
                    <div class="alert alert-danger">
                        <strong>Error:</strong> ${error.message || "Failed to load animation"}
                    </div>
                `;
            });
    }
}); 