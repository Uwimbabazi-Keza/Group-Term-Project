const express = require('express');
const fetch = require('node-fetch');

const app = express();
const port = 3000;

app.get('/', (req, res) => {
  fetch('http://127.0.0.1:5501/Home.html')
    .then(response => response.text())
    .then(data => res.send(data))
    .catch(error => console.log(error));
});

app.listen(port, () => {
  console.log(`API listening at http://localhost:${port}`);
});