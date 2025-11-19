// Main JavaScript for Personal Journal Web Application
// Vanilla JavaScript implementation (no Vue.js)

// API Base URL
const API_BASE = '/api';

// Journal API functions
const JournalAPI = {
    async listEntries(date = null) {
        const url = date 
            ? `${API_BASE}/journal/entries?date=${date}`
            : `${API_BASE}/journal/entries`;
        const response = await fetch(url, {
            credentials: 'same-origin' // Include cookies for authentication
        });
        if (!response.ok) {
            if (response.status === 401) {
                window.location.href = '/login';
                return;
            }
            throw new Error('Failed to fetch entries');
        }
        const data = await response.json();
        return data.entries || data; // Return entries array directly
    },

    async getEntry(id) {
        const response = await fetch(`${API_BASE}/journal/entries/${id}`, {
            credentials: 'same-origin'
        });
        if (!response.ok) {
            if (response.status === 401) {
                window.location.href = '/login';
                return;
            }
            throw new Error('Failed to fetch entry');
        }
        return response.json();
    },

    async createEntry(entry) {
        const response = await fetch(`${API_BASE}/journal/entries`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'same-origin',
            body: JSON.stringify(entry)
        });
        if (!response.ok) {
            const error = await response.json().catch(() => ({ error: 'Failed to create entry' }));
            throw new Error(error.error || 'Failed to create entry');
        }
        return response.json();
    },

    async updateEntry(id, entry) {
        const response = await fetch(`${API_BASE}/journal/entries/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'same-origin',
            body: JSON.stringify(entry)
        });
        if (!response.ok) {
            const error = await response.json().catch(() => ({ error: 'Failed to update entry' }));
            throw new Error(error.error || 'Failed to update entry');
        }
        return response.json();
    },

    async deleteEntry(id) {
        const response = await fetch(`${API_BASE}/journal/entries/${id}`, {
            method: 'DELETE',
            credentials: 'same-origin'
        });
        if (!response.ok) {
            const error = await response.json().catch(() => ({ error: 'Failed to delete entry' }));
            throw new Error(error.error || 'Failed to delete entry');
        }
        return response.json();
    }
};

// Auth API functions
const AuthAPI = {
    async login(username, password) {
        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        if (!response.ok) throw new Error('Login failed');
        return response.json();
    },

    async logout() {
        const response = await fetch(`${API_BASE}/auth/logout`, {
            method: 'POST'
        });
        return response.json();
    }
};

// Sync API functions
const SyncAPI = {
    async sync() {
        const response = await fetch(`${API_BASE}/calendar/sync`, {
            method: 'POST',
            credentials: 'same-origin'
        });
        if (!response.ok) {
            const error = await response.json().catch(() => ({ error: 'Sync failed' }));
            throw new Error(error.error || 'Sync failed');
        }
        return response.json();
    },

    async syncEntry(entryId) {
        const response = await fetch(`${API_BASE}/journal/entries/${entryId}/sync`, {
            method: 'POST',
            credentials: 'same-origin'
        });
        if (!response.ok) {
            const error = await response.json().catch(() => ({ error: 'Sync failed' }));
            throw new Error(error.error || 'Sync failed');
        }
        return response.json();
    },

    async getSyncStatus() {
        const response = await fetch(`${API_BASE}/calendar/events`, {
            credentials: 'same-origin'
        });
        if (!response.ok) {
            if (response.status === 401) {
                window.location.href = '/login';
                return;
            }
            throw new Error('Failed to get sync status');
        }
        return response.json();
    }
};

// Export API functions
const ExportAPI = {
    async exportEntry(id) {
        const response = await fetch(`${API_BASE}/journal/entries/${id}/export`, {
            method: 'POST',
            credentials: 'same-origin'
        });
        if (!response.ok) {
            const error = await response.json().catch(() => ({ error: 'Export failed' }));
            throw new Error(error.error || 'Export failed');
        }
        return response.json();
    },

    async batchExport(ids) {
        const response = await fetch(`${API_BASE}/journal/entries/batch-export`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'same-origin',
            body: JSON.stringify({ entry_ids: ids })
        });
        if (!response.ok) {
            const error = await response.json().catch(() => ({ error: 'Batch export failed' }));
            throw new Error(error.error || 'Batch export failed');
        }
        return response.json();
    },

    // Handle Shortcuts URL scheme (T092)
    openShortcuts(url) {
        try {
            // Try to open Shortcuts app
            window.location.href = url;
            // If Shortcuts app is not available, show error after timeout (T093)
            setTimeout(() => {
                // Check if we're still on the same page (Shortcuts didn't open)
                // This is a best-effort check - Shortcuts may have opened but page didn't navigate
                console.log('Shortcuts URL opened:', url);
            }, 1000);
        } catch (error) {
            console.error('Error opening Shortcuts:', error);
            throw new Error('无法打开 Shortcuts 应用。请确保已安装 Shortcuts 应用。');
        }
    }
};

// Native App functions
const NativeApp = {
    openCalendar(date) {
        const url = `calshow://${date}`;
        window.location.href = url;
    },

    openNotes() {
        const url = 'shortcuts://run-shortcut?name=ExportToNotes';
        window.location.href = url;
    }
};

