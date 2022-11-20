/**
 * App Bar
 */

import {
  AppBar as MuiAppBar,
  IconButton,
  ListItemIcon,
  Menu,
  MenuItem,
  Toolbar,
  Typography,
} from "@mui/material"
import * as React from "react"
import {ReactComponent as Logo} from "./logo-white.svg"
import {useAuth} from "./Auth/Provider"
import AccountCircle from "@mui/icons-material/AccountCircle"
import Logout from "@mui/icons-material/Logout"
import {useNavigate} from "react-router-dom"

export interface AppBarProps {
  title: string
  showUser?: boolean
}

function userElement(): JSX.Element | undefined {
  const authContext = useAuth()
  if (authContext == null || authContext.user === undefined) {
    return
  }
  const navigate = useNavigate()
  let userText = `${authContext.user.email}`
  if (authContext.user.is_superuser) {
    userText += " (admin)"
  }
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null)

  const handleMenu = (event: React.MouseEvent<HTMLElement>): void => {
    setAnchorEl(event.currentTarget)
  }
  const handleClose = (): void => {
    setAnchorEl(null)
  }
  const handleLogout = (): void => {
    authContext
      .logout()
      .then(() => navigate("/"))
      .catch((error) => console.warn("Unexpected error on logout", error))
  }

  return (
    <div>
      <IconButton
        size="large"
        aria-label="Current user"
        aria-controls="menu-appbar"
        aria-haspopup="true"
        onClick={handleMenu}
        color="inherit">
        <AccountCircle />
      </IconButton>
      <Menu
        id="menu-appbar"
        anchorEl={anchorEl}
        keepMounted
        open={Boolean(anchorEl)}
        onClose={handleClose}>
        <MenuItem disabled={true} divider={true}>
          {userText}
        </MenuItem>
        <MenuItem onClick={handleLogout}>
          <ListItemIcon>
            <Logout fontSize="small" />
          </ListItemIcon>
          Logout
        </MenuItem>
      </Menu>
    </div>
  )
}

export default function AppBar({
  title,
  showUser = false,
}: AppBarProps): JSX.Element {
  return (
    <MuiAppBar position="relative">
      <Toolbar>
        <Logo className="w-16 h-16 mr-10" />
        <Typography variant="h6" component="div" className="grow">
          {title}
        </Typography>
        {userElement()}
      </Toolbar>
    </MuiAppBar>
  )
}
