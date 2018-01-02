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
    let from = req.body.from;
    let to = req.body.to;

    try {
        let transHash = blockchain.sendTransaction(from, to);

        res.json({
            status: 'success',
            transactionHash: transHash
        })
    }
    catch(err) {
        console.log(err);

        res.json({
            status: 'some internal error occured'
        })
    }    
}

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
