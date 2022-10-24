import * as React from 'react'
import Container from '@mui/material/Container'
import Typography from '@mui/material/Typography'
import AppBar from './components/AppBar'
import SchoolsPage from './components/SchoolsPage'
import School from './models/School'

function Copyright (): JSX.Element {
  return (
    <Typography variant="body2" color="text.secondary" align="center">
      {'Copyright © '}
        Antoine Mandin
        {' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  )
}

const mockSchools = [
  new School('INSA Lyon', "Ecole d'ingénieur", 'https://insa-lyon.fr'),
  new School('KTH', "Ecole d'ingénieur en Suède", 'https://kth.se')
]

export default function App (): JSX.Element {
  return (
    <Container className='p-0 h-screen flex flex-col' maxWidth={false}>
        <AppBar title="Schools"/>
        <Container className='p-0 flex-1'>
          <SchoolsPage schools={mockSchools}/>
        </Container>
        <Copyright />
    </Container>
  )
}
