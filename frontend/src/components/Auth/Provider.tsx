/**
 * Authentication provider
 */

import * as React from "react"
import {api} from "../../core/api"
import {
  saveLocalToken,
  removeLocalToken,
  getLocalToken,
} from "../../core/storage"
import {IUser} from "../../models/User"

/**
 * AuthContext type
 */
interface AuthContextType {
  user?: IUser
  token?: string
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
  const [state, setState] = React.useState<{
    user?: IUser
    retrieving: boolean
    token?: string
  }>({retrieving: true})

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
    setState({...state, user, token})
    saveLocalToken(token)
    return true
  }

  /**
   * Logout
   */
  const logout = async (): Promise<void> => {
    setState({...state, user: undefined, token: undefined})
    removeLocalToken()
  }

  // Check token saved in local storage
  React.useEffect(() => {
    if (!state.retrieving) {
      return
    }
    const token = getLocalToken()
    if (token !== null) {
      api
        .getMe(token)
        .then((user) => {
          if (user === null || !user.is_active) {
            removeLocalToken()
            setState({user: undefined, token: undefined, retrieving: false})
          } else {
            setState({user, token, retrieving: false})
          }
        })
        .catch((_) => {
          removeLocalToken()
          setState({...state, retrieving: false})
        })
    } else {
      setState({...state, retrieving: false})
    }
  })

  const value = {user: state.user, token: state.token, login, logout}

  return <context.Provider value={value}>{props.children}</context.Provider>
}
