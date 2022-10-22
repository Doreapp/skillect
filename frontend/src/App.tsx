import * as React from 'react'
import Container from '@mui/material/Container'
import Typography from '@mui/material/Typography'
import AppBar from './components/AppBar'
import Link from '@mui/material/Link'

function Copyright (): JSX.Element {
  return (
    <Typography variant="body2" color="text.secondary" align="center">
      {'Copyright © '}
      <Link color="inherit" href="https://mui.com/">
        Antoine Mandin
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  )
}

export default function App (): JSX.Element {
  return (
    <Container maxWidth="sm">
        <AppBar title="Schools" />
        <Copyright />
    </Container>
  )
}
