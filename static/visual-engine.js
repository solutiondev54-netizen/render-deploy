// --- MAAE Core: Professional Cinematic Visual Engine (Diagnostic) ---
window.MAAEVisuals = {
    activeCharacter: "African Cinematic Subject",

    renderVisual: async function() {
        const visualOutput = document.getElementById('final-visual-output');
        const statusText = document.getElementById('feed-status-text');
        const promptInput = document.getElementById('plot-input') || document.getElementById('prompt-input');
        const userPrompt = promptInput ? promptInput.value.trim() : "";
        
        if (!visualOutput) return;

        if (statusText) {
            statusText.innerHTML = `
                <div style="font-weight:700; font-size:0.95rem; margin-bottom: 6px; color:#f59e0b;">SYNTHESIZING CINEMATIC FRAME...</div>
                <div style="font-size:0.75rem; color:#9ca3af;">Communicating with backend server...</div>`;
        }

        // Permanent African Cultural & Demographic Lock-in
        const culturalGuardrail = "authentic West African subject, rich natural melanin skin tones, African heritage, natural hair texture";
        const realismEnhancers = "shot on 35mm lens, Fujifilm Eterna film stock, anamorphic lighting, professional color grading, photorealistic, 8k resolution, cinematic composition";
        
        const finalPrompt = userPrompt 
            ? `${userPrompt}, featuring ${culturalGuardrail}, ${realismEnhancers}` 
            : `Cinematic professional portrait of a ${culturalGuardrail}, ${realismEnhancers}`;
       
        try {
            const response = await fetch('/api/render-video', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ prompt: finalPrompt })
            });
            
            const data = await response.json();
            console.log("Backend render response:", data); // Check your browser console for this!
            
        if (data.status === "success" && data.url) {
            visualOutput.style.backgroundImage = `url('${data.url}')`;
            visualOutput.style.backgroundSize = "cover";
            visualOutput.style.backgroundPosition = "center";
            if (statusText) statusText.innerHTML = ""; 
            } else {
                if (statusText) {
                    statusText.innerHTML = `<div style="color: #ef4444; font-size: 0.75rem; padding: 10px;">Server Error: ${data.message || JSON.stringify(data)}</div>`;
                }
            }
        } catch (e) {
            console.error("Render catch error:", e);
            if (statusText) {
                statusText.innerHTML = `<div style="color: #ef4444; font-size: 0.75rem; padding: 10px;">Exception: ${e.message}</div>`;
            }
        }
    }
};

window.generatePremiumLocalVisual = () => window.MAAEVisuals.renderVisual();
