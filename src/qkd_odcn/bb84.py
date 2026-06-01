"""
Simplified BB84 key generation utilities.

These functions implement a highly simplified version of the BB84 protocol
sufficient to illustrate raw-key generation and basic noise effects. This
module supports simulation context and does not implement a deployable QKD
protocol.
"""

from __future__ import annotations

import random
from typing import List, Tuple


def generate_raw_key(n: int) -> Tuple[List[int], List[int]]:
    """Generate ``n`` random bits and corresponding random bases."""
    bits = [random.randint(0, 1) for _ in range(n)]
    bases = [random.randint(0, 1) for _ in range(n)]
    return bits, bases


def measure(
    bits: List[int],
    sender_bases: List[int],
    receiver_bases: List[int],
    noise: float = 0.0,
) -> List[int]:
    """Simulate BB84 measurement with optional bit-flip noise."""
    measured = []
    for bit_value, sender_basis, receiver_basis in zip(
        bits,
        sender_bases,
        receiver_bases,
    ):
        if sender_basis == receiver_basis:
            measured_bit = bit_value
        else:
            measured_bit = random.randint(0, 1)
        if noise > 0.0 and random.random() < noise:
            measured_bit ^= 1
        measured.append(measured_bit)
    return measured


def sift_keys(
    bits: List[int],
    sender_bases: List[int],
    receiver_bases: List[int],
    measured: List[int],
) -> Tuple[List[int], List[int]]:
    """Return sender and receiver bits where bases matched."""
    sender_key = []
    receiver_key = []
    for bit_value, sender_basis, receiver_basis, measured_bit in zip(
        bits,
        sender_bases,
        receiver_bases,
        measured,
    ):
        if sender_basis == receiver_basis:
            sender_key.append(bit_value)
            receiver_key.append(measured_bit)
    return sender_key, receiver_key


def key_error_rate(sender_key: List[int], receiver_key: List[int]) -> float:
    """Compute the mismatch fraction between two sifted keys."""
    assert len(sender_key) == len(receiver_key)
    if not sender_key:
        return 0.0
    mismatches = sum(1 for a, b in zip(sender_key, receiver_key) if a != b)
    return mismatches / len(sender_key)
