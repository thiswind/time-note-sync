/**
 * API client service for backend communication.
 */
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

/**
 * Make an API request with error handling.
 */
async function request(url, options = {}) {
  const fullUrl = `${API_BASE_URL}${url}`
  const response = await fetch(fullUrl, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    credentials: 'include', // Include cookies for session authentication
  })

  if (!response.ok) {
    // Handle 401 Unauthorized - redirect to login
    if (response.status === 401) {
      // Don't redirect if we're already on login page
      if (!url.includes('/auth/login') && !url.includes('/auth/status')) {
        window.location.href = '/login'
      }
    }
    const error = await response.json().catch(() => ({ error: 'Request failed' }))
    throw new Error(error.error || `HTTP error! status: ${response.status}`)
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return null
  }

  return response.json()
}

/**
 * Journal API client.
 */
export const journalAPI = {
  /**
   * List journal entries.
   * @param {Object} params - Query parameters (date, limit, offset)
   * @returns {Promise<Object>} Response with entries and total count
   */
  async listEntries(params = {}) {
    const queryParams = new URLSearchParams()
    if (params.date) queryParams.append('date', params.date)
    if (params.limit) queryParams.append('limit', params.limit)
    if (params.offset) queryParams.append('offset', params.offset)

    const queryString = queryParams.toString()
    const url = `/journal/entries${queryString ? `?${queryString}` : ''}`
    return request(url)
  },

  /**
   * Get a specific journal entry.
   * @param {number} entryId - Entry ID
   * @returns {Promise<Object>} Journal entry object
   */
  async getEntry(entryId) {
    return request(`/journal/entries/${entryId}`)
  },

  /**
   * Create a new journal entry.
   * @param {Object} entry - Entry data (title, content, date)
   * @returns {Promise<Object>} Created journal entry
   */
  async createEntry(entry) {
    return request('/journal/entries', {
      method: 'POST',
      body: JSON.stringify(entry),
    })
  },

  /**
   * Update a journal entry.
   * @param {number} entryId - Entry ID
   * @param {Object} entry - Updated entry data
   * @returns {Promise<Object>} Updated journal entry
   */
  async updateEntry(entryId, entry) {
    return request(`/journal/entries/${entryId}`, {
      method: 'PUT',
      body: JSON.stringify(entry),
    })
  },

  /**
   * Delete a journal entry.
   * @param {number} entryId - Entry ID
   * @returns {Promise<void>}
   */
  async deleteEntry(entryId) {
    return request(`/journal/entries/${entryId}`, {
      method: 'DELETE',
    })
  },
}

