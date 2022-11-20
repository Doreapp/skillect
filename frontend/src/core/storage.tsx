/**
 * Local storage
 */

const TOKEN_KEY = "token"

/**
 * Search for token in local storage
 * @returns Token if saved or null
 */
export function getLocalToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

/**
 * Save the token in local storage
 * @param token token value
 */
export function saveLocalToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token)
}

/**
 * Remove the token saved in local storage
 */
export function removeLocalToken(): void {
  localStorage.removeItem(TOKEN_KEY)
}