// Utility functions
const Utils = {
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('zh-CN', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    },

    formatDateInput(dateString) {
        const date = new Date(dateString);
        return date.toISOString().split('T')[0];
    },

    truncateText(text, maxLength = 100) {
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    }
};

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Tab switching
    const tabButtons = document.querySelectorAll('.tab-btn');
    tabButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const tab = this.dataset.tab;
            
            // Update active state
            tabButtons.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // Show/hide content
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.add('hidden');
            });
            document.getElementById(tab + 'Tab').classList.remove('hidden');
            
            // Load data for active tab
            if (tab === 'all') {
                loadJournalList('all');
            } else if (tab === 'today') {
                const today = new Date().toISOString().split('T')[0];
                loadJournalList('today', today);
            } else if (tab === 'date') {
                const datePicker = document.getElementById('datePicker');
                if (datePicker) {
                    // Initialize date picker to today if not set
                    if (!datePicker.value) {
                        datePicker.value = new Date().toISOString().split('T')[0];
                    }
                    // Load entries for selected date
                    loadJournalList('date', datePicker.value);
                }
            }
        });
    });
    
    // Date navigation
    const datePicker = document.getElementById('datePicker');
    if (datePicker) {
        datePicker.addEventListener('change', function() {
            loadJournalList('date', this.value);
        });
    }
    
    const prevDateBtn = document.getElementById('prevDateBtn');
    const nextDateBtn = document.getElementById('nextDateBtn');
    
    if (prevDateBtn && datePicker) {
        prevDateBtn.addEventListener('click', function() {
            const date = new Date(datePicker.value);
            date.setDate(date.getDate() - 1);
            datePicker.value = date.toISOString().split('T')[0];
            loadJournalList('date', datePicker.value);
        });
    }
    
    if (nextDateBtn && datePicker) {
        nextDateBtn.addEventListener('click', function() {
            const date = new Date(datePicker.value);
            date.setDate(date.getDate() + 1);
            datePicker.value = date.toISOString().split('T')[0];
            loadJournalList('date', datePicker.value);
        });
    }
    
    // Create button
    const createBtn = document.getElementById('createBtn');
    if (createBtn) {
        createBtn.addEventListener('click', function() {
            window.location.href = '/entry/new';
        });
    }
    
    // Settings button
    const settingsBtn = document.getElementById('settingsBtn');
    if (settingsBtn) {
        settingsBtn.addEventListener('click', function() {
            window.location.href = '/settings';
        });
    }
    
    // Batch export button (T091)
    const exportBtn = document.getElementById('exportBtn');
    const batchExportControls = document.getElementById('batchExportControls');
    const selectAllBtn = document.getElementById('selectAllBtn');
    const deselectAllBtn = document.getElementById('deselectAllBtn');
    const batchExportBtn = document.getElementById('batchExportBtn');
    
    let batchModeEnabled = false;
    
    if (exportBtn && batchExportControls) {
        exportBtn.addEventListener('click', function() {
            batchModeEnabled = !batchModeEnabled;
            batchExportControls.style.display = batchModeEnabled ? 'block' : 'none';
            
            // Reload list to show/hide checkboxes
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
        });
    }
    
    // Select all entries
    if (selectAllBtn) {
        selectAllBtn.addEventListener('click', function() {
            document.querySelectorAll('.entry-checkbox').forEach(cb => {
                cb.checked = true;
            });
        });
    }
    
    // Deselect all entries
    if (deselectAllBtn) {
        deselectAllBtn.addEventListener('click', function() {
            document.querySelectorAll('.entry-checkbox').forEach(cb => {
                cb.checked = false;
            });
        });
    }
    
    // Batch export selected entries
    if (batchExportBtn) {
        batchExportBtn.addEventListener('click', async function() {
            const selectedCheckboxes = document.querySelectorAll('.entry-checkbox:checked');
            const selectedIds = Array.from(selectedCheckboxes).map(cb => parseInt(cb.dataset.entryId));
            
            if (selectedIds.length === 0) {
                alert('请至少选择一条日志');
                return;
            }
            
            batchExportBtn.disabled = true;
            batchExportBtn.textContent = '导出中...';
            
            try {
                const result = await ExportAPI.batchExport(selectedIds);
                if (result.shortcuts_url) {
                    ExportAPI.openShortcuts(result.shortcuts_url);
                    setTimeout(() => {
                        alert(`成功导出 ${selectedIds.length} 条日志！如果 Shortcuts 应用未打开，请检查是否已安装 Shortcuts 应用。`);
                    }, 500);
                } else {
                    alert(`成功导出 ${selectedIds.length} 条日志`);
                }
            } catch (error) {
                let errorMessage = '批量导出失败: ' + error.message;
                if (error.message.includes('Shortcuts') || error.message.includes('Notes')) {
                    errorMessage += '\n\n请确保：\n1. 已安装 Shortcuts 应用\n2. 已创建 "AddToNotes" Shortcut';
                }
                alert(errorMessage);
            } finally {
                batchExportBtn.disabled = false;
                batchExportBtn.textContent = '导出选中';
            }
        });
    }
    
    // Load initial data
    if (document.getElementById('journalListAll')) {
        loadJournalList('all');
    }
});

