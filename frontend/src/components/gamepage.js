import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Typography, Button, FormControl, InputLabel, Select, MenuItem, TextField } from '@mui/material';

const GamePage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [isAuthorized, setIsAuthorized] = useState(null);
  const [selectedLanguage, setSelectedLanguage] = useState('');
  const [resultMessage, setResultMessage] = useState('');
  const [funFact, setFunFact] = useState('');
  const [gameOverHint, setGameOverHint] = useState('');
  const [hint1, setHint1] = useState('');
  const [hint2, setHint2] = useState([]);
  const [hint3, setHint3] = useState('');
  const [showMultipleChoice, setShowMultipleChoice] = useState(false);
  const [phraseSound, setPhraseSound] = useState('');
  const [phraseSoundAI, setPhraseSoundAI] = useState('');

  useEffect(() => {
    const authToken = localStorage.getItem('authToken');
    /*console.log("gamepage got authtoken: ", authToken);*/

    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    /*console.log("gamepage got csrf: ", csrfToken);*/

    if (!authToken) {
      navigate("/login");
      return;
    }

    const requestOptions = {
      method: 'GET',
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
        "Authorization": `Token ${authToken}`,
      },
    };

    /*console.log("Gamepage Request Options Body:", requestOptions.body);
    */
    fetch(`/api/gameauth/${id}/`, requestOptions)
      .then(response => response.json())
      .then(data => {
        if (data.authorized) {
          /*console.log("gamepage viewing authorized");*/
          setIsAuthorized(true);
          setPhraseSound(data.phraseSound);
          const aiFile = data.phraseSound.replace('.mp3', 'AI.mp3');
          setPhraseSoundAI(aiFile);
          /*console.log("got phrasesound: ", data.phraseSound);
          console.log("generated AI phrasesound: ", aiFile);*/
        } else {
          /*console.log("gamepage viewing unauthorized");*/
          setIsAuthorized(false);
        }
      })
      .catch(error => {
        console.error('Error:', error);
        setIsAuthorized(false);
      });
  }, [id, navigate]);

  const handleGuess = () => {
    const authToken = localStorage.getItem('authToken');
    /*console.log("handleguess authtoken: ", authToken);*/
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    /*console.log("handleguess got csrf: ", csrfToken);*/
    const requestOptions = {
      method: 'POST',
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
        "Authorization": `Token ${authToken}`,
      },
      body: JSON.stringify({
        selected_language: selectedLanguage,
      }),
    };

    /*console.log("Gamepage Guess Request Options Body:", requestOptions.body);*/

    fetch(`/api/guess/${id}/`, requestOptions)
      .then(response => response.json())
      .then(data => {
        /*console.log("data result: ", data.result);*/
        setResultMessage(data.result);
        /*console.log("data result: ", data.result)*/
        if (data.gameStatus == 2) {
          setFunFact(data.funFact || "No fun fact available.");
        } else if (data.gameStatus == 0) {
          setGameOverHint(data.languageHint || "No hint available.");
        }

        if (data.hint1) {
          setHint1(data.hint1);
        }

        if (data.hint2 && data.hint2.length > 0) {
          setHint2(data.hint2);
          setShowMultipleChoice(true);
        }

        if (data.hint3) { 
          setHint3(data.hint3);
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
  };

  if (isAuthorized === null) {
    return <Typography>Loading...</Typography>;
  }

  const languageOptions = [
    "Afrikaans", "Albanian", "Amharic", "Arabic", "Armenian", "Azerbaijani", 
    "Bengali", "Bislama", "Bosnian", "Bulgarian", "Burmese", "Cantonese", 
    "Catalan", "Chichewa", "Chinese", "Croatian", "Czech", "Danish", "Dhivehi", 
    "Dutch", "Dzongkha", "English", "Estonian", "Fijian", "Filipino", "Finnish", 
    "French", "Georgian", "German", "Greek", "Guarani", "Hebrew", "Hindi", 
    "Hungarian", "Icelandic", "Indonesian", "Irish", "Italian", "Japanese", 
    "Kazakh", "Khmer", "Kinyarwanda", "Korean", "Kurdish", "Kyrgyz", 
    "Lao", "Latvian", "Lithuanian", "Luxembourgish", "Macedonian", "Malagasy", 
    "Malay", "Malayalam", "Maltese", "Mandarin", "Maori", "Marathi", 
    "Moldovan", "Mongolian", "Montenegrin", "Nauruan", "Nepali", "Norwegian", 
    "Pashto", "Persian", "Polish", "Portuguese", "Punjabi", "Quechua", 
    "Romanian", "Russian", "Samoan", "Serbian", "Sinhala", "Slovak", 
    "Slovenian", "Somali", "Sotho", "Spanish", "Swahili", "Swedish", 
    "Tajik", "Tamil", "Tatar", "Telugu", "Thai", "Tigrinya", "Tok Pisin", 
    "Tongan", "Turkish", "Turkmen", "Ukranian", "Urdu", "Uzbek", 
    "Vietnamese", "Welsh", "Xhosa", "Zulu"
];

  return (
    <div>
      {isAuthorized ? (
        <div>
          <Typography variant="h4">Game Started</Typography>
          
          {phraseSound && (
            <audio controls style={{ marginTop: '20px', width: '100%' }}>
              <source src={`/static/soundfiles/${phraseSound}`} type="audio/mp3" />
              Error displaying audio element.
            </audio>
          )}

          {phraseSoundAI && (
            <audio controls style={{ marginTop: '20px', width: '100%' }}>
              <source src={`/static/soundfiles/${phraseSoundAI}`} type="audio/mp3" />
              Error displaying audio element.
            </audio>
          )}

          <FormControl fullWidth margin="normal">
            <InputLabel id="select-language-label">Select Language</InputLabel>
            <Select
              labelId="select-language-label"
              value={selectedLanguage}
              onChange={(e) => setSelectedLanguage(e.target.value)}
            >
              {languageOptions.map((language) => (
                <MenuItem key={language} value={language}>{language}</MenuItem>
              ))}
            </Select>
          </FormControl>

          <div>
            <Button
              variant="contained"
              color="primary"
              onClick={handleGuess}
              disabled={!selectedLanguage}
            >
              Make Guess
            </Button>
          </div>

          {resultMessage && (
            <Typography variant="h6" color="secondary" style={{ marginTop: '20px' }}>
              {resultMessage}
            </Typography>
          )}

          {funFact && (
            <Typography variant="h6" style={{ marginTop: '20px', color: 'green' }}>
              Fun Fact: {funFact}
            </Typography>
          )}

          {gameOverHint && (
            <Typography variant="h6" style={{ marginTop: '20px', color: 'red' }}>
              Hint for Next Time: {gameOverHint}
            </Typography>
          )}

          {hint1 && (
            <TextField
              label="Hint 1"
              variant="outlined"
              fullWidth
              value={hint1}
              margin="normal"
              disabled
            />
          )}

          {showMultipleChoice && (
            <Button
              variant="contained"
              color="secondary"
              onClick={() => alert("Possible languages: " + hint2.join(', '))}
            >
              Multiple Choice Hint
            </Button>
          )}

          {hint3 && (
            <Typography variant="h6" style={{ marginTop: '20px', color: 'blue' }}>
              Language Family: {hint3}
            </Typography>
          )}

          <div>
            <Button
              variant="contained"
              color="secondary"
              onClick={() => navigate("/")}
              style={{ marginTop: '20px' }}
            >
              Back
            </Button>
          </div>
        </div>
      ) : (
        <div>
          <Typography variant="h4" color="error">Unauthorized</Typography>
          <Button color="primary" variant="contained" onClick={() => navigate("/")}>
            Go Back
          </Button>
        </div>
      )}
    </div>
  );
};

export default GamePage;