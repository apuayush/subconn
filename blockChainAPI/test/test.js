const expect = require('chai').expect;
const bc = require('../config');
const db = require('../db');

describe.skip('validate token of user', () => {
    it('return an array', (done) => {
        let sample = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1aWQiOiIzMzk1MTg3MTQ1MzciLCJ0aW1lIjoiMDQtMDEtMjAxOCAwMjo0MSBQTSJ9.UfG_b2A5J0gDn5OqDuUrp43NiK-qc-sFDP3A4SBiBHs';
        
        db.validateUser(sample, (err, res) => {
            console.log(res);
            if (!err) {
                expect(res.length).to.equal(1);
                done();
            }                
        });
    });
});

describe('getting ledgers', () => {
    it('return an array', (done) => {
        bc.useLedgers((err, res) => {
            expect(res).to.be.an('array');
            done();
        });
    });
});

describe('make a transaction', () => {
    it('return an hash string', (done) => {
        bc.sendTransaction('testfrom', 'testto', 'null', 'testgps');
        done();
    });
});