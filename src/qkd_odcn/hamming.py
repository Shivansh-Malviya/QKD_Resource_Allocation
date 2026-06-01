"""
Hamming (7,4) error-correction utilities.

This module implements basic encoding and decoding functions for the Hamming
(7,4) code. It can correct single-bit errors in a 7-bit codeword. It does not
reliably detect multiple-bit errors. When the syndrome is nonzero, the decoder
flips the bit indicated by that syndrome, which is only guaranteed to be valid
for a single-bit error.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Tuple

# Generator matrix for Hamming (7,4) in systematic form.
G = [
    [1, 0, 0, 0, 1, 1, 0],
    [0, 1, 0, 0, 1, 0, 1],
    [0, 0, 1, 0, 0, 1, 1],
    [0, 0, 0, 1, 1, 1, 1],
]

# Parity-check matrix for Hamming (7,4).
H = [
    [1, 1, 0, 1, 1, 0, 0],
    [1, 0, 1, 1, 0, 1, 0],
    [0, 1, 1, 1, 0, 0, 1],
]

SYNDROME_TO_POSITION = {
    tuple(H[row][column] for row in range(3)): column + 1
    for column in range(7)
}


@dataclass(frozen=True)
class DecodeResult:
    """Structured result returned by :func:`decode`.

    Attributes
    ----------
    data:
        Decoded 4-bit message.
    corrected:
        Whether the decoder flipped one bit in response to a nonzero syndrome.
    error_position:
        One-based position of the flipped bit, or ``None`` when no syndrome was
        observed.
    syndrome:
        Three-bit syndrome tuple.
    """

    data: List[int]
    corrected: bool
    error_position: Optional[int]
    syndrome: Tuple[int, int, int]


def _validate_bits(bits: List[int], expected_length: int, name: str) -> None:
    if len(bits) != expected_length:
        raise ValueError(f"{name} must be a list of {expected_length} bits (0/1)")
    if any(bit not in (0, 1) for bit in bits):
        raise ValueError(f"{name} must contain only bits (0/1)")


def encode(data: List[int]) -> List[int]:
    """Encode 4 data bits into a 7-bit Hamming codeword.

    Raises
    ------
    ValueError
        If ``data`` is not exactly four bits.
    """
    _validate_bits(data, 4, "data")
    codeword = [0] * 7
    for i in range(4):
        for j in range(7):
            codeword[j] ^= data[i] * G[i][j]
    return [bit % 2 for bit in codeword]


def syndrome(codeword: List[int]) -> List[int]:
    """Compute the syndrome of a 7-bit codeword.

    ``[0, 0, 0]`` indicates no observed syndrome. A nonzero syndrome is only a
    reliable locator for a single-bit error in standard Hamming (7,4).
    """
    _validate_bits(codeword, 7, "codeword")
    values = [0, 0, 0]
    for i in range(3):
        for j in range(7):
            values[i] ^= codeword[j] * H[i][j]
        values[i] %= 2
    return values


def decode(codeword: List[int]) -> DecodeResult:
    """Decode a 7-bit Hamming codeword.

    The decoder corrects single-bit errors. Multiple-bit errors are not
    reliably detected by this implementation. A nonzero syndrome causes the
    corresponding bit to be flipped, which may be wrong for multi-bit errors.
    """
    observed_syndrome = syndrome(codeword)
    error_position: Optional[int] = None
    corrected = False
    decoded = codeword.copy()

    if observed_syndrome != [0, 0, 0]:
        error_position = SYNDROME_TO_POSITION.get(tuple(observed_syndrome))
        if error_position is None:
            raise ValueError("computed syndrome maps outside the 7-bit codeword")
        decoded[error_position - 1] ^= 1
        corrected = True

    return DecodeResult(
        data=decoded[:4],
        corrected=corrected,
        error_position=error_position,
        syndrome=tuple(observed_syndrome),
    )
