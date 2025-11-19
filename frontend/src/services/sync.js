/**
 * Sync service for calendar synchronization and export operations.
 */
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

/**
 * Make an API request with error handling.
 */
async function request(url, options = {}) {
  const response = await fetch(`${API_BASE_URL}${url}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    credentials: 'include',
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Request failed' }))
    throw new Error(error.error || `HTTP error! status: ${response.status}`)
  }

  if (response.status === 204) {
    return null
  }

  return response.json()
}

/**
 * Sync API client.
 */
export const syncAPI = {
  /**
   * Sync a single journal entry to calendar.
   * @param {number} entryId - Entry ID
   * @returns {Promise<Object>} Sync result
   */
  async syncEntry(entryId) {
    return request(`/journal/entries/${entryId}/sync`, {
      method: 'POST',
    })
  },

  /**
   * Sync all pending entries.
   * @returns {Promise<Object>} Sync statistics
   */
  async syncAll() {
    return request('/calendar/sync', {
      method: 'POST',
    })
  },

  /**
   * List calendar events.
   * @returns {Promise<Object>} Calendar events
   */
  async listCalendarEvents() {
    return request('/calendar/events')
  },

  /**
   * Export single entry to Notes via Shortcuts.
   * @param {number} entryId - Entry ID
   * @returns {Promise<string>} Shortcuts URL
   */
  async exportEntry(entryId) {
    const response = await request(`/journal/entries/${entryId}/export`, {
      method: 'POST',
    })
    return response.shortcuts_url
  },

  /**
   * Export multiple entries to Notes via Shortcuts.
   * @param {Array<number>} entryIds - Entry IDs
   * @returns {Promise<string>} Shortcuts URL
   */
  async exportEntries(entryIds) {
    const response = await request('/journal/entries/batch-export', {
      method: 'POST',
      body: JSON.stringify({ entry_ids: entryIds }),
    })
    return response.shortcuts_url
  },
}





