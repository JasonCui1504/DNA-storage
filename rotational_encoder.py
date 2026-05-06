from converting_text_to_base import CHARSET, NUM_TO_BASE, BASE_TO_NUM
from verify_dna_quality import validate_oligo, check_homopolymers


def rotate_charset(shift):
    rotated = []
    i = 0
    while i < len(CHARSET):
        index = (i + shift) % len(CHARSET)
        rotated.append(CHARSET[index])
        i = i + 1
    return rotated


def shift_to_header(shift):
    # encode the shift number as 3 DNA bases so decoder knows which rotation was used
    first  = shift // 16
    second = (shift // 4) % 4
    third  = shift % 4

    base1 = NUM_TO_BASE[first]
    base2 = NUM_TO_BASE[second]
    base3 = NUM_TO_BASE[third]

    return base1 + base2 + base3


def header_to_shift(header):
    # decode the 3 base header back to a shift number
    num1 = BASE_TO_NUM[header[0]]
    num2 = BASE_TO_NUM[header[1]]
    num3 = BASE_TO_NUM[header[2]]

    return (num1 * 16) + (num2 * 4) + num3


def encode_with_rotation(text, shift):
    rotated_charset = rotate_charset(shift)
    dna = ''

    for char in text:
        if char not in rotated_charset:
            raise ValueError(f"'{char}' is not an allowed character")

        n = rotated_charset.index(char)

        first  = n // 16
        second = (n // 4) % 4
        third  = n % 4

        base1 = NUM_TO_BASE[first]
        base2 = NUM_TO_BASE[second]
        base3 = NUM_TO_BASE[third]

        dna = dna + base1 + base2 + base3

    return dna


def decode_with_rotation(dna, shift):
    rotated_charset = rotate_charset(shift)
    text = ''

    i = 0
    while i < len(dna):
        base1 = dna[i]
        base2 = dna[i + 1]
        base3 = dna[i + 2]

        num1 = BASE_TO_NUM[base1]
        num2 = BASE_TO_NUM[base2]
        num3 = BASE_TO_NUM[base3]

        n = (num1 * 16) + (num2 * 4) + num3
        text = text + rotated_charset[n]

        i = i + 3

    return text


def check_gc(dna):
    g_count = dna.count('G')
    c_count = dna.count('C')
    gc = (g_count + c_count) / len(dna) * 100
    return round(gc, 1)


def find_clean_oligo(text):
    print("Searching for a clean encoding across 64 rotations...")
    print()

    shift = 0
    while shift < 64:
        candidate = encode_with_rotation(text, shift)
        header    = shift_to_header(shift)
        oligo     = header + candidate

        # use check_homopolymers from verify_dna_quality but suppress its print
        # by doing the run check inline for the search loop
        max_run     = 1
        current_run = 1
        i = 1
        while i < len(oligo):
            if oligo[i] == oligo[i - 1]:
                current_run = current_run + 1
                if current_run > max_run:
                    max_run = current_run
            else:
                current_run = 1
            i = i + 1

        gc = check_gc(oligo)

        print("Shift " + str(shift) + ": GC=" + str(gc) + "%, longest run=" + str(max_run))

        if max_run <= 3 and gc >= 40 and gc <= 60:
            print()
            print("Clean oligo found at shift " + str(shift) + "!")
            return oligo, shift

        shift = shift + 1

    print("No clean encoding found across all 64 rotations.")
    return None, None


def decode_oligo(oligo):
    # first 3 bases are the header encoding the shift
    header  = oligo[0:3]
    payload = oligo[3:]

    shift = header_to_shift(header)
    print("Detected rotation shift: " + str(shift))

    text = decode_with_rotation(payload, shift)
    return text


def main():
    print("Rotational DNA Encoder")
    print()

    print("What would you like to do?")
    print("1 - Encode text to DNA")
    print("2 - Decode DNA to text")
    choice = input("Enter 1 or 2: ")

    print()

    if choice == '1':
        message = input("Enter your message: ")
        oligo, shift = find_clean_oligo(message)

        if oligo is not None:
            print("Final oligo:  " + oligo)
            print("Oligo length: " + str(len(oligo)) + " nt")
            print("GC content:   " + str(check_gc(oligo)) + "%")
            print()
            print("Final validation with IDT OligoAnalyzer...")
            validate_oligo(oligo)
            print()
            print("Final homopolymer check...")
            check_homopolymers(oligo)
        else:
            print("Could not find a clean oligo for this message.")

    elif choice == '2':
        oligo = input("Enter your DNA sequence: ")
        message = decode_oligo(oligo)
        print()
        print("Decoded message: " + message)

    else:
        print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()