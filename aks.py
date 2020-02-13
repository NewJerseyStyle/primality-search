"""
Successful implementation of aks primality test.
"""

from gmpy2 import log, sqrt, floor


def aks_test(n):
    """
    Implement the AKS primality test.
    """
    # Check if n is a perfect power. If so, return composite.
    if is_perfect_power(n):
        return "composite"
    
    # Find the smallest r such that the multiplicative order of n modulo r
    # is greater than log(n, 2)^2
    r = get_r(n)

    # If 1 < gcd(a, n) < n for some a <= r, return composite
    for a in range(1, r):
        if gcd(a, n) > 1 and gcd(a, n) < n:
            return "composite"

    # If n <= r, return prime
    if n <= r:
        return "prime"

    # Check if (x + a)^n mod (x^r - 1, n) != (x^n + a) mod (x^r - 1, n)
    for a in range(1, floor(sqrt(phi(r)) * log(n, 2))):
        if not is_congruent(a, n, r):
            return "composite"

    return "prime"


def ord(a, n):
    """
    Computes the multiplicative order of a modulo n, namely the smallest
    number k such that a^k is congruent with 1 (mod n). The multiplicative
    order only exists when a and n are coprime. 
    """
    k = 2
    while True:
        if (pow(a, k) % n) == 1:
            break
        else:
            k += 1
    
    return k


def is_perfect_power(n):
    """
    Returns True if n is a perfect power, that is, if there exist integers
    a and b such that n = a^b. This algorithm was proposed in
    https://link.springer.com/article/10.1007/BF01228507
    """
    # If n is a perfect bth power, then b <= log(n). Therefore, compute an
    # integer approximation x of n^(1/b) for every such b, starting with b = 2.
    # Only prime values of b need to be used.
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    b = 2
    while b <= (log(n, 2) + 1):
        if b in primes:
            # Establish upper limit for search of bases x to prime b
            lim = pow(2, (log(n, 2) / b) + 1)

            # Do a search between 2 and lim (BINARY SEARCH to optimise)
            x = 2
            while x <= int(lim):
                if pow(x, b) == n:
                    return True
                else:
                    x += 1
            b += 1
        else:
            b += 1
    
    return False


def gcd(a, b):
    """
    Euclidean algorithm for computing the greatest common divisor of two integers.
    """
    while b > 0: 
        a, b = (b, a % b)

    return a


def phi(n):
    """
    Counts the positive integers up to given integer n that are coprime with n.
    Also known as Euler's totient (or phi) function.
    """
    return len([x for x in range(1, n) if gcd(x, n) == 1])


def get_r(n):
    """
    Find the smallest r such that the multiplicative order of n modulo r
    is greater than log(n, 2)^2. If r and n are not coprime, skip this r.
    """
    r = 2
    while True:
        if gcd(r, n) != 1:
            r += 1
        elif ord(n, r) > pow(log(n, 2), 2):
            break
        else:
            r += 1
    
    return r


def polyMult(a, b, r, p):
    """
    Implements multiplication of polynomials a and b.
    """
    res = [0] * r
    for i, u in enumerate(a):
        for j, v in enumerate(b):
            idx = (i + j) % r
            res[idx] = (res[idx] + u * v) % p
    
    return res


def is_congruent(a, p, r):
    """
    Tests congruence (x + a)^p mod (x^r - 1, p) == (x^p + a) mod (x^r - 1, p). 
    """
    x, poly, n = ([1], [a, 1], p)
    while n != 0:
        if n & 1:
            x = polyMult(x, poly, r, p)
        n >>= 1
        poly = polyMult(poly, poly, r, p)

    check = [0] * r
    check[0] = a 
    check[p % r] = 1

    return x == check
