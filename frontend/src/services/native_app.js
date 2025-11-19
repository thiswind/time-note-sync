/**
 * Native app service for opening iPhone native apps via URL schemes.
 */

/**
 * Open a URL scheme (for native apps).
 * @param {string} url - URL scheme to open
 * @returns {Promise<boolean>} True if opened successfully, false otherwise
 */
export async function openNativeApp(url) {
  try {
    // Try to open the URL scheme
    window.location.href = url

    // Set a timeout to detect if the app didn't open
    return new Promise((resolve) => {
      const timeout = setTimeout(() => {
        // If we're still here after 2 seconds, the app probably didn't open
        resolve(false)
      }, 2000)

      // If the page loses focus, the app likely opened
      const handleBlur = () => {
        clearTimeout(timeout)
        window.removeEventListener('blur', handleBlur)
        resolve(true)
      }

      window.addEventListener('blur', handleBlur)
    })
  } catch (error) {
    console.error('Error opening native app:', error)
    return false
  }
}

/**
 * Open Calendar app.
 * @param {string} date - Optional date in YYYY-MM-DD format
 * @returns {Promise<boolean>} True if opened successfully
 */
export async function openCalendar(date = null) {
  let url = 'calshow://'
  if (date) {
    const dateStr = date.replace(/-/g, '')
    url = `calshow://${dateStr}`
  }
  return openNativeApp(url)
}

/**
 * Open Notes app.
 * @returns {Promise<boolean>} True if opened successfully
 */
export async function openNotes() {
  return openNativeApp('mobilenotes://')
}





