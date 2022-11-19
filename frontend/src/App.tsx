/**
 * Main content of the web page.
 *
 * Will always be displayed by `index.tsx` main script.
 */

import * as React from "react"
import Container from "@mui/material/Container"
import Typography from "@mui/material/Typography"
import AppBar from "./components/AppBar"
import SchoolsPage from "./components/SchoolsPage"
import {Routes, Route} from "react-router-dom"

/**
 * Copyright element
 * @returns Element containing copyright information
 */
function Copyright(): JSX.Element {
  return (
    <Typography variant="body2" color="text.secondary" align="center">
      {"Copyright © "}
      Antoine Mandin {new Date().getFullYear()}
      {"."}
    </Typography>
  )
}

/**
 * Builds the app-level element
 * @returns Element containing the main content
 */
export default class App extends React.Component<{}, {}> {
  render(): JSX.Element {
    return (
      <Container className="p-0 h-screen flex flex-col" maxWidth={false}>
        <AppBar title="Schools" />
        <Routes>
          <Route path="/">
            <Route path="school" element={<SchoolsPage />} />
          </Route>
        </Routes>
        <Copyright />
      </Container>
    )
  }
}
