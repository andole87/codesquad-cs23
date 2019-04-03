function nor(parA, parB) {
    return !(parA || parB);
};
function nand(parA, parB) {
    return !(parA && parB);
};

function halfadder(bitA, bitB) {
    var answer = [];
    answer.push(Number(bitA && bitB));
    answer.push(Number(nand(bitA, bitB) && (bitA || bitB)));
    return answer;
};

function fulladder(bitA, bitB, carry) {
    var answer = [];
    preGate = halfadder(bitA, bitB);
    answer.push(Number(preGate[0] || halfadder(preGate[1], carry)[0]));
    answer.push(Number(halfadder(preGate[1], carry)[1]));
    return answer;
};

function byteAdder(byteA, byteB) {
    var answer = [];
    var carry = [0];

    for (let i = 0; i < byteA.length; i++) {
        temp = fulladder(byteA[i], byteB[i], carry[i]);
        carry.push(temp[0]);
        answer.push(temp[1]);
    }
    answer.push(carry[carry.length - 1]);
    return answer;
};