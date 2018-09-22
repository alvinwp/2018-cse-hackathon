import React, { Component } from 'react';

import { withStyles } from '@material-ui/core/styles';


import Header from './components/Header';
import Search from './components/Search';
import ReactSelect from './components/Search';

const styles = {
  root: {
    display: 'flex',
    height: '100vh',
    // width: '100vw',
    flexDirection: 'column',
    // justifyContent: 'center',
    alignItems: 'center',
    minHeight: '400px',
  },
  body: {
    display: 'flex',
    marginTop: '70px',
    minWidth: '600px',
    padding: '60 20 0 20',
    width: '85%',
  }
}

class App extends Component {
  state = {

  }

  render() {

    const { classes } = this.props;
    
    return (
      <div className={classes.root}>
        <Header/>
        <section className={classes.body}>
          <Search/>
        </section>
      </div>
    );
  }
}

export default withStyles(styles)(App);
