"""
Q1 - Error Detection & Correction: "Catch the Corrupted Message"

Simulates sending a short text message over a noisy channel and detects
whether it got corrupted, using two methods:
  1. A single parity bit (even parity)
  2. A checksum (sum of ASCII character codes)

Run:
    python error_detection.py
"""

import random


# ---------------------------------------------------------------------
# 1. Convert text to binary
# ---------------------------------------------------------------------
def text_to_binary(message: str) -> str:
    """Convert a string into a single string of 8-bit binary chunks."""
    return "".join(format(ord(ch), "08b") for ch in message)


def binary_to_text(binary: str) -> str:
    """Convert a binary string (multiple of 8 bits) back into text."""
    chars = [binary[i:i + 8] for i in range(0, len(binary), 8)]
    return "".join(chr(int(b, 2)) for b in chars)


# ---------------------------------------------------------------------
# 2. Parity bit
# ---------------------------------------------------------------------
def calculate_parity_bit(binary: str, mode: str = "even") -> str:
    """
    Calculate a single parity bit for a binary string.
    Even parity -> total number of 1s (including parity bit) is even.
    Odd parity  -> total number of 1s (including parity bit) is odd.
    """
    ones = binary.count("1")
    if mode == "even":
        return "0" if ones % 2 == 0 else "1"
    else:  # odd parity
        return "1" if ones % 2 == 0 else "0"


def check_parity(binary: str, received_parity_bit: str, mode: str = "even") -> bool:
    """Return True if the message is still consistent with its parity bit."""
    expected_parity_bit = calculate_parity_bit(binary, mode)
    return expected_parity_bit == received_parity_bit


# ---------------------------------------------------------------------
# 3. Checksum (sum of character codes)
# ---------------------------------------------------------------------
def calculate_checksum(message: str) -> int:
    """Simple checksum: sum of ASCII codes of every character, mod 256."""
    return sum(ord(ch) for ch in message) % 256


def check_checksum(message: str, received_checksum: int) -> bool:
    return calculate_checksum(message) == received_checksum


# ---------------------------------------------------------------------
# 4. Simulate noise: flip one random bit
# ---------------------------------------------------------------------
def flip_random_bit(binary: str) -> str:
    """Flip exactly one random bit in a binary string and return the result."""
    bit_list = list(binary)
    pos = random.randint(0, len(bit_list) - 1)
    bit_list[pos] = "1" if bit_list[pos] == "0" else "0"
    return "".join(bit_list)


def generate_noisy_messages(message: str, count: int = 5):
    """
    Build `count` test cases from the same original message.
    Each test case simulates transmission noise by flipping one random
    bit in the *binary payload* before it reaches the receiver.
    Returns a list of dicts with everything needed to check both methods.
    """
    original_binary = text_to_binary(message)
    original_parity = calculate_parity_bit(original_binary, mode="even")
    original_checksum = calculate_checksum(message)

    test_cases = []
    for i in range(count):
        corrupted_binary = flip_random_bit(original_binary)
        corrupted_text = binary_to_text(corrupted_binary)
        test_cases.append({
            "id": i + 1,
            "corrupted_binary": corrupted_binary,
            "corrupted_text": corrupted_text,
            "received_parity_bit": original_parity,   # parity bit travels unchanged
            "received_checksum": original_checksum,   # checksum travels unchanged
        })
    return test_cases


# ---------------------------------------------------------------------
# 5. Main demo
# ---------------------------------------------------------------------
def main():
    random.seed()  # remove/replace with a fixed number for reproducible output
    message = "HELLO"
    print(f"Original message: {message!r}")
    print(f"Binary payload:   {text_to_binary(message)}")
    print(f"Even parity bit:  {calculate_parity_bit(text_to_binary(message))}")
    print(f"Checksum:         {calculate_checksum(message)}")
    print("-" * 70)

    test_cases = generate_noisy_messages(message, count=5)

    parity_catches = 0
    checksum_catches = 0

    header = f"{'#':<3}{'Corrupted Text':<20}{'Parity Check':<20}{'Checksum Check':<20}"
    print(header)
    print("-" * len(header))

    for case in test_cases:
        parity_ok = check_parity(case["corrupted_binary"],
                                  case["received_parity_bit"], mode="even")
        checksum_ok = check_checksum(case["corrupted_text"],
                                      case["received_checksum"])

        parity_result = "OK" if parity_ok else "ERROR DETECTED"
        checksum_result = "OK" if checksum_ok else "ERROR DETECTED"

        if not parity_ok:
            parity_catches += 1
        if not checksum_ok:
            checksum_catches += 1

        # corrupted_text may contain non-printable characters; show safely
        safe_text = case["corrupted_text"].encode("unicode_escape").decode()

        print(f"{case['id']:<3}{safe_text:<20}{parity_result:<20}{checksum_result:<20}")

    print("-" * len(header))
    print(f"Parity method caught:   {parity_catches}/5 corrupted messages")
    print(f"Checksum method caught: {checksum_catches}/5 corrupted messages")


if __name__ == "__main__":
    main()
