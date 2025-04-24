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
            result: resultEl
        });
        
        // Make a direct API request
        console.log("Fetching animation data...");
        fetch('/api/animation?animation_type=pendulum&num_frames=10')
            .then(response => {
                console.log("API response received", response);
                return response.json();
            })
            .then(data => {
                console.log("Animation data:", data);
                console.log("Data type:", typeof data);
                console.log("Data keys:", Object.keys(data));
                
                if (data.frames) {
                    console.log("Frames type:", typeof data.frames);
                    console.log("Frames is array:", Array.isArray(data.frames));
                    console.log("Frames length:", data.frames.length);
                    console.log("First frame preview (first 100 chars):", data.frames[0].substring(0, 100) + "...");
                }
                
                loadingEl.style.display = 'none';
                
                if (data.frames && data.frames.length > 0) {
                    console.log(`Received ${data.frames.length} frames`);
                    
                    // Display the first frame as a test
                    const testFrame = document.createElement('img');
                    testFrame.src = `data:image/png;base64,${data.frames[0]}`;
                    testFrame.alt = "Animation Frame";
                    testFrame.className = "img-fluid";
                    testFrame.style.border = "2px solid red";
                    testFrame.style.maxWidth = "100%";
                    
                    framesEl.appendChild(testFrame);
                    
                    document.getElementById('animationWrapper').style.display = 'block';
                    
                    resultEl.innerHTML = `
                        <div class="alert alert-success mt-3">
                            <strong>Success!</strong> Loaded ${data.frames.length} frames.
                            Check the console for more details.
                        </div>
                    `;
                } else {
                    console.error("No frames received in animation data");
                    resultEl.innerHTML = `
                        <div class="alert alert-danger">
                            <strong>Error:</strong> No animation frames received.
                            Check the console for details.
                        </div>
                    `;
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