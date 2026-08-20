// --- MAAE Core: Professional Cinematic Visual Engine ---
window.MAAEVisuals = {
    activeCharacter: "African Cinematic Subject",

    renderVisual: async function() {
        const visualOutput = document.getElementById('final-visual-output');
        const statusText = document.getElementById('feed-status-text');
        const promptInput = document.getElementById('plot-input') || document.getElementById('prompt-input');
        const userPrompt = promptInput ? promptInput.value.trim() : "";
        
        if (!visualOutput) return;

        // Apply loading state to matching HTML structure
        if (statusText) {
            statusText.innerHTML = `
                <div style="font-weight:700; font-size:0.95rem; margin-bottom: 6px; color:#f59e0b;">SYNTHESIZING CINEMATIC FRAME...</div>
                <div style="font-size:0.75rem; color:#9ca3af;">Applying 35mm lens optics & professional color grading...</div>`;
        }

        const realismEnhancers = "shot on 35mm lens, Fujifilm Eterna film stock, natural skin texture, anamorphic lighting, professional color grading, photorealistic, 8k resolution, film grain";
        const finalPrompt = userPrompt ? `${userPrompt}, ${realismEnhancers}` : `Cinematic professional studio shot, ${realismEnhancers}`;

        try {
            const response = await fetch('/api/render-video', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt: finalPrompt })
            });
            
            const data = await response.json();
            
            if (data.status === "success" || data.url) {
                visualOutput.style.backgroundImage = `url('${data.url || data.image_url}')`;
                visualOutput.style.backgroundSize = "cover";
                visualOutput.style.backgroundPosition = "center";
                if (statusText) statusText.innerHTML = ""; 
            } else {
                if (statusText) statusText.innerHTML = `<span style="color: #ef4444;">Render failed: ${data.message || 'Unknown error'}</span>`;
            }
        } catch (e) {
            if (statusText) statusText.innerHTML = `<span style="color: #ef4444;">Connection error: ${e.message}</span>`;
        }
    }
};

window.generatePremiumLocalVisual = () => window.MAAEVisuals.renderVisual();
