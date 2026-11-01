# file for syntax analyzer

wazzup_counter = 0
buhbye_counter = 0
obtw_counter = 0
tldr_counter = 0


def syntax(lex):
	if not lex or lex[0] != 'START':
		raise SyntaxError('must start with HAI')
	if lex[-1] != 'END':
		raise SyntaxError('must end with KTHXBYE')

	i = 1
	# loops through all of the tokens and ends before KTHXBYE
	while i < len(lex) - 1:
		if (lex[i] in ('WAZZUP', 'BUHBYE')):
			vardec_helper(lex[i])
			i+=1
		elif (lex[i] in ('OBTW', 'TLDR')):
			comm_helper(lex[i])
			i+=1
		elif (lex[i] == 'GIMMEH'):		
			i = input_helper(lex, i)	# returns the next read index because input would be reading the next token as well
		else:
			i += 1
# WAZZUP needs to end in BUHBYE

# OBTW needs to end in TLDR

def vardec_helper(lex):
	pass

def comm_helper(lex):			
	if (lex[i] == 'OBTW'):
		obtw_counter += 1
	else:
		tldr_counter += 1

	if ((obtw_counter - tldr_counter) > 1):
		return 'error: obtw must be closed with tldr'
	elif ((obtw_counter - tldr_counter) < 0):
		return 'error: tldr should be paired with a obtw'

# GIMMEH needs to be followed with a variable

def input_helper(lex, i):
	if i + 1 >= len(lex) or not is_varident(lex[i+1]):
		raise SyntaxError('GIMMEH must be followed by a variable')
	return i + 2
	

# ARITHMETIC OPERATIONS ----------------------------------------

# SUM OF followed by a variable | literal | arithmetic AN followed by a variable | literal | arithmetic
# DIFF OF followed by a variable | literal | arithmetic AN followed by a variable | literal | arithmetic
# PRODUKT OF followed by a variable | literal | arithmetic AN followed by a variable | literal | arithmetic
# QUOSHUNT OF followed by a variable | literal | arithmetic AN followed by a variable | literal | arithmetic
# MOD OF followed by a variable | literal | arithmetic AN followed by a variable | literal | arithmetic

