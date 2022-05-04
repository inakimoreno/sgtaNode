const http = require('http');
const pa11y = require('pa11y');

const hostname = '127.0.0.1';
const port = 3000;

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  pa11y('google.com/').then((results) => {
    res.end(JSON.stringify(results))
  });

});

server.listen(port, hostname, () => {
  console.log(`El servidor se está ejecutando en http://${hostname}:${port}/`);
});