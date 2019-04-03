function dec2bin(decimal) {
    var answer = [];
    var remainder;

    do {
        remainder = decimal % 2;
        answer.push(remainder);
        decimal = parseInt(decimal / 2);
    } while (decimal != 0)

    return answer;
};