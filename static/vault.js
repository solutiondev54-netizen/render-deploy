// MAAE Core: Premium Local Vault Engine & UI Controller
class MAAEVaultManager {
    constructor(storageKey = 'maae_core_secure_vault_v2') {
        this.storageKey = storageKey;
    }

    getVault() {
        try {
            const rawData = localStorage.getItem(this.storageKey);
            return rawData ? JSON.parse(rawData) : [];
        } catch (error) {
            console.error("Vault access error:", error);
            return [];
        }
    }

    saveScript(scriptData) {
        const vault = this.getVault();
        const entry = {
            id: 'script_' + Date.now(),
            title: scriptData.title || 'Untitled Production',
            content: scriptData.content,
            timestamp: new Date().toLocaleDateString(),
            metrics: {
                retentionScore: scriptData.retentionScore || '94% Retention',
                topCharacter: scriptData.topCharacter || 'Papa Kofi',
                renderWeight: scriptData.renderWeight || 'Pro Tier'
            }
        };
        vault.unshift(entry);
        localStorage.setItem(this.storageKey, JSON.stringify(vault));
        return entry;
    }

    deleteScript(id) {
        let vault = this.getVault();
        vault = vault.filter(script => script.id !== id);
        localStorage.setItem(this.storageKey, JSON.stringify(vault));
        return vault;
    }

    purgeVault() {
        localStorage.removeItem(this.storageKey);
        return [];
    }
}

// Initialize global vault instance
const maaeVault = new MAAEVaultManager();

window.saveCurrentWorkspaceToVault = () => {
    const workspace = document.getElementById('workspace');
    if (!workspace || !workspace.value.trim()) {
        alert("Please generate or write a script in the workspace first.");
        return;
    }
    
    maaeVault.saveScript({
        title: 'Production ' + new Date().toLocaleTimeString(),
        content: workspace.value,
        retentionScore: '96% Score',
        topCharacter: 'Mama Akos',
        renderWeight: 'High Impact'
    });

    alert("Script successfully secured to your private local vault.");
};

// --- Premium Vault Clearing & Purge Extension ---
window.confirmAndClearVault = () => {
    const vault = maaeVault.getVault();
    
    if (vault.length === 0) {
        alert("Your vault is already empty.");
        return;
    }

    const userConfirmed = confirm("SECURE VAULT PURGE:\n\nAre you sure you want to permanently clear all saved productions from your local vault? This action cannot be undone.");
    
    if (userConfirmed) {
        maaeVault.purgeVault();
        alert("Vault successfully purged. All local production data has been cleared.");
        
        // Optional: Refresh any active vault UI list if present
        if (typeof window.renderVaultUI === 'function') {
            window.renderVaultUI();
        }
    }
};
