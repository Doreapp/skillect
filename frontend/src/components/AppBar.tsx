/**
 * App Bar
 */

import {AppBar as MuiAppBar, Toolbar, Typography} from "@mui/material"
import * as React from "react"
import {ReactComponent as Logo} from "./logo-white.svg"

export interface AppBarProps {
  title: string
}

export default function AppBar(props: AppBarProps): JSX.Element {
  return (
    <MuiAppBar position="relative">
      <Toolbar>
        <Logo className="w-16 h-16 mr-10" />
        <Typography variant="h6" component="div">
          {props.title}
        </Typography>
      </Toolbar>
    </MuiAppBar>
  )
}
