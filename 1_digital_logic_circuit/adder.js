function nor(parA, parB) {
    return !(parA || parB);
}
function nand(parA, parB) {
    return !(parA && parB);
}

function halfadder(bitA, bitB) {
    var answer = [];
    answer.push(Number(bitA && bitB));
    answer.push(Number(nand(bitA, bitB) && (bitA || bitB)));
    return answer;
}

function fulladder(bitA, bitB, carry) {
    var answer = [];
    preGate = halfadder(bitA,bitB);
    answer.push(Number(preGate[0] || halfadder(preGate[1], carry)[0]));
    answer.push(Number(halfadder(preGate[1], carry)[1]));
    return answer;
}