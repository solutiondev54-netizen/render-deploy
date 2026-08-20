// --- MAAE Core: Standalone Visual & Character Engine ---
window.MAAEVisuals = {
    activeCharacter: "African Cinematic Subject",

    setCharacter: function(charName) {
        this.activeCharacter = charName;
        console.log("Active character updated to:", charName);
    },

    renderVisual: async function(mode = 'cinematic') {
        const feed = document.getElementById('video-feed');
        const promptInput = document.getElementById('prompt-input');
        const userPrompt = promptInput ? promptInput.value.trim() : "";
        
        if (!feed) return;

        feed.style.backgroundImage = 'none';
        feed.innerHTML = `<div style="display:flex; justify-content:center; align-items:center; height:100%; color:#f59e0b; font-weight:600; font-size:0.85rem;">Synthesizing Non-AI Cinematic Frame...</div>`;

        // Modifiers to ensure a raw, professional, non-artificial look
        const realismEnhancers = "shot on 35mm lens, Fujifilm Eterna film stock, natural skin texture, anamorphic lighting, professional color grading, photorealistic, 8k resolution, film grain";
        
        const finalPrompt = userPrompt 
            ? `${userPrompt}, featuring ${this.activeCharacter}, ${realismEnhancers}` 
            : `Cinematic portrait of ${this.activeCharacter}, ${realismEnhancers}`;

        try {
            const response = await fetch('/api/render-video', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    prompt: finalPrompt, 
                    mode: mode, 
                    character: this.activeCharacter 
                })
            });
            
            const data = await response.json();
            
            if (data.status === "success" || data.url) {
                feed.style.backgroundImage = `url('${data.url || data.image_url}')`;
                feed.style.backgroundSize = "cover";
                feed.style.backgroundPosition = "center";
                feed.innerHTML = ""; 
            } else {
                feed.innerHTML = `<span style="color: #ef4444; font-size: 0.8rem; padding: 10px;">Render failed: ${data.message || 'Unknown error'}</span>`;
            }
        } catch (e) {
            feed.innerHTML = `<span style="color: #ef4444; font-size: 0.8rem; padding: 10px;">Connection error: ${e.message}</span>`;
        }
    }
};
