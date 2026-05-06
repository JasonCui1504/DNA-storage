import reedsolo
from converting_text_to_base import CHARSET, NUM_TO_BASE, BASE_TO_NUM


# number of redundancy bytes — can correct up to REDUNDANCY/2 errors
REDUNDANCY = 8

def encode_with_reed_solomon(text):
    # convert text to bytes
    message_bytes = []
    for char in text:
        if char not in CHARSET:
            raise ValueError(f"'{char}' is not an allowed character")
        message_bytes.append(CHARSET.index(char))

    # apply Reed-Solomon
    rs = reedsolo.RSCodec(REDUNDANCY)
    protected_bytes = list(rs.encode(message_bytes))

    print("Original bytes:  " + str(len(message_bytes)))
    print("Protected bytes: " + str(len(protected_bytes)))

    # encode to DNA using 4 bases per byte (handles values 0-255)
    dna = ''
    for n in protected_bytes:
        first  = n // 64
        second = (n // 16) % 4
        third  = (n // 4) % 4
        fourth = n % 4

        base1 = NUM_TO_BASE[first]
        base2 = NUM_TO_BASE[second]
        base3 = NUM_TO_BASE[third]
        base4 = NUM_TO_BASE[fourth]

        dna = dna + base1 + base2 + base3 + base4

    return dna


def decode_with_reed_solomon(dna):
    dna = dna.strip()

    # decode DNA using 4 bases per byte
    protected_bytes = []
    i = 0
    while i < len(dna):
        base1 = dna[i]
        base2 = dna[i + 1]
        base3 = dna[i + 2]
        base4 = dna[i + 3]

        num1 = BASE_TO_NUM[base1]
        num2 = BASE_TO_NUM[base2]
        num3 = BASE_TO_NUM[base3]
        num4 = BASE_TO_NUM[base4]

        n = (num1 * 64) + (num2 * 16) + (num3 * 4) + num4
        protected_bytes.append(n)

        i = i + 4

    # apply Reed-Solomon correction
    rs = reedsolo.RSCodec(REDUNDANCY)
    try:
        corrected_bytes, _, _ = rs.decode(protected_bytes)
        print("Reed-Solomon: no errors, or errors corrected successfully")
    except reedsolo.ReedSolomonError:
        print("Reed-Solomon: too many errors to correct")
        return ''

    # convert corrected bytes back to text
    text = ''
    for n in corrected_bytes:
        text = text + CHARSET[n]

    return text