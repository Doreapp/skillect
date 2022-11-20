/**
 * Authentication provider
 */

import * as React from "react"
import {api} from "../../core/api"
import {saveLocalToken, removeLocalToken} from "../../core/storage"
import {IUser} from "../../models/User"

/**
 * AuthContext type
 */
interface AuthContextType {
  user?: IUser
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
  const [user, setUser] = React.useState<IUser | undefined>(undefined)

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
    const user = await api.getMe(token)
    if (user === null) {
      return false
    }
    setUser(user)
    saveLocalToken(token)
    return true
  }

  /**
   * Logout
   */
  const logout = async (): Promise<void> => {
    setUser(undefined)
    removeLocalToken()
  }

  const value = {user, login, logout}

  return <context.Provider value={value}>{props.children}</context.Provider>
}
