#include<stdio.h>
#include<stdlib.h>
#include<assert.h>
#include<string.h>
_int16 peek(_int16* mem, unsigned address) {
	assert(0 <= address && address <= 131071);
	return mem[address];
}

void locate(_int16* mem, _int16* program, unsigned length) {
	for (int i = 0; i < length; i++) {
		mem[i] = program[i];
	}
}

_int16 fetch(_int16* mem, _int16 program_count) {
	return mem[program_count];
}

_int16 load(_int16* mem, _int16 address) {
	_int16 edited_address = 65535 + address;
	assert(65536 <= edited_address && edited_address <= 131071);
	return mem[edited_address];
}

void store(_int16* mem, _int16 address, _int16 data) {
	_int16 edited_address = 65535 + address;
	assert(65536 <= edited_address && edited_address <= 131071);
	mem[edited_address] = data;
}

int main() {
	_int16 *memory = (_int16*)malloc(sizeof(_int16) * 2 << 16);
	
	_int16 program[7] = { 1, 2, 3, 4, 5, 6, 7 };

	locate(memory, program, 14);
	
	for (int i = 0; i < sizeof(program)/sizeof(_int16); i++) {
		printf("%d\n", peek(memory, i));
	}
	free(memory);
}