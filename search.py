from os import path
from gmpy2 import mpz, is_prime, bit_length
import pickle
from aks import aks_test

if path.exists('p.pkl')
	with open('p.pkl', 'rb') as f:
		p = pickle.load(f)
else:
	known_largest_prime_power = 82589933
	searching_begin_power = known_largest_prime_power * 5
	p = mpz(2) ** searching_begin_power

	with open('p.pkl', 'wb') as f:
		pickle.dump(p, f)

while True:
	t = p - 1
	if is_prime(t):
		if aks_test(t):
			print('Find interesting thing: 2**%d-1' %bit_length(t))
			with open('findings.txt', 'a') as f:
				f.write('2**%d-1\n' %bit_length(t))
	p *= 2
