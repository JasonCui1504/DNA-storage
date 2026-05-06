from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from rotational_encoder import find_clean_oligo, decode_oligo, check_gc
from verify_dna_quality import check_homopolymers

import io
import sys

app = FastAPI(title="DNA Rotational Encoder API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)


class EncodeRequest(BaseModel):
    text: str

class DecodeRequest(BaseModel):
    oligo: str


@app.post("/encode")
def encode(req: EncodeRequest):
    if not req.text:
        raise HTTPException(status_code=400, detail="text is required")

    # suppress print output from find_clean_oligo
    captured = io.StringIO()
    sys.stdout = captured
    try:
        oligo, shift = find_clean_oligo(req.text)
    finally:
        sys.stdout = sys.__stdout__

    if oligo is None:
        raise HTTPException(
            status_code=422,
            detail="No clean encoding found across all 64 rotations for this input."
        )

    gc = check_gc(oligo)

    # compute max homopolymer run inline (avoid print side effects)
    max_run = 1
    current_run = 1
    for i in range(1, len(oligo)):
        if oligo[i] == oligo[i - 1]:
            current_run += 1
            if current_run > max_run:
                max_run = current_run
        else:
            current_run = 1

    return {
        "oligo": oligo,
        "shift": shift,
        "gc": gc,
        "max_run": max_run,
        "length": len(oligo),
    }


@app.post("/decode")
def decode(req: DecodeRequest):
    oligo = req.oligo.strip().upper()
    if not oligo:
        raise HTTPException(status_code=400, detail="oligo is required")
    if len(oligo) < 6 or len(oligo) % 3 != 0:
        raise HTTPException(status_code=400, detail="Sequence must be at least 6 bases and a multiple of 3.")

    valid_bases = set("ACGT")
    for base in oligo:
        if base not in valid_bases:
            raise HTTPException(status_code=400, detail=f"Invalid base '{base}' — only A, C, G, T allowed.")

    captured = io.StringIO()
    sys.stdout = captured
    try:
        text = decode_oligo(oligo)
    finally:
        sys.stdout = sys.__stdout__

    return {"text": text}


@app.get("/health")
def health():
    return {"status": "ok"}