// Load journal list
async function loadJournalList(listId, date = null) {
    const listElement = document.getElementById(`journalList${listId.charAt(0).toUpperCase() + listId.slice(1)}`);
    if (!listElement) return;
    
    try {
        listElement.innerHTML = '<div class="empty-state">加载中...</div>';
        const entries = await JournalAPI.listEntries(date);
        
        if (!entries || entries.length === 0) {
            // Show appropriate empty state message based on context
            let emptyMessage = '<div class="empty-state"><div class="empty-state-icon">📝</div><div class="empty-state-text">暂无日志</div>';
            
            if (listId === 'date' && date) {
                const formattedDate = Utils.formatDate(date);
                emptyMessage += `<div class="empty-state-date">${formattedDate} 没有日志条目</div>`;
            } else if (listId === 'today') {
                emptyMessage += '<div class="empty-state-date">今天还没有创建日志</div>';
            }
            
            emptyMessage += '</div>';
            listElement.innerHTML = emptyMessage;
            return;
        }
        
        // Check if batch export mode is enabled
        const batchExportControls = document.getElementById('batchExportControls');
        const isBatchMode = batchExportControls && batchExportControls.style.display !== 'none';
        
        listElement.innerHTML = entries.map(entry => {
            // Sync status indicator (T079)
            let syncStatusIcon = '';
            if (entry.sync_status === 'synced') {
                syncStatusIcon = '<span class="sync-status synced" title="已同步">✓</span>';
            } else if (entry.sync_status === 'sync_pending') {
                syncStatusIcon = '<span class="sync-status pending" title="待同步">⏳</span>';
            } else if (entry.sync_status === 'sync_error') {
                syncStatusIcon = '<span class="sync-status error" title="同步失败">⚠</span>';
            }
            
            // Batch export checkbox (T091)
            const checkbox = isBatchMode 
                ? `<input type="checkbox" class="entry-checkbox" data-entry-id="${entry.id}" onclick="event.stopPropagation();">`
                : '';
            
            return `
            <div class="journal-entry ${isBatchMode ? 'batch-mode' : ''}" onclick="${isBatchMode ? '' : `window.location.href='/entry/${entry.id}'`}">
                ${checkbox}
                <div class="journal-entry-header">
                    <div class="journal-entry-title">${entry.title || '无标题'}</div>
                    ${syncStatusIcon}
                </div>
                <div class="journal-entry-date">${Utils.formatDate(entry.date)}</div>
                <div class="journal-entry-content">${Utils.truncateText(entry.content || '')}</div>
            </div>
        `;
        }).join('');
    } catch (error) {
        console.error('Error loading journal list:', error);
        listElement.innerHTML = `<div class="empty-state"><div class="empty-state-icon">⚠️</div><div class="empty-state-text">加载失败: ${error.message}</div></div>`;
    }
}

