const express = require('express');
const app = express();
const cors = require('cors');

app.use(cors())

app.get('/', (req, res) => {
      res.send(Math.floor(Math.random() * 1000) + 1)
})

app.listen(8080, () => {
      console.log('server listening on port 8080')
})