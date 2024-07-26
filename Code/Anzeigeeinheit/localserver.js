var http = require('http');
var url = require('url');
var fs = require('fs');
var path = require('path');

var jsonPath = path.join(__dirname, 'js', 'data.json');
const { MongoClient, ServerApiVersion } = require('mongodb');
var uri = "mongodb+srv://raumgestalter01:Projektmanagment2023@raumuebersicht.9ewq6ka.mongodb.net/?retryWrites=true&w=majority";
const client = new MongoClient(uri, {
  serverApi: {
    version: ServerApiVersion.v1,
    strict: true,
    deprecationErrors: true,
  }
});
var minutes = 1, the_interval = minutes * 60 * 100;
async function run() {
  try {
    await client.connect().then();
    const daba = client.db("Raumuebersicht");
    const col = daba.collection("raeume");
    setInterval(async function(){
      fs.writeFileSync(jsonPath, '', function(err){if (err) throw err;})
      var stream = fs.createWriteStream(jsonPath, {flags:'a'});
      stream.write("{");
      let string1 = "rooms";
      let jsonStr1 = JSON.stringify(string1);
      stream.write(jsonStr1);
      stream.write(":[");
      var dataSet = await daba.collection("raeume").find().toArray();
      console.log(dataSet);
      var zaehler = 0;
      for await(var doc of dataSet) {
        if (zaehler > 0) {
          stream.write(",");
        }
        let data = JSON.stringify(doc);
        console.log(data);
        stream.write(data);
        zaehler = zaehler + 1;
      }
      stream.write("]}");
      stream.end();  
    }, the_interval);  
  } finally {
    //await client.close();
  }  
}
run().catch(console.dir);

/*console.log('Lokaler Server erstellt. Guck mal hier: http://localhost:8080/index.html');
console.log('Strg + C zum Stoppen');*/

http.createServer(function (req, res) {
  var q = url.parse(req.url, true);
  var filename = path.join(__dirname, q.pathname) ;
    if (path.normalize(decodeURI(q.pathname)) !== decodeURI(q.pathname)) {
        res.statusCode = 403;
        res.end();
        return;
    }
  fs.readFile(filename, function(err, data) {
    if (err) {
      console.log(err);
      res.writeHead(404, {'Content-Type': 'text'});
      return res.end("404 Not Found");
    }
    var validExtensions = {
      ".html" : "text/html",
      ".js": "application/javascript",
      ".css": "text/css",
      ".txt": "text/plain",
      ".jpg": "image/jpeg",
      ".gif": "image/gif",
      ".png": "image/png",
      ".woff": "application/font-woff",
      ".woff2": "application/font-woff2"
    };
    res.writeHead(200, {'Content-Type': 'text'});
    res.write(data);
    return res.end();
  });
}).listen(8080);