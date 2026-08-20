// --- MAAE Core: Professional Cinematic Visual Engine ---
window.MAAEVisuals = {
    activeCharacter: "African Cinematic Subject",

    setCharacter: function(charName) {
        this.activeCharacter = charName;
        console.log("Studio Active Character Updated:", charName);
    },

    renderVisual: async function() {
        const feed = document.getElementById('video-feed');
        const promptInput = document.getElementById('prompt-input');
        const userPrompt = promptInput ? promptInput.value.trim() : "";
        
        if (!feed) return;

        // Premium loading state matching studio theme
        feed.style.backgroundImage = 'none';
        feed.innerHTML = `
            <div style="display:flex; flex-direction:column; justify-content:center; align-items:center; height:100%; color:#f59e0b; font-family:system-ui, sans-serif; text-align:center; padding: 20px;">
                <div style="font-weight:700; font-size:0.95rem; margin-bottom: 6px; letter-spacing: 0.05em;">SYNTHESIZING CINEMATIC FRAME</div>
                <div style="font-size:0.75rem; color:#9ca3af;">Applying 35mm lens optics & professional color grading...</div>
            </div>`;

        // High-end modifiers to eliminate the generic "AI look"
        const realismEnhancers = "shot on 35mm lens, Fujifilm Eterna film stock, natural skin texture, anamorphic lighting, professional color grading, photorealistic, 8k resolution, film grain, cinematic composition";
        
        const finalPrompt = userPrompt 
            ? `${userPrompt}, featuring ${this.activeCharacter}, ${realismEnhancers}` 
            : `Cinematic professional portrait of ${this.activeCharacter}, ${realismEnhancers}`;

        try {
            const response = await fetch('/api/render-video', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    prompt: finalPrompt, 
                    character: this.activeCharacter,
                    quality: "cinematic"
                })
            });
            
            const data = await response.json();
            
            if (data.status === "success" || data.url) {
                feed.style.backgroundImage = `url('${data.url || data.image_url}')`;
                feed.style.backgroundSize = "cover";
                feed.style.backgroundPosition = "center";
                feed.innerHTML = ""; 
            } else {
                feed.innerHTML = `<div style="color: #ef4444; font-size: 0.8rem; padding: 20px; text-align:center;">Render Warning: ${data.message || 'Studio pipeline busy.'}</div>`;
            }
        } catch (e) {
            feed.innerHTML = `<div style="color: #ef4444; font-size: 0.8rem; padding: 20px; text-align:center;">Connection Error: Please check network uplink.</div>`;
        }
    }
};

// Map to global shorthand function for existing button triggers
window.generatePremiumLocalVisual = () => window.MAAEVisuals.renderVisual();
