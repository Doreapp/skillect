/**
 * Admin pages
 */

import * as React from "react"
import SchoolsPage from "./Schools"
import LoginPage from "./Login"
import HomePage from "./Home"
import {Route, Outlet} from "react-router-dom"
import AuthProvider from "../../components/Auth/Provider"

/**
 * Admin pages router
 */
export default function AdminRouter(): JSX.Element {
  const layout = (
    <AuthProvider>
      <Outlet />
    </AuthProvider>
  )
  return (
    <Route path="admin/" element={layout}>
      <Route index element={<HomePage />} />
      <Route path="login" element={<LoginPage />} />
      <Route path="school" element={<SchoolsPage />} />
    </Route>
  )
}
