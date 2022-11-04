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
import {ISchool} from "./models/School"
import {api} from "./core/api"

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

interface AppState {
  schools: ISchool[]
  fetching: boolean
}

/**
 * Builds the app-level element
 * @returns Element containing the main content
 */
export default class App extends React.Component<{}, AppState> {
  state: AppState = {
    schools: [],
    fetching: true,
  }

  componentDidMount(): void {
    console.log("Fetching schools...")
    api
      .getSchools()
      .then((schools) => {
        this.setState({schools, fetching: false})
      })
      .catch((error) => {
        console.warn("Error while fetching schools:", error)
        this.setState({...this.state, fetching: false})
      })
  }

  render(): JSX.Element {
    return (
      <Container className="p-0 h-screen flex flex-col" maxWidth={false}>
        <AppBar title="Schools" />
        <Container className="p-0 flex-1">
          <SchoolsPage
            schools={this.state.schools}
            loading={this.state.fetching}
          />
        </Container>
        <Copyright />
      </Container>
    )
  }
}
