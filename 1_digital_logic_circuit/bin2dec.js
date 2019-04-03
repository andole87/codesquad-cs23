function bin2dec(bin) {
    var answer = 0;

    for (let i = 0; i < bin.length; i++) {
        answer += (2 ** i) * bin[i];
    }

    return answer;
}