/**
 * Entrypoint of the frontend.
 *
 * Setup the web page.
 */

import React from "react"
import {createRoot} from "react-dom/client"
import {
  createTheme,
  StyledEngineProvider,
  ThemeProvider,
} from "@mui/material/styles"
import {CssBaseline} from "@mui/material"
import "./index.css"
import App from "./App"

const rootElement = document.getElementById("root")
// eslint-disable-next-line @typescript-eslint/no-non-null-assertion
const root = createRoot(rootElement!)

// All `Portal`-related components need to have the the main app wrapper element as a container
// so that the are in the subtree under the element used in the `important` option of the Tailwind's config.
const theme = createTheme({
  components: {
    MuiPopover: {
      defaultProps: {
        container: rootElement,
      },
    },
    MuiPopper: {
      defaultProps: {
        container: rootElement,
      },
    },
  },
  palette: {
    primary: {
      main: "#2b4079",
      light: "#5b6aa8",
      dark: "#00194b",
      contrastText: "#fff",
    },
    secondary: {
      main: "#d23040",
      light: "#ff666b",
      dark: "#9a001a",
      contrastText: "#fff",
    },
  },
})

root.render(
  <React.StrictMode>
    <StyledEngineProvider injectFirst>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <App />
      </ThemeProvider>
    </StyledEngineProvider>
  </React.StrictMode>
)
