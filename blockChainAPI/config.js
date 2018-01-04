const {getLedger} = require('./utils');
const Web3 = require('web3');

let web3 = new Web3(new Web3.providers.HttpProvider('http://localhost:8042'));

// might change when we deploy a new contract
let abi = [{"constant":false,"inputs":[{"name":"from","type":"bytes32"},{"name":"to","type":"bytes32"},{"name":"prev_item_transaction","type":"bytes32"},{"name":"gps","type":"bytes32"}],"name":"makeTransaction","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"name":"from","type":"bytes32"},{"indexed":false,"name":"to","type":"bytes32"},{"indexed":false,"name":"prev_item_transaction","type":"bytes32"},{"indexed":false,"name":"gps","type":"bytes32"}],"name":"TransactionSuccessful","type":"event"}];
let adr = '0x995cde5a5c695cf77689c343ec4b74f3dd7c1205';
let contract = web3.eth.contract(abi).at(adr);

// enable transactions from account 0
web3.eth.defaultAccount = web3.eth.accounts[0];

function getAccounts() {
    /*
    get all accounts in the current node of the
    blockchain
    */
    return web3.eth.accounts;
}

function sendTransaction(from, to, prev_item_transaction, gps) {
    /*
    make a transaction and return the transaction hash
    NOTE: the client(geth) needs to be mining for transaction to 
    complete
    */
    let transHash = contract.makeTransaction(from, to, prev_item_transaction, gps);
    return transHash;
}

function useLedgers(callback) {
    /*
    get all the ledgers of the blockchain
    corresponding to the contract
    callback: args - err, res{an array of transactions}
    */
    let options = {
        fromBlock: 0,
        from: 0,
        toBlock: 'latest',
        to: 'latest',
        address: adr,
        topics: [web3.sha3('TransactionSuccessful(bytes32,bytes32,bytes32,bytes32)')]
    };

    let filter = web3.eth.filter(options);

    function wrapper(err, res) {
        // extract reqd data before callback
        if (err) {
            callback(err, null);
        }
        else {
            let ledger = getLedger(res);

            callback(null, ledger);
        }
    }

    filter.get(wrapper);
}

module.exports = {
    sendTransaction: sendTransaction,
    useLedgers: useLedgers
}
