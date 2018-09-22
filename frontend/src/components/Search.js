import React from 'react';
import PropTypes from 'prop-types';
import classNames from 'classnames';
import Select from 'react-select';
import { withStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import NoSsr from '@material-ui/core/NoSsr';
import TextField from '@material-ui/core/TextField';
import Paper from '@material-ui/core/Paper';
import Chip from '@material-ui/core/Chip';
import MenuItem from '@material-ui/core/MenuItem';
import CancelIcon from '@material-ui/icons/Cancel';
import { emphasize } from '@material-ui/core/styles/colorManipulator';


const suggestions = [
  { label: "Ainsworth : J17" },
  { label: "CSE : K17" }
].map(suggestion => ({
  value: suggestion.label.split(':')[1].trim(),
  label: suggestion.label,
}));

const styles = theme => ({
  root: {
    flexGrow: 1,
    height: 250,
  },
  input: {
    display: 'flex',
    padding: 0,
  },
  valueContainer: {
    display: 'flex',
    flexWrap: 'wrap',
    flex: 1,
    alignItems: 'center',
  },
  chip: {
    margin: `${theme.spacing.unit / 2}px ${theme.spacing.unit / 4}px`,
  },
  chipFocused: {
    backgroundColor: emphasize(
      theme.palette.type === 'light' ? theme.palette.grey[300] : theme.palette.grey[700],
      0.08,
    ),
  },
  placeholder: {
    position: 'absolute',
    left: 2,
    fontSize: 16,
  },
  paper: {
    position: 'absolute',
    zIndex: 1,
    marginTop: theme.spacing.unit,
    left: 0,
    right: 0,
  },
  buildingList: { 
    marginTop: '20px !important',
    minHeight: '100px',
  },
  roomList: {
    marginTop: '20px',
    minHeight:'100px',
  }
});

function inputComponent({ inputRef, ...props }) {
  return <div ref={inputRef} {...props} />;
}

function Control(props) {
  return (
    <TextField
      fullWidth
      InputProps={{
        inputComponent,
        inputProps: {
          className: props.selectProps.classes.input,
          inputRef: props.innerRef,
          children: props.children,
          ...props.innerProps,
        },
      }}
      {...props.selectProps.textFieldProps}
    />
  );
}

function Option(props) {
  return (
    <MenuItem
      buttonRef={props.innerRef}
      selected={props.isFocused}
      component="div"
      style={{
        fontWeight: props.isSelected ? 500 : 400,
      }}
      {...props.innerProps}
    >
      {props.children}
    </MenuItem>
  );
}

function Placeholder(props) {
  return (
    <Typography
      color="textSecondary"
      className={props.selectProps.classes.placeholder}
      {...props.innerProps}
    >
      {props.children}
    </Typography>
  );
}

function ValueContainer(props) {
  return <div className={props.selectProps.classes.valueContainer}>{props.children}</div>;
}

function MultiValue(props) {
  return (
    <Chip
      tabIndex={-1}
      label={props.children}
      className={classNames(props.selectProps.classes.chip, {
        [props.selectProps.classes.chipFocused]: props.isFocused,
      })}
      onDelete={props.removeProps.onClick}
      deleteIcon={<CancelIcon {...props.removeProps} />}
    />
  );
}

function Menu(props) {
  return (
    <Paper square className={props.selectProps.classes.paper} {...props.innerProps}>
      {props.children}
    </Paper>
  );
}

const components = {
  Control,
  Menu,
  MultiValue,
  Option,
  Placeholder,
  ValueContainer,
};

class Search extends React.Component {
  state = {
    buildings: null,
  };

  handleChange = name => value => {
    console.log(value);
    
    // TODO: Make POST request to retrieve rooms of selected buildings

    this.setState({
      buildings: value,
    });
  };

  render() {
    console.log(this.state.buildings);
    const { classes, theme } = this.props;

    const selectStyles = {
      input: base => ({
        ...base,
        color: theme.palette.text.primary,
        '& input': {
          font: 'inherit',
        },
      }),
    };

    return (
      <div className={classes.root}>
        <div></div>
        <NoSsr>
          <Select
            classes={classes}
            styles={selectStyles}
            textFieldProps={{
              label: 'Building Search',
              InputLabelProps: {
                shrink: true,
              },
            }}
            options={suggestions}
            components={components}
            value={this.state.multi}
            onChange={this.handleChange()}
            placeholder="Select buildings"
            isMulti
            />
        </NoSsr>
          
          <div className={classes.buildingList}>
            <Typography variant="title">
              Top Buildings
            </Typography>
          </div>

        <div>
          <NoSsr>
            <Select
              classes={classes}
              styles={selectStyles}
              textFieldProps={{
                label: 'Room Search',
                InputLabelProps: {
                  shrink: true,
                },
              }}
              options={suggestions}
              components={components}
              value={this.state.multi}
              onChange={this.handleChange()}
              placeholder="Select rooms"
              isMulti
              isDisabled={!Boolean(this.state.buildings)}
              /> 
          </NoSsr>
        </div>

        <div className={classes.roomList}>
          <Typography variant='title'>
            Free rooms in Search
          </Typography>
        </div>
      </div>
    );
  }
}

export default withStyles(styles, { withTheme: true })(Search);