from os import path
from gmpy2 import mpz, is_prime, log
import pickle
from aks import aks_test
import ray

@ray.remote
def search_range(x, step=2):
	if x & 1 == 0:
		x += 1
	return_val = []
	for i in range(x, x + 2*log(x), step):
		if is_prime(i):
			return_val.append(i)
	return return_val


def next_prime(x, num_workers=31):
	# search range split
	jobs = []
	for i in range(num_workers):
		jobs.append(search_range.remote(x + i*2, num_workers*2))
	return [i for e in ray.get(jobs) for i in e]


ray.init()
known_largest_prime_power = mpz(82589933)
searching_power = known_largest_prime_power * 5

if path.exists('p.pkl'):
	with open('p.pkl', 'rb') as f:
		p = pickle.load(f)
else:
	p = mpz(2) ** searching_power

	with open('p.pkl', 'wb') as f:
		pickle.dump(p, f)


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
	searching_powers = next_prime(searching_powers[-1])
