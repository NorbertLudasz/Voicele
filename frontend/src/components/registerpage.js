import React, { useState } from 'react';
import { TextField, Button, Grid, Typography } from "@mui/material";
import { Link, useNavigate } from "react-router-dom";

const RegisterPage = () => {
  /*console.log("functional register page loaded")*/
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleUsernameChange = (e) => {
    setUsername(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleRegisterPressed = () => {
    if (!username || !password) {
      setError("Both fields are required.");
      return;
    }

    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    const requestOptions = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify({
        username: username,
        password: password,
      }),
    };

    /*console.log("Request Options:", requestOptions);
    console.log("CSRF Token:", csrfToken);*/

    fetch('/api/register/', requestOptions)
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        throw new Error("Registration failed");
      })
      .then((data) => {
        /*console.log(data);*/
        setError('');
        navigate('/login'); // Use navigate to redirect to the login page after successful registration
      })
      .catch((error) => {
        console.log('Error:', error);
        setError("Registration failed. Try again.");
      });
  };

  return (
    <Grid container spacing={1} alignItems="center" justifyContent="center">
      <Grid item xs={12} align="center">
        <Typography component="h4" variant="h4">
          Register
        </Typography>
      </Grid>
      <Grid item xs={12} align="center">
        <TextField
          label="Username"
          variant="outlined"
          value={username}
          onChange={handleUsernameChange}
          required
        />
      </Grid>
      <Grid item xs={12} align="center">
        <TextField
          label="Password"
          type="password"
          variant="outlined"
          value={password}
          onChange={handlePasswordChange}
          required
        />
      </Grid>
      {error && (
        <Grid item xs={12} align="center">
          <Typography color="error">{error}</Typography>
        </Grid>
      )}
      <Grid item xs={12} align="center">
        <Button color="primary" variant="contained" onClick={handleRegisterPressed}>
          Register
        </Button>
      </Grid>
      <Grid item xs={12} align="center">
        <Button color="secondary" variant="contained" component={Link} to="/login">
          Already have an account? Login
        </Button>
      </Grid>
      <Grid item xs={12} align="center">
        <Button color="primary" variant="contained" component={Link} to="/">
          Back
        </Button>
      </Grid>
    </Grid>
  );
};

export default RegisterPage;