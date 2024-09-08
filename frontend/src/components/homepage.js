import React, { useEffect, useState } from 'react';
import { Button, Box, Typography } from '@mui/material';
import { Link, useNavigate } from 'react-router-dom';

const HomePage = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const authToken = localStorage.getItem('authToken');
    if (authToken) {
      setIsLoggedIn(true);
      fetchCurrentUser(authToken);
    }

    const hasReloaded = localStorage.getItem('hasReloaded');
    if (!hasReloaded) {
      localStorage.setItem('hasReloaded', 'true');
      window.location.reload();
    } else {
      localStorage.removeItem('hasReloaded');
    }
  }, []);

  const fetchCurrentUser = (authToken) => {
    fetch('/api/currentuser/', {
      method: 'GET',
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Token ${authToken}`,
      }
    })
      .then(response => {
        if (response.ok) {
          return response.json();
        }
        throw new Error('Failed to fetch user');
      })
      .then(data => {
        setUsername(data.username);
      })
      .catch(error => {
        console.error('Error fetching user:', error);
      });
  };

  const handleLogout = () => {
    localStorage.removeItem('authToken');
    navigate('/login');
  };

  return (
    <Box
      display="flex"
      flexDirection="column"
      justifyContent="center"
      alignItems="center"
      minHeight="100vh"
      textAlign="center"
    >
      <Typography variant="h1" component="h1" gutterBottom>
        Voicele
      </Typography>

      <Button 
        variant="contained" 
        color="primary" 
        component={Link} 
        to="/creategame"
        style={{ marginBottom: '10px', width: '200px' }}
      >
        Start Game
      </Button>
      <Button 
        variant="contained" 
        color="primary" 
        component={Link} 
        to="/pastgames"
        style={{ marginBottom: '10px', width: '200px' }}
      >
        Past Games
      </Button>
      <Button 
        variant="contained" 
        color="primary" 
        component={Link} 
        to="/stats"
        style={{ marginBottom: '10px', width: '200px' }}
      >
        Stats
      </Button>

      {isLoggedIn ? (
        <>
          <Button 
            variant="contained" 
            color="secondary" 
            onClick={handleLogout}
            style={{ marginBottom: '10px', width: '200px' }}
          >
            Log Out
          </Button>
          <Typography variant="h6">
            Logged in as: {username}
          </Typography>
        </>
      ) : (
        <>
          <Button 
            variant="contained" 
            color="primary" 
            component={Link} 
            to="/login"
            style={{ marginBottom: '10px', width: '200px' }}
          >
            Log In
          </Button>
          <Button 
            variant="contained" 
            color="primary" 
            component={Link} 
            to="/register"
            style={{ width: '200px' }}
          >
            Register
          </Button>
        </>
      )}
    </Box>
  );
};

export default HomePage;