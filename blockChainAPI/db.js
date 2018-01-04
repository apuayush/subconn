const MongoClient = require('mongodb').MongoClient;
const url = require('./db.json');
const dbname = 'subconn';
const tokenColl = 'token';

function validateUser(token, callback) {
    /* 
    token to validate, callback to execute on validation
    */
    MongoClient.connect(url.url)
    .then(function(client) {
        const db = client.db(dbname);
        const col = db.collection(tokenColl);

        let p = col.find({token: token})
        .toArray((err, docs) => {
            console.log(docs.length);
            if (!err)
                callback(null, docs);
            else
                callback(err, docs);
        });
        client.close();
    })
    .catch(err => {
        callback(err, null);
    });
}


module.exports = {
    validateUser: validateUser
}