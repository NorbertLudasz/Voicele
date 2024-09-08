import React, { useState } from 'react';
import { TextField, Button, Grid, Typography } from "@mui/material";
import { Link, useNavigate } from "react-router-dom";

const LoginPage = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleUsernameChange = (e) => {
    setUsername(e.target.value);
  };

  const handlePasswordChange = (e) => {
    setPassword(e.target.value);
  };

  const handleLoginPressed = () => {
    if (!username || !password) {
      setError("Both fields are required.");
      return;
    }

    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    /*console.log('CSRF Token during login:', csrfToken);*/

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

    fetch('/api/login/', requestOptions)
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        throw new Error("Login failed");
      })
      .then((data) => {
        /*console.log("Response data: ", data);
        console.log("token from response: ", data.token)*/
        if(data.token) {
          localStorage.setItem('authToken', data.token); // Save the auth token in local storage
          const storedToken = localStorage.getItem('authToken');
          /*console.log("Token retrieved from localStorage:", storedToken);*/

          setError('');//was ""
          navigate("/"); // Redirect to home after successful login
        } else {
            throw new Error("Token not found in response");
          }
      })
      .catch((error) => {
        console.log('Error:', error);
        setError("Login failed. Check your credentials and try again.");
      });
  };

  return (
    <Grid container spacing={1} alignItems="center" justify="center">
      <Grid item xs={12} align="center">
        <Typography component='h4' variant='h4'>
          Login
        </Typography>
      </Grid>
      <Grid item xs={12} align="center">
        <TextField
          label="Username"
          variant="outlined"
          onChange={handleUsernameChange}
          required
        />
      </Grid>
      <Grid item xs={12} align="center">
        <TextField
          label="Password"
          type="password"
          variant="outlined"
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
        <Button color="primary" variant="contained" onClick={handleLoginPressed}>
          Login
        </Button>
      </Grid>
      <Grid item xs={12} align="center">
        <Button color="secondary" variant="contained" to="/register" component={Link}>
          Don't have an account? Register
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

export default LoginPage;