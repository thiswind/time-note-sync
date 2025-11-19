// Settings page JavaScript for calendar sync controls

document.addEventListener('DOMContentLoaded', function() {
    const autoSyncCheckbox = document.getElementById('autoSync');
    const manualSyncBtn = document.getElementById('manualSyncBtn');
    const syncStatusDiv = document.getElementById('syncStatus');
    const syncStatusMessage = document.getElementById('syncStatusMessage');

    // Load current sync settings
    async function loadSyncSettings() {
        try {
            // TODO: Implement GET /api/user/settings endpoint to load sync preferences
            // For now, default to false
            autoSyncCheckbox.checked = false;
        } catch (error) {
            console.error('Error loading sync settings:', error);
        }
    }

    // Save sync settings
    async function saveSyncSettings(enabled) {
        try {
            // TODO: Implement PUT /api/user/settings endpoint to save sync preferences
            // For now, just log
            console.log('Auto sync:', enabled ? 'enabled' : 'disabled');
        } catch (error) {
            console.error('Error saving sync settings:', error);
            alert('保存设置失败: ' + error.message);
        }
    }

    // Handle auto sync toggle
    if (autoSyncCheckbox) {
        autoSyncCheckbox.addEventListener('change', function() {
            saveSyncSettings(this.checked);
        });
    }

    // Handle manual sync
    if (manualSyncBtn) {
        manualSyncBtn.addEventListener('click', async function() {
            if (this.disabled) return;
            
            this.disabled = true;
            this.textContent = '同步中...';
            syncStatusDiv.style.display = 'block';
            syncStatusMessage.textContent = '正在同步...';
            syncStatusMessage.className = 'sync-status-message pending';

            try {
                const result = await SyncAPI.sync();
                syncStatusMessage.textContent = `同步完成：成功 ${result.success} 条，失败 ${result.failed} 条`;
                syncStatusMessage.className = 'sync-status-message success';
                
                // Refresh journal list if on home page
                if (window.location.pathname === '/' || window.location.pathname === '/home') {
                    const activeTab = document.querySelector('.tab-btn.active');
                    if (activeTab) {
                        const tab = activeTab.dataset.tab;
                        if (tab === 'all') {
                            loadJournalList('all');
                        } else if (tab === 'today') {
                            const today = new Date().toISOString().split('T')[0];
                            loadJournalList('today', today);
                        } else if (tab === 'date') {
                            const datePicker = document.getElementById('datePicker');
                            if (datePicker && datePicker.value) {
                                loadJournalList('date', datePicker.value);
                            }
                        }
                    }
                }
            } catch (error) {
                syncStatusMessage.textContent = '同步失败: ' + error.message;
                syncStatusMessage.className = 'sync-status-message error';
                alert('同步失败: ' + error.message);
            } finally {
                this.disabled = false;
                this.textContent = '手动同步';
                setTimeout(() => {
                    syncStatusDiv.style.display = 'none';
                }, 5000);
            }
        });
    }

    // Load settings on page load
    loadSyncSettings();
});

