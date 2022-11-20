/**
 * Component requiring authentication.
 * If not authenticate, redirect to /login page.
 * When redirecting, save the routing in cache.
 */

import {useLocation, Navigate} from "react-router-dom"
import {useAuth} from "./Provider"
import * as React from "react"

interface Props {
  children: JSX.Element
}

export default function RequireAuth(props: Props): JSX.Element {
  const auth = useAuth()
  const location = useLocation()

  if (auth == null || !auth.loggedIn) {
    // Redirect them to the /login page, but save the current location they were
    // trying to go to when they were redirected. This allows us to send them
    // along to that page after they login, which is a nicer user experience
    // than dropping them off on the home page.
    return <Navigate to="/login" state={{from: location}} replace />
  }

  return props.children
}
