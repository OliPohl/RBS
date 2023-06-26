var http = require('http');
var url = require('url');
var fs = require('fs');

console.log('Lokaler Server erstellt. Guck mal hier: http://localhost:8080/index.html');
console.log('Strg + C zum Stoppen');

http.createServer(function (req, res) {
  var q = url.parse(req.url, true);
  var filename = "." + q.pathname;
  fs.readFile(filename, function(err, data) {
    if (err) {
      res.writeHead(404, {'Content-Type': 'text'});
      return res.end("404 Not Found");
    }
    res.writeHead(200, {'Content-Type': 'text'});
    res.write(data);
    return res.end();
  });
}).listen(8080);
