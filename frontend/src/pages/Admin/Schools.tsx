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
  TextField,
  Box,
  Container,
  Alert,
} from "@mui/material"
import LoadingButton from "@mui/lab/LoadingButton"
import * as React from "react"
import {ISchool} from "../../models/School"
import {api} from "../../core/api"
import AddIcon from "@mui/icons-material/Add"
import Page from "./Page"
import {useParams, useNavigate} from "react-router-dom"
import {useAuth} from "../../components/Auth/Provider"

export interface SchoolsPageState {
  schools?: ISchool[]
  tried: boolean
}

export interface SchoolPageState {
  school?: ISchool
  tried: boolean
  success?: string
  error?: string
  submiting: boolean
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
  onClick: React.MouseEventHandler<HTMLDivElement> | undefined = undefined
): JSX.Element {
  return (
    <ListItem key={key} className="p-0">
      <ListItemButton onClick={onClick} disabled={onClick === undefined}>
        <ListItemText primary={primary} secondary={secondary} />
      </ListItemButton>
    </ListItem>
  )
}
export function SchoolsPage(): JSX.Element {
  const [state, setState] = React.useState<SchoolsPageState>({
    schools: undefined,
    tried: false,
  })
  const navigate = useNavigate()

  React.useEffect(() => {
    if (state.tried) {
      return
    }
    console.log("Fetching schools...")
    api
      .getSchools()
      .then((schools) => {
        setState({schools, tried: true})
      })
      .catch((error) => {
        console.warn("Error while fetching schools:", error)
        setState({schools: [], tried: true})
      })
  })

  const items = []
  if (state.schools === undefined) {
    // Only show a single squeleton element
    items.push(
      listItem(0, <Skeleton variant="text" />, <Skeleton variant="text" />)
    )
  } else {
    let key = 0
    for (const school of state.schools) {
      const onClick = (): void => {
        navigate(`${school.id}`, {replace: false})
      }
      items.push(listItem(key++, school.name, school.description, onClick))
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

/**
 * Page for a single school.
 * The id of the school shall be passed via a route param
 */
export function SchoolPage(): JSX.Element {
  const {id} = useParams()
  const [state, setState] = React.useState<SchoolPageState>({
    school: undefined,
    tried: false,
    success: undefined,
    error: undefined,
    submiting: false,
  })
  const authContext = useAuth()

  React.useEffect(() => {
    if (state.tried) {
      return
    }
    if (id === undefined || isNaN(parseInt(id))) {
      console.error("The id is undefined or NaN:", id)
      setState({
        ...state,
        error: "The URL looks weird...",
        school: undefined,
        tried: true,
      })
      return
    }
    console.log(`Fetching school with id ${id}...`)
    api
      .getSchool(id)
      .then((school) => {
        setState({...state, school, tried: true})
      })
      .catch((error) => {
        console.warn("Error while fetching school:", error)
        if (error.response.status === 404) {
          setState({
            ...state,
            error: "School not found",
            school: undefined,
            tried: true,
          })
        } else {
          setState({
            ...state,
            error: "Unexpected error.",
            school: undefined,
            tried: true,
          })
        }
      })
  })

  /**
   * Handler of the change submit
   * @param event
   * @returns
   */
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>): void => {
    event.preventDefault()
    if (id === undefined || isNaN(parseInt(id))) {
      console.error("Id is undefined or NaN:", id)
      setState({...state, error: "The URL looks weird..."})
      return
    }
    if (authContext?.token === undefined) {
      console.error("Unable to authenticate the used")
      setState({
        ...state,
        error: "[Internal error] You do not look authenticated",
      })
      return
    }
    const data = new FormData(event.currentTarget)
    const newSchool = {
      id: parseInt(id),
      name: data.get("name")?.toString() ?? "",
      description: data.get("description")?.toString() ?? "",
      link: data.get("link")?.toString() ?? "",
    }
    if (
      state.school?.name === newSchool.name &&
      state.school?.description === newSchool.description &&
      state.school?.link === newSchool.link
    ) {
      setState({...state, error: "There is not change to save."})
    } else {
      setState({
        ...state,
        error: undefined,
        submiting: true,
        success: undefined,
      })
      api
        .updateSchool(newSchool, authContext.token)
        .then((school) => {
          setState({
            ...state,
            school,
            submiting: false,
            error: undefined,
            success: "School updated",
          })
        })
        .catch((error) => {
          console.error("Error while pushing update", error)
          setState({...state, submiting: false, error: "Internal error"})
        })
    }
  }

  let errorAlert
  if (state.error !== undefined) {
    errorAlert = (
      <Alert className="w-full" severity="error">
        {state.error}
      </Alert>
    )
  }

  let successAlert
  if (state.success !== undefined) {
    successAlert = (
      <Alert className="w-full" severity="success">
        {state.success}
      </Alert>
    )
  }

  let schoolElement
  if (state.school !== undefined) {
    schoolElement = (
      <Box
        component="form"
        onSubmit={handleSubmit}
        className="w-full"
        noValidate>
        <TextField
          margin="normal"
          fullWidth
          id="name"
          label="Name"
          name="name"
          defaultValue={state.school.name}
        />
        <TextField
          margin="normal"
          multiline
          fullWidth
          id="description"
          label="Description"
          name="description"
          defaultValue={state.school.description}
        />
        <TextField
          margin="normal"
          fullWidth
          id="link"
          label="Link"
          name="link"
          defaultValue={state.school.link}
        />
        <LoadingButton
          type="submit"
          fullWidth
          loading={state.submiting}
          variant="contained"
          sx={{mt: 3, mb: 2}}>
          Save changes
        </LoadingButton>
      </Box>
    )
  }

  return (
    <Page title="School edition" requireLogin={true}>
      <Container className="flex justify-around">
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            mt: 1,
          }}
          className="max-w-md">
          {successAlert}
          {errorAlert}
          {schoolElement}
        </Box>
      </Container>
    </Page>
  )
}
