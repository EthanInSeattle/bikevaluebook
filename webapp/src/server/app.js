const express = require('express');
const app = express();
const bodyParser = require('body-parser');
const path = require('path');
const PORT = process.env.PORT || 8000;

app.use(express.static(path.join(__dirname, '../../dist')));
app.use(bodyParser.json());


app.get('/api/getRequest', (req, res) => {
 //API logic
 res.send("hello!");
});

app.post('/api/postRequest', (req, res) => {
 //API logic
});

app.get('*/bundle.js', (req,res) => {
    res.sendFile(path.join(__dirname, '../../dist/bundle.js'));
   });
  
app.get('*', (req,res) => {
res.sendFile(path.join(__dirname, '../../dist/index.html'));
});

app.listen(PORT, () => {
 console.log('Listening on port', PORT);
});