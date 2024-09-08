import React, { useEffect, useState } from 'react';
import { Grid, Typography, Paper, Button } from '@mui/material';
import { Link } from 'react-router-dom';

const PastGames = () => {
  const [pastGames, setPastGames] = useState([]);

  useEffect(() => {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    const authToken = localStorage.getItem('authToken');

    const requestOptions = {
      method: 'GET',
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
        "Authorization": `Token ${authToken}`
      }
    };

    fetch('/api/past-games/', requestOptions)
      .then(response => response.json())
      .then(data => {
        setPastGames(data);
        /*console.log(data);*/
      })
      .catch(error => console.log('Error: ', error));
  }, []);

  const getGameStatusText = (status) => {
    switch (status) {
      case 0:
        return "Defeat";
      case 1:
        return "Abandoned";
      case 2:
        return "Victory";
      default:
        return "Bad value for gameStatus";
    }
  };

  return (
    <div>
      <Typography variant="h4" gutterBottom align="center">
        Past Games
      </Typography>

      {pastGames.length === 0 ? (
        <Typography variant="body1" align="center">
          No past games available.
        </Typography>
      ) : (
        <Paper elevation={3} style={{ padding: '16px', marginTop: '16px' }}>
          <Grid container spacing={2} style={{ marginBottom: '8px' }}>
            <Grid item xs={6}>
              <Typography variant="h6" align="center">
                Game Date
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography variant="h6" align="center">
                Game Result
              </Typography>
            </Grid>
          </Grid>

          {pastGames.map(game => (
            <Grid container spacing={2} key={game.id} style={{ marginBottom: '8px' }}>
              <Grid item xs={6}>
                <Typography variant="body1" align="center">
                  {new Date(game.createdAt).toLocaleDateString()}
                </Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography variant="body1" align="center">
                  {getGameStatusText(game.gameStatus)}
                </Typography>
              </Grid>
            </Grid>
          ))}
        </Paper>
      )}
      <Grid item xs={12} align="center">
        <Button color="primary" variant="contained" component={Link} to="/">
          Back
        </Button>
      </Grid>
    </div>
  );
};

export default PastGames;