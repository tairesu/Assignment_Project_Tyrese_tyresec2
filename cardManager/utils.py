import random

def rand_char():
	chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
	rand_int = random.randint(0, len(chars) - 1)
	return chars[rand_int]

def gen_card_token():
	token = ''
	token_length = 7
	while len(token) < token_length:
		token += rand_char()
	return token
