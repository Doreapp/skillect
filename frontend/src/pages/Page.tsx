/**
 * Base page
 */

import {Container, Typography} from "@mui/material"
import AppBar from "../components/AppBar"
import * as React from "react"

/**
 * Basic page props
 */
export interface PageProps {
  title: string
  children?: JSX.Element | JSX.Element[]
}

/**
 * Basic page
 */
export default function Page(props: PageProps): JSX.Element {
  return (
    <Container className="p-0 h-screen flex flex-col" maxWidth={false}>
      <AppBar title={props.title} />
      <Container className="p-0 flex-1">{props.children}</Container>
      <Typography variant="body2" color="text.secondary" align="center">
        {"Copyright © "}
        Antoine Mandin {new Date().getFullYear()}
        {"."}
      </Typography>
    </Container>
  )
}
