/**
 * Base page
 */

import {Container, Typography} from "@mui/material"
import AppBar from "../components/AppBar"
import RequireAuth from "../components/Auth/RequireAuth"
import * as React from "react"

/**
 * Basic page props
 */
export interface PageProps {
  title: string
  requireLogin?: boolean
  children?: JSX.Element | JSX.Element[]
}

/**
 * Basic page
 */
export default function Page({
  title,
  children,
  requireLogin = false,
}: PageProps): JSX.Element {
  const mainContent = (
    <Container className="p-0 h-screen flex flex-col" maxWidth={false}>
      <AppBar title={title} />
      <Container className="p-0 flex-1">{children}</Container>
      <Typography variant="body2" color="text.secondary" align="center">
        {"Copyright © "}
        Antoine Mandin {new Date().getFullYear()}
        {"."}
      </Typography>
    </Container>
  )

  if (requireLogin) {
    return <RequireAuth>{mainContent}</RequireAuth>
  } else {
    return mainContent
  }
}
