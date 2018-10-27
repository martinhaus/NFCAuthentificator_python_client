from prototypes.basic_diffie import basic_diffie
from prototypes.basic_ssl import basic_ssl
import time

ssl_start = time.time()
for i in range(500):
    basic_ssl()

ssl_end = time.time()

dh_start = time.time()
for i in range(500):
    basic_diffie()

dh_end = time.time()


print("DH: " + str((dh_end - dh_start) / 500))
print("SSL: " + str((ssl_end - ssl_start) / 500))
