"""Tests for Hamming (7,4) encode/decode behavior."""

from __future__ import annotations

import itertools

import pytest

from qkd_odcn.hamming import DecodeResult, decode, encode


@pytest.mark.parametrize("data", itertools.product([0, 1], repeat=4))
def test_all_messages_roundtrip_cleanly(data: tuple[int, int, int, int]) -> None:
    message = list(data)
    result = decode(encode(message))
    assert result.data == message
    assert result.corrected is False
    assert result.error_position is None
    assert result.syndrome == (0, 0, 0)


@pytest.mark.parametrize("data", itertools.product([0, 1], repeat=4))
@pytest.mark.parametrize("error_index", range(7))
def test_all_single_bit_errors_are_corrected(
    data: tuple[int, int, int, int],
    error_index: int,
) -> None:
    message = list(data)
    codeword = encode(message)
    codeword[error_index] ^= 1
    result = decode(codeword)
    assert result.data == message
    assert result.corrected is True
    assert result.error_position == error_index + 1
    assert result.syndrome != (0, 0, 0)


@pytest.mark.parametrize("invalid", [[0, 1, 0], [0, 1, 0, 1, 0]])
def test_invalid_message_lengths_raise(invalid: list[int]) -> None:
    with pytest.raises(ValueError):
        encode(invalid)


@pytest.mark.parametrize("invalid", [[0, 1, 2, 0], [0, -1, 1, 0]])
def test_invalid_message_bits_raise(invalid: list[int]) -> None:
    with pytest.raises(ValueError):
        encode(invalid)


@pytest.mark.parametrize("invalid", [[0, 1, 0, 1, 0, 1], [0, 1, 0, 1, 0, 1, 0, 1]])
def test_invalid_codeword_lengths_raise(invalid: list[int]) -> None:
    with pytest.raises(ValueError):
        decode(invalid)


@pytest.mark.parametrize("invalid", [[0, 1, 0, 1, 0, 1, 2], [0, 1, 0, 1, 0, 1, -1]])
def test_invalid_codeword_bits_raise(invalid: list[int]) -> None:
    with pytest.raises(ValueError):
        decode(invalid)


def test_double_bit_error_behavior_is_not_overclaimed() -> None:
    message = [1, 1, 0, 0]
    codeword = encode(message)
    codeword[0] ^= 1
    codeword[1] ^= 1
    result = decode(codeword)
    assert isinstance(result, DecodeResult)
    assert result.syndrome != (0, 0, 0)
