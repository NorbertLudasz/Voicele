import React, { useState } from 'react';
import Button from "@mui/material/Button";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import { FormHelperText } from '@mui/material';
import TextField from "@mui/material/TextField";
import FormControl from "@mui/material/FormControl";
import Radio from "@mui/material/Radio";
import RadioGroup from "@mui/material/RadioGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import { Link, useNavigate } from "react-router-dom";
import { format, subDays } from 'date-fns';

const CreateGamePage = () => {
  const defaultGuessHintNum = 3;
  const [hintPerms, setHintPerms] = useState(true);
  const [guessHintNum, setGuessHintNum] = useState(defaultGuessHintNum);
  const [selectedDate, setSelectedDate] = useState(format(new Date(), 'yyyy-MM-dd'));
  const navigate = useNavigate();

  const getPastSevenDates = () => {
    const today = new Date();
    return Array.from({ length: 7 }, (_, i) => {
      const date = subDays(today, i);
      return format(date, 'yyyy-MM-dd');
    });
  };

  const handleGuessHintNumChange = (e) => {
    setGuessHintNum(e.target.value);
    /*console.log("Guess Hint Number changed:", e.target.value);*/
  }

  const handleHintPermsChange = (e) => {
    setHintPerms(e.target.value === 'true');
    /*console.log("Hint Permissions changed:", e.target.value === 'true');*/
  }

  const handleDateChange = (e) => {
    setSelectedDate(e.target.value);
    /*console.log("Selected Date changed:", e.target.value);*/
  }

  const handleCreateGamePressed = () => {
    /*console.log({ hintPerms, guessHintNum, selectedDate });*/

    if (guessHintNum == null || hintPerms == null) {
      console.error("Missing required fields");
      return;
    }

    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const authToken = localStorage.getItem('authToken');

    /*console.log("CSRF Token:", csrfToken);
    console.log("Auth Token:", authToken);
    */
    const requestOptions = {
      method: 'POST',
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
        "Authorization": `Token ${authToken}`
      },
      body: JSON.stringify({
        guessHintNum: guessHintNum,
        hintPerms: hintPerms,
        seed_date: selectedDate
      })
    };

    /*console.log("Request Options Body:", requestOptions.body);
    */
    fetch('/api/create-game/', requestOptions)
      .then(response => response.json())
      .then(data => {
        /*console.log("Response data:", data);*/
        if (data.error) {
          alert(data.error);
          console.error("Error from server:", data.error);
        } else {
          const gameId = data.id;
          /*console.log("Created game ID:", gameId);*/
          navigate(`/play/${gameId}`);
        }
      })
      .catch(error => console.log('Error:', error));
  }

  return (
    <Grid container spacing={1}>
      <Grid item xs={12} align="center">
        <Typography component='h4' variant='h4'>
          Start Game
        </Typography>
      </Grid>
      <Grid item xs={12} align="center">
        <FormControl component="fieldset">
          <FormHelperText>
            <div align='center'>
              To show hints after 3 wrong guesses?
            </div>
          </FormHelperText>
          <RadioGroup row defaultValue='true' onChange={handleHintPermsChange}>
            <FormControlLabel value='true' 
              control={<Radio color="primary" />}
              label="Show Hints"
              labelPlacement='bottom' />
            <FormControlLabel value='false' 
              control={<Radio color="secondary" />}
              label="Hints OFF"
              labelPlacement='bottom' />
          </RadioGroup>
        </FormControl>
      </Grid>
      <Grid item xs={12} align="center">
        <FormControl>
          <TextField
            required={true}
            type="number"
            onChange={handleGuessHintNumChange}
            defaultValue={defaultGuessHintNum}
            inputProps={{
              min: 1,
              style: { textAlign: "center" }
            }}
          />
          <FormHelperText>
            <div align='center'>
              Guesses required to show hints
            </div>
          </FormHelperText>
        </FormControl>
      </Grid>
      <Grid item xs={12} align="center">
        <FormControl>
          <TextField
            select
            label="Select Date"
            value={selectedDate}
            onChange={handleDateChange}
            SelectProps={{
              native: true,
            }}
            variant="outlined"
          >
            {getPastSevenDates().map(date => (
              <option key={date} value={date}>
                {date}
              </option>
            ))}
          </TextField>
          <FormHelperText>
            <div align='center'>
              Select a date from the past 7 days
            </div>
          </FormHelperText>
        </FormControl>
      </Grid>
      <Grid item xs={12} align="center">
        <Button color="secondary" variant="contained" onClick={handleCreateGamePressed}>
          Play
        </Button>
      </Grid>
      <Grid item xs={12} align="center">
        <Button color="primary" variant="contained" to="/" component={Link}>
          Back
        </Button>
      </Grid>
    </Grid>
  );
};

export default CreateGamePage;