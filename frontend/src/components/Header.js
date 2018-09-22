import React from 'react';

import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar'
import Typography from "@material-ui/core/Typography";
import { withStyles } from '@material-ui/core/styles';

import RoomIcon from '@material-ui/icons/Room';
import DeleteIcon from '@material-ui/icons/Delete';


const styles = {
  root: {
    background: 'white',
  }
}


class Header extends React.Component { 
  render() {
    const { classes } = this.props;

    return(
      <AppBar className={classes.root}>
        <Toolbar>
          <Typography variant='title'> UNSW Room Mate </Typography>
        </Toolbar>
      </AppBar>
    )
  }
}

export default withStyles(styles)(Header);