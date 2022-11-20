/**
 * Login page
 */

import {
  Box,
  TextField,
  FormControlLabel,
  Checkbox,
  Button,
  Link,
  TextFieldProps,
  Alert,
  Container,
} from "@mui/material"
import * as React from "react"
import Page from "./Page"
import {useAuth} from "../components/Auth/Provider"
import {useLocation, useNavigate} from "react-router-dom"

function field(
  name: string,
  label: string,
  props: TextFieldProps
): JSX.Element {
  return (
    <TextField
      margin="normal"
      required
      fullWidth
      id={name}
      label={label}
      name={name}
      {...props}
    />
  )
}

interface State {
  error?: string
  warning?: string
}

/**
 * Login page
 * @returns
 */
export default function LoginPage(): JSX.Element {
  const [state, setState] = React.useState<State>({
    error: undefined,
    warning: undefined,
  })

  const authContext = useAuth()
  const location = useLocation()
  const navigate = useNavigate()
  const from = location.state?.from?.pathname ?? "/"

  // Submit handler, request /login endpoint
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>): void => {
    event.preventDefault()
    if (authContext == null) {
      setState({...state, error: "Internal error (context null)."})
      return
    }

    const data = new FormData(event.currentTarget)
    const email = data.get("email")
    const password = data.get("password")

    if (email == null || typeof email !== "string") {
      setState({...state, error: "Email field is required."})
      return
    }
    if (password == null || typeof password !== "string") {
      setState({...state, error: "Password field is required."})
      return
    }

    authContext
      .login(email, password)
      .then((success) => {
        if (success) {
          navigate(from, {replace: true})
        } else {
          setState({...state, error: "Signin failed."})
        }
      })
      .catch((error) => {
        console.warn("Unable to login", error)
        setState({...state, error: "Signin failed."})
      })
  }

  // Alert element
  let errorAlert
  if (state.error != null) {
    errorAlert = <Alert severity="error">{state.error}</Alert>
  }

  return (
    <Page title="Login">
      <Container className="flex justify-around">
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
          className="max-w-md">
          <h3>Sign in</h3>
          <Box component="form" onSubmit={handleSubmit} noValidate sx={{mt: 1}}>
            {field("email", "Email Address", {
              autoComplete: "email",
              autoFocus: true,
            })}
            {field("password", "Password", {
              autoComplete: "current-password",
            })}
            <FormControlLabel
              control={<Checkbox value="remember" color="primary" />}
              label="Remember me"
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{mt: 3, mb: 2}}>
              Sign In
            </Button>
            <Link href="#" variant="body2">
              Forgot password?
            </Link>
            {errorAlert}
          </Box>
        </Box>
      </Container>
    </Page>
  )
}
