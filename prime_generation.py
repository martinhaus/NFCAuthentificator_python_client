import json
from Encryption import generatePrime


def generate_primes_with_root_modulos(count, prime_size):
    primes = []

    for i in range(count):
        primes.append({'prime': generatePrime(prime_size), 'root': 2})

    with open('primes.json', 'w') as outfile:
        json.dump(primes, outfile)
