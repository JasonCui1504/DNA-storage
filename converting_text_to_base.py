# 64 = 4^3, so each character encodes to exactly 3 DNA bases
CHARSET = [
    ' ',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '.', ',', '!', '?', '-', '\'', '"', ':', ';', '(', ')'
]

# The four DNA bases and their number equivalents
NUM_TO_BASE = {
    0: 'A',
    1: 'C',
    2: 'G',
    3: 'T'
}

BASE_TO_NUM = {
    'A': 0,
    'C': 1,
    'G': 2,
    'T': 3
}


def text_to_dna(text):
    dna = ''

    for char in text:
        if char not in CHARSET:
            raise ValueError(f"'{char}' is not an allowed character")

        n = CHARSET.index(char)

        first  = n // 16
        second = (n // 4) % 4
        third  = n % 4

        base1 = NUM_TO_BASE[first]
        base2 = NUM_TO_BASE[second]
        base3 = NUM_TO_BASE[third]

        dna = dna + base1 + base2 + base3

    print("Encoded length: " + str(len(dna)))
    print("Input length:   " + str(len(text)))
    print("Expected nt:    " + str(len(text) * 3))
    return dna


def dna_to_text(dna):
    text = ''
    dna = dna.strip() # removes whitespace from the start and end of the string
    print("Input length: " + str(len(dna)))
    print("Input is: '" + dna + "'")

    if len(dna) % 3 != 0:
        print("Error: length " + str(len(dna)) + " is not divisible by 3")
        return ''


    i = 0
    while i < len(dna):
        base1 = dna[i]
        base2 = dna[i + 1]
        base3 = dna[i + 2]

        num1 = BASE_TO_NUM[base1]
        num2 = BASE_TO_NUM[base2]
        num3 = BASE_TO_NUM[base3]

        n = (num1 * 16) + (num2 * 4) + num3

        char = CHARSET[n]
        text = text + char

        i = i + 3

    return text

def main():
    # inputs
    print("What would you like to do?")
    print("1 - Encode text to DNA")
    print("2 - Decode DNA to text")
    choice = input("Enter 1 or 2: ")

    print()

    if choice == '1':
        message = input("Enter your message: ")
        oligo = text_to_dna(message)

        print("DNA oligo: " + oligo)
        print("Oligo length: " + str(len(oligo)) + " nt")

    elif choice == '2':
        oligo = input("Enter your DNA sequence: ")
        message = dna_to_text(oligo)
        print()
        print("Decoded message: " + message)

    else:
        print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()