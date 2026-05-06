# DNA Text Encoder

Converts English text into a DNA sequence and back. Built for real oligo synthesis and sequencing.

---

## How it works

Each character in your message maps to 3 DNA bases. The encoder tries different character arrangements until it finds a sequence that is safe to synthesize. The sequence is then validated using IDT's OligoAnalyzer API before you order.

---

## Files

**converting_text_to_base.py**
The core encoder and decoder. Run this to convert text to DNA or DNA back to text.

**verify_dna_quality.py**
Checks the oligo for GC content and homopolymer runs. Calls the IDT API automatically.

**rotational_encoder.py**
The main script to use. Finds an encoding that passes all biological checks. Run this first.

**error_correcting_reed_solomon.py**
Adds error correction so that sequencing mistakes can be recovered. Use this if your sequencing result comes back with errors.

---

## How to run

```bash
python rotational_encoder.py
```

Enter your message, and it will return a validated DNA sequence ready to order.

---

## Requirements

```bash
pip install requests reedsolo
```
