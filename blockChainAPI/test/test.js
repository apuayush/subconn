const expect = require('chai').expect;
const bc = require('../config');

describe('getting ledgers', () => {
    it('return an array', (done) => {
        bc.useLedgers((err, res) => {
            expect(res).to.be.an('array');
            done();
        });
    });
});

describe.skip('make a transaction', () => {
    it('return an hash string', (done) => {
        bc.sendTransaction('testfrom', 'testto');
        done();
    });
});