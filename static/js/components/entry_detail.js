// Entry detail page functionality
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('entryForm');
    const saveBtn = document.getElementById('saveBtn');
    const deleteBtn = document.getElementById('deleteBtn');
    const exportBtn = document.getElementById('exportBtn');
    const titleInput = document.getElementById('title');
    const dateInput = document.getElementById('date');
    const contentInput = document.getElementById('content');
    
    const isNewEntry = entryId === null || entryId === undefined;
    
    // Load entry data if editing
    if (!isNewEntry && entryId) {
        loadEntry(entryId);
    } else {
        // Set default date for new entry
        dateInput.value = new Date().toISOString().split('T')[0];
    }
    
    // Save button handler
    if (saveBtn) {
        saveBtn.addEventListener('click', async function() {
            await saveEntry();
        });
    }
    
    // Delete button handler
    if (deleteBtn) {
        deleteBtn.addEventListener('click', async function() {
            if (confirm('确定要删除这条日志吗？')) {
                await deleteEntry();
            }
        });
    }
    
    // Export button handler
    if (exportBtn) {
        exportBtn.addEventListener('click', async function() {
            await exportEntry();
        });
    }
    
    // Form submission handler
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            await saveEntry();
        });
    }
    
    // Load entry data
    async function loadEntry(id) {
        try {
            const entry = await JournalAPI.getEntry(id);
            titleInput.value = entry.title || '';
            dateInput.value = Utils.formatDateInput(entry.date);
            contentInput.value = entry.content || '';
        } catch (error) {
            alert('加载日志失败: ' + error.message);
            window.location.href = '/';
        }
    }
    
    // Save entry
    async function saveEntry() {
        const title = titleInput.value.trim();
        const date = dateInput.value;
        const content = contentInput.value.trim();
        
        if (!title && !content) {
            alert('请输入标题或内容');
            return;
        }
        
        if (!date) {
            alert('请选择日期');
            return;
        }
        
        saveBtn.disabled = true;
        saveBtn.textContent = '保存中...';
        
        try {
            const entryData = {
                title: title || '',
                content: content || '',
                date: date
            };
            
            if (isNewEntry) {
                const result = await JournalAPI.createEntry(entryData);
                alert('日志创建成功');
                window.location.href = `/entry/${result.id}`;
            } else {
                await JournalAPI.updateEntry(entryId, entryData);
                alert('日志更新成功');
                window.location.href = '/';
            }
        } catch (error) {
            alert('保存失败: ' + error.message);
        } finally {
            saveBtn.disabled = false;
            saveBtn.textContent = '保存';
        }
    }
    
    // Delete entry
    async function deleteEntry() {
        if (isNewEntry) {
            window.location.href = '/';
            return;
        }
        
        deleteBtn.disabled = true;
        deleteBtn.textContent = '删除中...';
        
        try {
            await JournalAPI.deleteEntry(entryId);
            alert('日志已删除');
            window.location.href = '/';
        } catch (error) {
            alert('删除失败: ' + error.message);
        } finally {
            deleteBtn.disabled = false;
            deleteBtn.textContent = '删除';
        }
    }
    
    // Export entry
    async function exportEntry() {
        if (isNewEntry) {
            alert('请先保存日志');
            return;
        }
        
        exportBtn.disabled = true;
        exportBtn.textContent = '导出中...';
        
        try {
            const result = await ExportAPI.exportEntry(entryId);
            if (result.shortcuts_url) {
                window.location.href = result.shortcuts_url;
            } else {
                alert('导出成功');
            }
        } catch (error) {
            alert('导出失败: ' + error.message);
        } finally {
            exportBtn.disabled = false;
            exportBtn.textContent = '↗';
        }
    }
});

