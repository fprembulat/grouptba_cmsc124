# file for syntax analyzer

wazzup_counter = 0
buhbye_counter = 0

def syntax(lex):
	while (lex[i] != 'KTHXBYE'):
		# HAI needs to end in KTHXBYE
		if (lex[-1] != 'KTHXBYE'):
			return 'must end with KTHXBYE'
		elif (lex[0] != 'HAI'):
			return 'must start with HAI'
		elif (lex[i] in ('WAZZUP', 'BUHBYE')):
			vardec_helper()

# WAZZUP needs to end in BUHBYE



# OBTW needs to end in TLDR

# GIMMEH needs to be followed with a variable

# ARITHMETIC OPERATIONS ----------------------------------------

# SUM OF followed by a variable | literal | arithmetic AN followed by a variable | literal | arithmetic
# DIFF OF followed by a variable | literal | arithmetic AN followed by a variable | literal | arithmetic
# PRODUKT OF followed by a variable | literal | arithmetic AN followed by a variable | literal | arithmetic
# QUOSHUNT OF followed by a variable | literal | arithmetic AN followed by a variable | literal | arithmetic
# MOD OF followed by a variable | literal | arithmetic AN followed by a variable | literal | arithmetic

