contract Trans {
    address public owner;

    function Trans() {
        owner = msg.sender;
    }

    event TransactionSuccessful(bytes32 from, bytes32 to, bytes32 prev_item_transaction, bytes32 gps);

    function makeTransaction(bytes32 from, bytes32 to, bytes32 prev_item_transaction, bytes32 gps) public {
        TransactionSuccessful(from, to, prev_item_transaction, gps);
    }
}