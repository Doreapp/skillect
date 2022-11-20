/**
 * Base admin page
 */

import {Container, Typography, Link} from "@mui/material"
import AppBar from "../../components/AppBar"
import RequireAuth from "../../components/Auth/RequireAuth"
import * as React from "react"

/**
 * Basic page props
 */
export interface PageProps {
  title: string
  requireLogin?: boolean
  children?: JSX.Element | JSX.Element[]
}

function Copyright(): JSX.Element {
  return (
    <Typography
      variant="body2"
      color="text.secondary"
      align="center"
      className="mt-1">
      {"Copyright © "}
      Antoine Mandin {new Date().getFullYear()}
      {"."}
    </Typography>
  )
}

function BottomLinks(): JSX.Element {
  return (
    <Container className="flex justify-around w-1/2 mt-1">
      <Link variant="body2" href="https://github.com/Doreapp/skillect/">
        Source code
      </Link>
      <Link variant="body2" href="/docs">
        Swagger
      </Link>
      <Link variant="body2" href="/redoc">
        ReDoc
      </Link>
    </Container>
  )
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
      <AppBar title={title} showUser={true} />
      <Container className="p-0 flex-1">{children}</Container>
      <BottomLinks />
      <Copyright />
    </Container>
  )

  if (requireLogin) {
    return <RequireAuth>{mainContent}</RequireAuth>
  } else {
    return mainContent
  }
}
