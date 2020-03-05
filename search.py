from os import path
from gmpy2 import mpz, is_prime, bit_length, next_prime
import pickle
from aks import aks_test

if path.exists('p.pkl')
	with open('p.pkl', 'rb') as f:
		p = pickle.load(f)
else:
	known_largest_prime_power = mpz(82589933)
	searching_power = known_largest_prime_power * 5
	p = mpz(2) ** searching_power

	with open('p.pkl', 'wb') as f:
		pickle.dump(p, f)


pre_p = p
pre_searching_power = searching_power
while True:
	if aks_test(searching_power) == "prime":
		p *= mpz(2)**(searching_power-pre_searching_power)
		pre_searching_power = searching_power
		t = p - 1
		if is_prime(t):
			if aks_test(t) == "prime":
				print('Find interesting thing: 2**%s-1' %searching_power)
				with open('findings.txt', 'a') as f:
					f.write('2**%s-1\n' %searching_power)
	searching_power = next_prime(searching_power)
