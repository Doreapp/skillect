/**
 * Main content of the web page.
 *
 * Will always be displayed by `index.tsx` main script.
 */

import * as React from "react"
import adminRouter from "./pages/Admin"
import HomePage from "./pages/Home"
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
          <Route index element={<HomePage />} />
          {adminRouter()}
        </Route>
      </Routes>
    )
  }
}
