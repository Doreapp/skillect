/**
 * Main content of the web page.
 *
 * Will always be displayed by `index.tsx` main script.
 */

import * as React from "react"
import SchoolsPage from "./pages/Schools"
import LoginPage from "./pages/Login"
import {Routes, Route} from "react-router-dom"
import AuthProvider from "./components/Auth/Provider"

/**
 * Builds the app-level element
 * @returns Element containing the main content
 */
export default class App extends React.Component<{}, {}> {
  render(): JSX.Element {
    return (
      <AuthProvider>
        <Routes>
          <Route path="/">
            <Route path="login" element={<LoginPage />} />
            <Route path="school" element={<SchoolsPage />} />
          </Route>
        </Routes>
      </AuthProvider>
    )
  }
}
