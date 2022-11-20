/**
 * Main content of the web page.
 *
 * Will always be displayed by `index.tsx` main script.
 */

import * as React from "react"
import SchoolsPage from "./pages/Schools"
import {Routes, Route} from "react-router-dom"

/**
 * Builds the app-level element
 * @returns Element containing the main content
 */
export default class App extends React.Component<{}, {}> {
  render(): JSX.Element {
    return (
      <Routes>
        <Route path="/">
          <Route path="school" element={<SchoolsPage />} />
        </Route>
      </Routes>
    )
  }
}
