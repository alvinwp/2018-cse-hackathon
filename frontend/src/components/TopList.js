import React from 'react'
import { withStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemText from '@material-ui/core/ListItemText';

class TopList extends React.Component {
  render() {
    const { items } = this.props;
    return(
      <List>
        <ListItem
          button
          selected={this.state.selectedIndex === 2}
          onClick={event => this.handleListItemClick(event, index)}
        >
          <ListItemText primary="Trash" />
        </ListItem>
      </List>
    )
  }
}

export default TopList