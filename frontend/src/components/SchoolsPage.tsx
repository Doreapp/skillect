/**
 * Page containing schools
 */

import { Container, List, ListItem, ListItemText } from '@mui/material'
import * as React from 'react'
import School from '../models/School'

export interface SchoolsPageProps {
  schools: School[]
}

export default function SchoolsPage (props: SchoolsPageProps): JSX.Element {
  const items = []
  let key = 0
  for (const school of props.schools) {
    items.push(
        <Container maxWidth="sm">
        <ListItem key={key++}>
            <ListItemText
                primary={school.name}
                secondary={school.description} />
        </ListItem>
        </Container>
    )
  }

  return (
     <List>
         {items}
     </List>
  )
}
