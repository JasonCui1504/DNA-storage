import sys

import requests
import xml.etree.ElementTree as ET

from converting_text_to_base import text_to_dna, dna_to_text, CHARSET
from error_correcting_reed_solomon import encode_with_reed_solomon, decode_with_reed_solomon

def validate_oligo(dna_sequence):
    url = "https://www.idtdna.com/AnalyzerService/AnalyzerService.asmx/Analyze"

    params = {
        "Sequence":   dna_sequence,
        "TargetType": "DNA",
        "OligoConc":  "0.25",
        "NaConc":     "50",
        "MgConc":     "0",
        "dNTPsConc":  "0"
    }

    response = requests.get(url, params=params)

    # parse the XML response
    namespace = "http://services.idtdna.com/"
    root = ET.fromstring(response.text)

    gc_content    = root.find(f"{{{namespace}}}GCPctg").text
    melt_temp     = root.find(f"{{{namespace}}}MeltTemp").text
    length        = root.find(f"{{{namespace}}}SequenceLength").text
    has_errors    = root.find(f"{{{namespace}}}HasErrors").text
    errors        = root.find(f"{{{namespace}}}Errors").text

    print("Oligo length: " + length + " nt")
    print("GC content:   " + gc_content + "%")
    print("Melting temp: " + melt_temp + " C")

    # warn if GC is outside the safe range
    gc = float(gc_content)
    if gc < 40:
        print("WARNING: GC content is too low (want 40-60%)")
    elif gc > 60:
        print("WARNING: GC content is too high (want 40-60%)")
    else:
        print("GC content: OK")

    if has_errors == "true":
        print("IDT ERROR: " + errors)
    else:
        print("No errors reported by IDT")

def check_homopolymers(dna_sequence):
    max_run = 1
    current_run = 1
    worst_base = dna_sequence[0]
    worst_position = 0

    i = 1
    while i < len(dna_sequence):
        if dna_sequence[i] == dna_sequence[i - 1]:
            current_run = current_run + 1
            if current_run > max_run:
                max_run = current_run
                worst_base = dna_sequence[i]
                worst_position = i - current_run + 1
        else:
            current_run = 1
        i = i + 1

    print("Longest homopolymer run: " + str(max_run) + " (" + worst_base + " at position " + str(worst_position) + ")")

    if max_run >= 4:
        print("WARNING: homopolymer run of " + str(max_run) + " detected — may cause synthesis errors")
        return 1
    else:
        print("Homopolymer runs: OK")
        return 0

def main():
    input_message = input("Enter a message to encode: ")
    oligo = text_to_dna(input_message)
    print("Oligo: " + oligo)

    print()
    print("Validating oligo quality with IDT OligoAnalyzer...")
    validate_oligo(oligo)
    print()
    print("Validating homopolymer quality ...")
    homopolymers = check_homopolymers(oligo)
    if homopolymers == 1:
        print("Holomopolymer warning. Will re-encode with Reed-Solomon error correction!")
        oligo = encode_with_reed_solomon(input_message)
        print("New oligo: " + oligo)
        print("New oligo length: " + str(len(oligo)) + " nt")
        print()

        print("Re-validating oligo quality ...")
        validate_oligo(oligo)
    else:
        print()
        print("Oligo passed all checks — ready to order!")

if __name__ == "__main__":
    main()