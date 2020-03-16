from os import path
from gmpy2 import mpz, log, next_prime
import pickle
from aks import aks_test
import ray

@ray.remote
def search_range(x, y):
	return_val = []
	while x < y:
		x = next_prime(x)
		return_val.append(x)
	return return_val[:-1]


def search_next_prime(x, num_workers=31):
	# search range split
	step =  2*log(x)//num_workers
	jobs = [search_range.remote(x + step*i, mpz(x + step*i + step)) for i in range(num_workers)]
	return [i for e in ray.get(jobs) for i in e]


ray.init()
known_largest_prime_power = mpz(82589933)
searching_power = known_largest_prime_power * 5

if path.exists('p.pkl'):
	with open('p.pkl', 'rb') as f:
		p = pickle.load(f)
	with open('pow.pkl', 'rb') as f:
		searching_power = pickle.load(f)
else:
	p = mpz(2) ** searching_power

	with open('p.pkl', 'wb') as f:
		pickle.dump(p, f)
	with open('pow.pkl', 'wb') as f:
		pickle.dump(searching_power, f)


searching_powers = [searching_power]
pre_searching_power = searching_power
while True:
	for searching_power in searching_powers:
		if aks_test(searching_power) == "prime":
			p *= mpz(2)**(searching_power-pre_searching_power)
			pre_searching_power = searching_power
			t = p - 1
			if is_prime(t):
				if aks_test(t) == "prime":
					print('Find interesting thing: 2**%s-1' %searching_power)
					with open('findings.txt', 'a') as f:
						f.write('2**%s-1\n' %searching_power)
	searching_powers = search_next_prime(searching_powers[-1])
	# Checkpoint
	with open('p.pkl', 'wb') as f:
		pickle.dump(p, f)
	with open('pow.pkl', 'wb') as f:
		pickle.dump(searching_powers[-1], f)
