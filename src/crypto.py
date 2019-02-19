"""
The server is assumed secure, and only the client needs to be authenticated.
Authentication is based on the challenge/response mechanism, used in cellular networks.
Upon receiving HELLO (Client-ID-A), the server looks up Client A’s secret key K_A.
Then it generates a random number rand. Rand and K_A are input into an authentication algorithm A3.
The output, XRES, is stored by the server. Then the server sends rand in the CHALLENGE (rand).
Client A is expected to run the same algorithm A3 with the same inputs rand and K_A, and produce RES, which is sent to the server in the RESPONSE (Res) message.
If RES matches XRES, the server has authenticated the client. For this assignment, use a hash function for algorithm A3: RES = hash1(rand + K_A), where + denotes concatenation.
Examples are MD5, SHA1, SHA256 etc.
"""

import hashlib
from os import urandom


def cRandom(bytes=512):
    """Cryptographic random number generator

    Returns:
        hex: Cryptographically secure random number
    """
    return urandom(bytes).hex()
    raise NotImplementedError


# Don't implement a version of a3 that subcalls cryptographicRandom,
# it's not helpful for this project.


def a3(rand, secret):
    """A3 authentnication algorithm

    Args:
        rand (int): Random
        secret (int): Client secret

    Returns:
        hexdigest: XRES 
    """
    r = hashlib.sha256()
    r.update(repr(rand).encode('utf-8'))
    r.update(repr(secret).encode('utf-8'))
    return r.hexdigest()
