/**
 * Page containing schools
 */

import {
  List,
  ListItem,
  ListItemText,
  ListItemButton,
  ListItemIcon,
} from "@mui/material"
import * as React from "react"
import {ISchool} from "../models/School"
import AddIcon from "@mui/icons-material/Add"

export interface SchoolsPageProps {
  schools: ISchool[]
}

/**
 * Instantiate the "Add" button
 * @returns Element representing the "+ Add" button
 */
function AddButton(): JSX.Element {
  return (
    <ListItemButton
      onClick={(event) => console.log(event, 0)}
      alignItems="center">
      <ListItemIcon>
        <AddIcon color="primary" />
      </ListItemIcon>
      <ListItemText primary="Add a school" />
    </ListItemButton>
  )
}

export default function SchoolsPage(props: SchoolsPageProps): JSX.Element {
  const items = []
  let key = 0
  for (const school of props.schools) {
    items.push(
      <ListItem key={key++} className="p-0">
        <ListItemButton>
          <ListItemText primary={school.name} secondary={school.description} />
        </ListItemButton>
      </ListItem>
    )
  }

  return (
    <List>
      {items}
      {AddButton()}
    </List>
  )
}
