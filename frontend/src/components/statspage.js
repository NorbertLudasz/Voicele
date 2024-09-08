import React, { useEffect, useState } from 'react';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid';
import { Link, useNavigate } from 'react-router-dom';
import { Pie } from 'react-chartjs-2';
import 'chart.js/auto';

const StatsPage = () => {
  const [stats, setStats] = useState(null);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch('/api/stats/');
        if (response.ok) {
          const data = await response.json();
          setStats(data);
          /*console.log('Fetched Stats:', data);*/
        } else if (response.status === 401) {
          setError('Unauthorized');
        } else {
          setError('Failed to fetch stats.');
        }
      } catch (error) {
        setError('Stats fetching error.');
      }
    };

    fetchStats();
  }, []);

  if (error) {
    return (
      <Grid container spacing={3} alignItems="center" justifyContent="center">
        <Grid item xs={12} align="center">
          <Typography variant="h4" color="error">
            {error}
          </Typography>
        </Grid>
        <Grid item xs={12} align="center">
          <Button variant="contained" color="primary" onClick={() => navigate('/')}>
            Back
          </Button>
        </Grid>
      </Grid>
    );
  }

  if (!stats) {
    return (
      <Grid container spacing={3} alignItems="center" justifyContent="center">
        <Grid item xs={12} align="center">
          <Typography variant="h4">
            Loading...
          </Typography>
        </Grid>
      </Grid>
    );
  }

  const pieData = {
    labels: ['Games Won', 'Games Lost'],
    datasets: [
      {
        label: 'Games Statistics',
        data: [stats.games_won, stats.games_lost],
        backgroundColor: ['#FFA500', '#0000FF'],
        hoverOffset: 4,
      },
    ],
  };

  return (
    <>
      <Grid container spacing={3} alignItems="center" justifyContent="center">
        <Grid item xs={12} align="center">
          <Typography variant="h4">
            Your Statistics
          </Typography>
        </Grid>
        <Grid item xs={12} align="center">
          <Typography variant="h6">
            Games Played: {stats.games_played || 'N/A'}
          </Typography>
        </Grid>
        <Grid item xs={12} align="center">
          <Typography variant="h6">
            Games Won: {stats.games_won || 'N/A'}
          </Typography>
        </Grid>
        <Grid item xs={12} align="center">
          <Typography variant="h6">
            Games Lost: {stats.games_lost || 'N/A'}
          </Typography>
        </Grid>
        <Grid item xs={12} align="center">
          <Typography variant="h6">
            Average Guesses to Win: {stats.average_guesses_to_win || 'N/A'}
          </Typography>
        </Grid>
        <Grid item xs={12} align="center">
          <Typography variant="h6">
            Daily Streak: {stats.daily_streak || 'N/A'}
          </Typography>
        </Grid>

        {stats.language_stats && Object.keys(stats.language_stats).length > 0 && (
          <Grid item xs={12} align="center">
            <Typography variant="h6" style={{ marginTop: '20px' }}>
              Success Rate by Language:
            </Typography>
            <ul>
              {Object.entries(stats.language_stats).map(([language, rate]) => (
                <li key={language}>
                  {language}: {rate}%
                </li>
              ))}
            </ul>
          </Grid>
        )}
      </Grid>

      <div style={{ display: 'flex', justifyContent: 'center', marginTop: '20px' }}>
        <Pie data={pieData} />
      </div>

      <div style={{ display: 'flex', justifyContent: 'center', marginTop: '20px' }}>
        <Button color="primary" variant="contained" component={Link} to="/">
          Back
        </Button>
      </div>
    </>
  );
};

export default StatsPage;