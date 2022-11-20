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
import {ISchool} from "../../models/School"
import {api} from "../../core/api"
import AddIcon from "@mui/icons-material/Add"
import Page from "./Page"

export interface SchoolsPageState {
  schools: ISchool[]
  loading: boolean
  tried: boolean
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
export default function SchoolsPage(): JSX.Element {
  const [state, setState] = React.useState<SchoolsPageState>({
    schools: [],
    loading: true,
    tried: false,
  })

  React.useEffect(() => {
    if (state.tried) {
      return
    }
    console.log("Fetching schools...")
    api
      .getSchools()
      .then((schools) => {
        setState({schools, loading: false, tried: true})
      })
      .catch((error) => {
        console.warn("Error while fetching schools:", error)
        setState({...state, loading: false, tried: true})
      })
  })

  const items = []
  if (state.schools == null) {
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
    for (const school of state.schools) {
      items.push(listItem(key++, school.name, school.description))
    }
  }

  return (
    <Page title="Schools" requireLogin={true}>
      <List>
        {items}
        {AddButton()}
      </List>
    </Page>
  )
}
