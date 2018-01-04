const blockchain = require('./config');
const app = require('express')();
const bodyParser = require('body-parser');

app.use(bodyParser.urlencoded({extended: true}));
app.use(bodyParser.json());

function viewLedger(req, res) {
    blockchain.useLedgers((err, ledger) => {
        if (err)
            res.json({
                status: 'some internal error occured'
            });
        else {
            res.json({
                status: 'success',
                ledger: ledger
            });
        }
    });
}

function makeTransaction(req, res) {
    /*
    expected request body:
    from: from uid
    to: to uid
    jwt: token of user
    gps: string
    prev_item_transaction
    */
    let from = req.body.from;
    let to = req.body.to;
    let prev_trans = req.body.prev_trans;
    let gps = req.body.gps;

    try {
        let transHash = blockchain.sendTransaction(from, to, prev_trans, gps);

        res.json({
            status: 'success',
            transactionHash: transHash,
            dateOfTransaction: new Date()
        })
    }
    catch(err) {
        console.log(err);

        res.json({
            status: 'some internal error occured'
        })
    }    
}

// TODO route to verify the transactions

app.route('/viewLedger')
.get(viewLedger);

app.route('/transaction')
.post(makeTransaction);

app.use((req, res) => {
    res.json({
        status: 'invalid url'
    });
});

app.listen(8080);
