function hexToString(hex) {
    let string = '';
    for (let i = 0; i < hex.length; i += 2) {
      if (parseInt(hex.substr(i, 2), 16))
          string += String.fromCharCode(parseInt(hex.substr(i, 2), 16));
    }
    return string;
}

function extractData(transaction) {
    /*
    extract useful data from a transaction
    */
    let data = {};

    data.transHash = transaction.transactionHash;
    transaction = transaction.data.slice(2);

    data.from = hexToString(transaction.slice(0, transaction.length/4-1));
    data.to = hexToString(transaction.slice(transaction.length/4, transaction.length/2 - 1));
    data.prev_item_transaction = hexToString(transaction.slice(transaction.length/2, 3 * transaction.length/4 - 1));
    data.gps = hexToString(transaction.slice(3 * transaction.length/4));

    return data;
}

function getLedger(transactions) {
    let ledger = transactions.map(extractData);

    return ledger;
}

module.exports = {
    getLedger: getLedger
};
