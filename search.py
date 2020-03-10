from os import path
from gmpy2 import mpz, is_prime, bit_length
import pickle
from aks import aks_test
import ray

@ray.remote
def search_range(x, r=8192):
	if x & 1 == 0:
		x += 1
	return_val = []
	for i in range(x, x + r, 2):
		if is_prime(i):
			return_val.append(i)
	return return_val


def next_prime(x, num_workers=31):
	# search range split
	jobs = []
	while True:
		for x in range(x, x + num_workers, 2):
			jobs.append(search_range.remote(x))
		result = ray.get(jobs)
		if sum(result):
			return_val = []
			for i in result:
				for j in i:
					if j:
						return_val.append(j)
			return return_val


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
