
from collections import namedtuple
import itertools

# 1. Take any number with >= 4 digits
# 2. decompose the number along the digits into 4 new numbers
#    without changing the sequence of digits(how? explore all possible splits)
# 3. start with the leftmost number in your decomposition and apply the following operations:
#    [-, *, /] left-to-right in whatever order produces the smallest whole positive number
# 4. If the result is 4 or more digits, repeat.

Decomp = namedtuple('Decomp', ['a', 'b', 'c', 'd'])

class Operators:
    @staticmethod
    def subtract(a: int, b: int) -> int:
        return a-b

    @staticmethod
    def multiply(a: int, b: int) -> int:
        return a * b

    @staticmethod
    def divide(a: int, b: int) -> float:
        return a / b

OP_CHOICES = [Operators.subtract, Operators.multiply, Operators.divide]
OP_PERMUTATIONS = list(itertools.permutations(OP_CHOICES))

def is_int(x) -> bool:
    return x == int(x)

def consolidate_digits(digits: list[int]) -> int:
    return int(''.join(str(d) for d in digits))

# returns a list of all possible decompositions
def decompose_digits(num: int) -> list[Decomp]:
    digits = [ int(d) for d in str(num) ]
    decompositions = []
    # we find 3 partitions within the digits, each representing one decomposition
    num_digits = len(digits)
    for i in range(1, num_digits - 2):
        for j in range(i+1, num_digits - 1):
            for k in range(j+1, num_digits):
                num1 = consolidate_digits(digits[:i])
                num2 = consolidate_digits(digits[i:j])
                num3 = consolidate_digits(digits[j:k])
                num4 = consolidate_digits(digits[k:])
                decomp = Decomp(num1,num2,num3,num4)
                decompositions.append(decomp)
    return decompositions


# 1. We always take the first integer in the decomposition
# 2. We then use one of the (-, *, /) operations incorporating each additional integer,
#    left-associating each time.
# 3 This results in 3! = 6 possible results, from which we choose the
#   smallest positive whole number.
def find_smallest_whole_arithmetic_result(decomp: Decomp) -> int:
    results = []
    for permutation in OP_PERMUTATIONS:
        first_op = permutation[0]
        second_op = permutation[1]
        third_op = permutation[2]
        try:
            result = third_op(second_op(first_op(decomp.a, decomp.b), decomp.c), decomp.d)
            # print(first_op.__name__, second_op.__name__, third_op.__name__, result)
        except ZeroDivisionError:
            result = -1
        results.append(result)
    whole_results = [int(result) for result in results if is_int(result) and result > 0]
    if len(whole_results) == 0:
        return -1
    else:
        return min(whole_results)

# This seems mostly useless
def numeric_core(num: int) -> int:
    if not is_int(num):
        return -1
    if num < 1000:
        return num
    decomps = decompose_digits(num)
    cores = []
    for decomp in decomps:
        core = find_smallest_whole_arithmetic_result(decomp)
        cores.append(core)
    valid_cores = [core for core in cores if core > 0]
    # print(valid_cores)
    return min(valid_cores)


# takes a single character string and returns a numeric value based on a normalized ordinal
def letter_value(x: str) -> int:
    return ord(x) - ord('a') + 1


# takes a 4-letter word, and maps each character to an int, before calculating its numeric core
def word_numeric_core(word: str) -> int:
    if len(word) != 4:
        return -1
    word = word.lower()
    letter_values = [letter_value(c) for c in word]
    decomp = Decomp(*letter_values)
    return find_smallest_whole_arithmetic_result(decomp)

# for d in decompose_digits(12345):
#     print(d)

# numeric_core(1000200112)

# decomp = Decomp(1000, 200, 11, 2)
# print(find_smallest_whole_arithmetic_result(decomp))
words = [
    'pigs', 'sand', 'mail', 'date', 'head',
    'clam', 'peak', 'heat', 'joya', 'well',
    'toad', 'card', 'will', 'tape', 'legs',
    'tree', 'road', 'maid', 'slab', 'rock',
    'hand', 'vase', 'safe', 'clay', 'toes'
]
for word in words:
    # print(word_numeric_core(word))
    print(chr(word_numeric_core(word) + ord('a') - 1))
