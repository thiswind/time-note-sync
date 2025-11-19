/**
 * Authentication service for login/logout.
 */
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

/**
 * Login user.
 */
export async function login(username, password) {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify({ username, password }),
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ error: 'Login failed' }))
    throw new Error(error.error || 'Login failed')
  }

  return response.json()
}

/**
 * Logout user.
 */
export async function logout() {
  const response = await fetch(`${API_BASE_URL}/auth/logout`, {
    method: 'POST',
    credentials: 'include',
  })

  if (!response.ok) {
    throw new Error('Logout failed')
  }

  return response.json()
}

/**
 * Check authentication status.
 */
export async function checkAuthStatus() {
  const response = await fetch(`${API_BASE_URL}/auth/status`, {
    credentials: 'include',
  })

  if (!response.ok) {
    return { authenticated: false }
  }

  return response.json()
}





