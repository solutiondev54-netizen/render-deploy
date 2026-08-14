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

// --- Premium Frosted-Glass Vault UI Modal Extension ---
window.toggleVaultModal = () => {
    let modalOverlay = document.getElementById('maae-vault-modal');
    
    if (modalOverlay) {
        modalOverlay.remove();
        return;
    }

    const vaultData = maaeVault.getVault();

    modalOverlay = document.createElement('div');
    modalOverlay.id = 'maae-vault-modal';
    modalOverlay.style.cssText = `
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(13, 17, 23, 0.85); backdrop-filter: blur(8px);
        z-index: 9999; display: flex; justify-content: center; align-items: center; padding: 16px;
    `;

    let itemsHtml = vaultData.length === 0 ? 
        `<div style="text-align: center; color: #9caaf; padding: 40px 0;">No productions stored in your vault yet.</div>` :
        vaultData.map(item => `
            <div style="background: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 12px; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                    <span style="color: #f2c94c; font-size: 13px; font-weight: 700;">${item.title}</span>
                    <span style="color: #9caaf; font-size: 10px;">${item.timestamp}</span>
                </div>
                <div style="color: #c9d1d9; font-size: 12px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-bottom: 8px;">
                    ${item.content}
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="background: #1f2937; color: #f2c94c; font-size: 9px; padding: 2px 6px; border-radius: 4px;">${item.metrics.retentionScore}</span>
                    <button onclick="window.deleteVaultItem('${item.id}')" style="background: transparent; color: #ff5c5c; border: none; font-size: 11px; cursor: pointer; font-weight: 600;">Delete</button>
                </div>
            </div>
        `).join('');

    modalOverlay.innerHTML = `
        <div style="background: #0b0f19; border: 1px solid #30363d; border-radius: 14px; width: 100%; max-width: 420px; max-height: 80vh; display: flex; flex-direction: column; overflow: hidden; box-shadow: 0 16px 32px rgba(0,0,0,0.5);">
            <div style="padding: 16px; border-bottom: 1px solid #30363d; display: flex; justify-content: space-between; align-items: center; background: #161b22;">
                <div>
                    <h3 style="color: #f3f4f6; font-size: 15px; margin: 0; font-weight: 800;">SECURE SCRIPT VAULT</h3>
                    <span style="color: #9caaf; font-size: 11px;">Isolated Local Storage Matrix</span>
                </div>
                <button onclick="toggleVaultModal()" style="background: #1f2937; color: #f3f4f6; border: none; width: 28px; height: 28px; border-radius: 50%; cursor: pointer; font-weight: bold;">✕</button>
            </div>
            
            <div style="padding: 16px; overflow-y: auto; flex: 1;">
                ${itemsHtml}
            </div>

            <div style="padding: 12px 16px; border-top: 1px solid #30363d; background: #161b22; display: flex; justify-content: space-between; align-items: center;">
                <button onclick="confirmAndClearVault()" style="background: transparent; color: #ff5c5c; border: 1px solid #ff5c5c; padding: 6px 12px; border-radius: 6px; font-size: 11px; font-weight: 600; cursor: pointer;">Purge Vault</button>
                <span style="color: #9caaf; font-size: 11px;">Total: ${vaultData.length}</span>
            </div>
        </div>
    `;

    document.body.appendChild(modalOverlay);
};

window.deleteVaultItem = (id) => {
    maaeVault.deleteScript(id);
    toggleVaultModal();
    toggleVaultModal(); // Refresh modal view
};

window.confirmAndClearVault = () => {
    if (confirm("Are you sure you want to permanently clear all items from your vault?")) {
        maaeVault.purgeVault();
        toggleVaultModal();
        alert("Vault has been completely cleared.");
    }
};
