import { AppBar as MuiAppBar, Toolbar, Typography } from '@mui/material' ;
import * as React from 'react';

export interface AppBarProps {
   title: string
}

export default function AppBar(props: AppBarProps) {
  return (
    <MuiAppBar>
        <Toolbar>
            <Typography variant="h6" component="div">{props.title}</Typography>
        </Toolbar>
    </MuiAppBar>
  );
}
