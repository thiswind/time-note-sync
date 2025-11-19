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
            method: 'POST'
        });
        if (!response.ok) throw new Error('Sync failed');
        return response.json();
    }
};

// Export API functions
const ExportAPI = {
    async exportEntry(id) {
        const response = await fetch(`${API_BASE}/journal/entries/${id}/export`, {
            method: 'POST'
        });
        if (!response.ok) throw new Error('Export failed');
        return response.json();
    },

    async batchExport(ids) {
        const response = await fetch(`${API_BASE}/journal/entries/batch-export`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ entry_ids: ids })
        });
        if (!response.ok) throw new Error('Batch export failed');
        return response.json();
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
                if (datePicker && !datePicker.value) {
                    datePicker.value = new Date().toISOString().split('T')[0];
                }
                loadJournalList('date', datePicker.value);
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
            listElement.innerHTML = '<div class="empty-state"><div class="empty-state-icon">📝</div><div class="empty-state-text">暂无日志</div></div>';
            return;
        }
        
        listElement.innerHTML = entries.map(entry => `
            <div class="journal-entry" onclick="window.location.href='/entry/${entry.id}'">
                <div class="journal-entry-title">${entry.title || '无标题'}</div>
                <div class="journal-entry-date">${Utils.formatDate(entry.date)}</div>
                <div class="journal-entry-content">${Utils.truncateText(entry.content || '')}</div>
            </div>
        `).join('');
    } catch (error) {
        listElement.innerHTML = `<div class="empty-state">加载失败: ${error.message}</div>`;
    }
}

