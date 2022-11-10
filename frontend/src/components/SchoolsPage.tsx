/**
 * Page containing schools
 */

import {
  List,
  ListItem,
  ListItemText,
  ListItemButton,
  ListItemIcon,
  Skeleton,
} from "@mui/material"
import * as React from "react"
import {ISchool} from "../models/School"
import AddIcon from "@mui/icons-material/Add"

export interface SchoolsPageProps {
  schools: ISchool[]
  loading: boolean
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

/**
 * Create and return a list item
 * @param key Key of the item
 * @param primary Primary text
 * @param secondary Secondary text
 * @param disabled Is it disabled. Default to false.
 * @returns ListItem element to put into a List element
 */
function listItem(
  key: number,
  primary: React.ReactNode,
  secondary: React.ReactNode,
  disabled: boolean = false
): JSX.Element {
  return (
    <ListItem key={key} className="p-0">
      <ListItemButton disabled={disabled}>
        <ListItemText primary={primary} secondary={secondary} />
      </ListItemButton>
    </ListItem>
  )
}

export default function SchoolsPage(props: SchoolsPageProps): JSX.Element {
  const items = []

  if (props.loading) {
    // Only show a single squeleton element
    items.push(
      listItem(
        0,
        <Skeleton variant="text" />,
        <Skeleton variant="text" />,
        true
      )
    )
  } else {
    let key = 0
    for (const school of props.schools) {
      items.push(listItem(key++, school.name, school.description))
    }
  }

  return (
    <List>
      {items}
      {AddButton()}
    </List>
  )
}
