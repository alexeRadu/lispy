import math
import operator as op


def standard_env():
	"An environment with some Lisp standard procedures."
	env = dict()
	env.update(vars(math))
	env.update({
		'+': op.add,
		'-': op.sub,
		'*': op.mul
	})
	return env

global_env = standard_env()

def tokenize(chars):
	"Convert a string of characters into a list of tokens."
	return chars.replace('(', ' ( ').replace(')', ' ) ').split()

def atom(token):
	"Numbers become numbers; every other token is a symbol"
	try: return int(token)
	except ValueError:
		try: return float(token)
		except ValueError:
			return token

def read_from_tokens(tokens):
	"Read an expression from a sequence of tokens."
	if len(tokens) == 0:
		raise SyntaxError('unexpected EOF while reading')

	token = tokens.pop(0)
	if token == '(':
		L = []

		while tokens[0] != ')':
			L.append(read_from_tokens(tokens))

		tokens.pop(0) # pop off ')'
		return L
	elif token == ')':
		raise SyntaxError('unexpected )')
	else:
		return atom(token)

def parse(program):
	"Read a Lisp expression from a string."
	return read_from_tokens(tokenize(program))

program = "\
(begin\
	(define r 10)\
	(* pi (* r r)))"


print program
print tokenize(program)
print parse(program)
print global_env
