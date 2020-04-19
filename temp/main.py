import random

def check_code(char, code):
	print(char)
	moorse_input = input()
	if moorse_input == 'exit':
		exit()
	else:
		if moorse_input == code:
			print('Correct')
		else:
			print('Wrong!! Try again')
			check_code(char, code)


alphanum_chars = []
morse_codes = []
with open('morse_code.csv', 'r') as morse_file:
	for line in morse_file:
		alphanum_chars.append(line.strip().split(',')[0])
		morse_codes.append(line.strip().split(',')[1])

print('Give the morse code for the shown alpha numeric character\nGive "exit" as input at any time to leave')

while (True):
	rand_index = random.randrange(0,len(alphanum_chars))
	check_code(alphanum_chars[rand_index], morse_codes[rand_index])
