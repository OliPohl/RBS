var http = require('http');
var url = require('url');
var fs = require('fs');
//var MongoClient = require('mongodb').MongoClient;


const { MongoClient, ServerApiVersion } = require('mongodb');
const uri = "mongodb+srv://raumgestalter01:Projektmanagment2023@raumuebersicht.9ewq6ka.mongodb.net/?retryWrites=true&w=majority";
/*MongoClient.connect(uri, function(err, db) {
  if (err) throw err;
  console.log("Database created!");
  db.close();
});*/
// Create a MongoClient with a MongoClientOptions object to set the Stable API version
const client = new MongoClient(uri, {
  serverApi: {
    version: ServerApiVersion.v1,
    strict: true,
    //deprecationErrors: true,
  }
});
async function run() {
  try {
    // Connect the client to the server    (optional starting in v4.7)
    await client.connect();
    // Send a ping to confirm a successful connection
    await client.db("admin").command({ ping: 1 });
    console.log("Pinged your deployment. You successfully connected to MongoDB!");
  } finally {
    // Ensures that the client will close when you finish/error
    await client.close();
  }
}
run().catch(console.dir);



/*console.log('Lokaler Server erstellt. Guck mal hier: http://localhost:8080/index.html');
console.log('Strg + C zum Stoppen');*/

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
