# file for syntax analyzer

wazzup_counter = 0
buhbye_counter = 0
obtw_counter = 0
tldr_counter = 0

def syntax(lex):
	while (lex[i] != 'KTHXBYE'):
		# HAI needs to end in KTHXBYE
		if (lex[-1] != 'KTHXBYE'):
			return 'must end with KTHXBYE'
		elif (lex[0] != 'HAI'):
			return 'must start with HAI'
		elif (lex[i] in ('WAZZUP', 'BUHBYE')):
			vardec_helper(lex[i])
		elif (lex[i] in ('OBTW', 'TLDR')):
			comm_helper(lex[i])
		elif (lex[i] == 'GIMMEH'):
			input_helper(lex[i])

# WAZZUP needs to end in BUHBYE

# OBTW needs to end in TLDR

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

def input_helper(lex):


# ARITHMETIC OPERATIONS ----------------------------------------

# SUM OF followed by a variable | literal | arithmetic AN followed by a variable | literal | arithmetic
# DIFF OF followed by a variable | literal | arithmetic AN followed by a variable | literal | arithmetic
# PRODUKT OF followed by a variable | literal | arithmetic AN followed by a variable | literal | arithmetic
# QUOSHUNT OF followed by a variable | literal | arithmetic AN followed by a variable | literal | arithmetic
# MOD OF followed by a variable | literal | arithmetic AN followed by a variable | literal | arithmetic

