
const { MongoClient, ServerApiVersion } = require('mongodb');
const uri = "mongodb+srv://umaidansari123:<password>@cluster0.evumt2u.mongodb.net/?retryWrites=true&w=majority";
const client = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true, serverApi: ServerApiVersion.v1 });
client.connect(err => {
  const collection = client.db("test").collection("devices");
  // perform actions on the collection object
  client.close();
});

mongodb+srv://umaidansari123:<password>@cluster0.evumt2u.mongodb.net/?retryWrites=true&w=majority
