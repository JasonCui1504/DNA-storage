# add_primers.py

FORWARD_PRIMER = "CGTAGCTAGTCGATCGTAGC"
REVERSE_PRIMER = "GCATCGTAGCTAGTCGATGC"

def add_primers(oligo):
    full_sequence = FORWARD_PRIMER + oligo + REVERSE_PRIMER
    return full_sequence

def remove_primers(full_sequence):
    forward_length = len(FORWARD_PRIMER)
    reverse_length = len(REVERSE_PRIMER)

    # strip the forward primer from the front
    # strip the reverse primer from the back
    oligo = full_sequence[forward_length : len(full_sequence) - reverse_length]
    return oligo

def main():
    print("=== Primer Addition Tool ===")
    print()
    print("Forward primer: " + FORWARD_PRIMER)
    print("Reverse primer: " + REVERSE_PRIMER)
    print()

    print("What would you like to do?")
    print("1 - Add primers to an oligo")
    print("2 - Remove primers from a full sequence")
    choice = input("Enter 1 or 2: ")

    print()

    if choice == '1':
        oligo = input("Enter your encoded oligo: ")
        full_sequence = add_primers(oligo)

        print()
        print("Forward primer:  " + FORWARD_PRIMER)
        print("Encoded message: " + oligo)
        print("Reverse primer:  " + REVERSE_PRIMER)
        print()
        print("Full sequence to order: " + full_sequence)
        print("Total length: " + str(len(full_sequence)) + " nt")

    elif choice == '2':
        full_sequence = input("Enter your full sequence: ")
        oligo = remove_primers(full_sequence)

        print()
        print("Encoded oligo: " + oligo)
        print("Oligo length:  " + str(len(oligo)) + " nt")

    else:
        print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()