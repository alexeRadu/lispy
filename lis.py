#!/usr/bin/python
import math
import operator as op


class Env(dict):
	"An environment: a dict of {'var':val} pairs, with an outher Env."
	def __init__(self, params = (), args = (), outer = None):
		self.update(zip(params, args))
		self.outer = outer

	def find(self, var):
		return self if (var in self) else self.outer.find(var)

def standard_env():
	"An environment with some Lisp standard procedures."
	env = Env()
	env.update(vars(math))
	env.update({
		'+': op.add,
		'-': op.sub,
		'*': op.mul,
		'/': op.div,
		'>': op.gt,
		'<': op.lt,
		'>=': op.ge,
		'<=': op.le,
		'=': op.eq,
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

class Procedure(object):
	"A user-defined Lisp procedure."
	def __init__(self, params, body, env):
		self.params = params
		self.body = body
		self.env = env

	def __call__(self, *args):
		return eval(self.body, Env(self.params, args, self.env))

def eval(x, env=global_env):
	"Evaluate an expression in an environment."
	if isinstance(x, str):		# variable reference
		return env.find(x)[x]
	elif not isinstance(x, list):	# constant literal
		return x
	elif x[0] == 'quote':		# quotation
		(__, exp) = x
		return exp
	elif x[0] == 'if':		# conditional
		(_, test, conseq, alt) = x
		exp = (conseq if eval(test, env) else alt)
		return eval(exp, env)
	elif x[0] == 'define':		# definition
		(_, var, exp) = x
		env[var] = eval(exp, env)
	elif x[0] == 'set!':		# assignment
		(_, var, exp) = x
		env.find(var)[var] = eval(exp, env)
	elif x[0] == 'lambda':		# procedure
		(_, params, body) = x
		return Procedure(params, body, env)
	else:				# procedure call
		proc = eval(x[0], env)
		args = [eval(arg, env) for arg in x[1:]]
		return proc(*args)

def repl(prompt='lis.py> '):
	"A prompt-read-eval-print loop."
	while True:
		val = eval(parse(raw_input(prompt)))
		if val is not None:
			print str(val)

repl()
