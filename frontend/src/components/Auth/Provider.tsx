/**
 * Authentication provider
 */

import * as React from "react"
import {api} from "../../core/api"
import {saveLocalToken, removeLocalToken} from "../../core/storage"

/**
 * AuthContext type
 */
interface AuthContextType {
  loggedIn: boolean
  login: (username: string, password: string) => Promise<boolean>
  logout: () => Promise<void>
}

/**
 * Actual auth context
 */
export const context = React.createContext<AuthContextType | null>(null)

/**
 * Tool to get auth context using `useContext`
 * @returns Auth context
 */
export function useAuth(): AuthContextType | null {
  return React.useContext(context)
}

interface Props {
  children: JSX.Element | JSX.Element[]
}

/**
 * AuthProvider element, provides AuthContext
 * @param props children elements
 * @returns Element
 */
export default function AuthProvider(props: Props): JSX.Element {
  const [loggedIn, setLoggedIn] = React.useState<boolean>(false)

  /**
   * Login function
   * @param username email identifying the user
   * @param password user's password
   * @returns boolean whether the authentication succeed
   */
  const login = async (
    username: string,
    password: string
  ): Promise<boolean> => {
    const token = await api.logInGetToken(username, password)
    if (token === undefined) {
      return false
    }
    setLoggedIn(true)
    saveLocalToken(token)
    return true
  }

  /**
   * Logout
   */
  const logout = async (): Promise<void> => {
    setLoggedIn(false)
    removeLocalToken()
  }

  const value = {loggedIn, login, logout}

  return <context.Provider value={value}>{props.children}</context.Provider>
}
