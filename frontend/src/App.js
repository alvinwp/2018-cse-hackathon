import React, { Component } from 'react';

import { withStyles } from '@material-ui/core/styles';

import axios from 'axios'

import Header from './components/Header';
import Search from './components/Search';

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
    marginTop: '80px',
    minWidth: '600px',
    padding: '60 20 0 20',
    width: '85%',
  }
}

class App extends Component {
  state = {
    allBuildings : [],
  }
  componentDidMount() {
    // axios({
    //   method: 'get',
    //   url: `localhost:8000/rooms`,
    // }).then(response => {
    //   this.setState({rooms: response});
    // })
    console.log('mount');

    axios({
      method: 'get',
      url: `http://localhost:5000/buildings/mapping`,
    }).then(response => {
      console.log(response.data);
      this.setState({ allBuildings: response.data });
    });
  }


  render() {

    const { classes } = this.props;
    const { allBuildings } = this.state;
    
    return (
      <div className={classes.root}>
        <Header/>
        <section className={classes.body}>
          <Search allBuildings={allBuildings}/>
        </section>
      </div>
    );
  }
}

export default withStyles(styles)(App);
