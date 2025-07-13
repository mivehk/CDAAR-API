from flask_openapi3 import OpenAPI, Info, Tag
from flask import jsonify
from pydantic import BaseModel, Field, validator

# here is how i installed some of the openapi UI on zsh venv
# `python3 -m pip install -U "flask-openapi3[swagger,redoc,rapidoc,rapipdf,scalar,elements]"`
# Second run i had to uninstall+install pydantic on my venv

info = Info(title="Central Dogma Transcription API", version="2.0.1")
app = OpenAPI(__name__, info=info)


class RNAQuery(BaseModel):
    seq: str = Field(
        ..., pattern="^[ATGCatgc]+$", description="DNA sequence with only A, T, G and C"
    )

    @validator("seq")
    def check_length(cls, v):
        if len(v) > 10000:
            raise ValueError("Sequence must be 10000 nucleotides or fewer")
        return v


class DNAQuery(BaseModel):
    seq: str = Field(
        ..., pattern="^[ATGCatgc]+$", description="DNA sequence with only A, T, G and C"
    )

    @validator("seq")
    def check_length(cls, v):
        if len(v) > 10000:
            raise ValueError("Sequence must be 10000 nucleotides or fewer")
        return v


class CDNAQuery(BaseModel):
    seq: str = Field(
        ..., pattern="^[AUGCaugc]+$", description="RNA sequence with only A, U, G and C"
    )

    @validator("seq")
    def check_length(cls, v):
        if len(v) > 10000:
            raise ValueError("Sequence must be 10000 nucleotides or fewer")
        return v


class Translation(BaseModel):
    seq: str = Field(
        ...,
        pattern="^[AUGCaugc]+$",
        description="mRNA sequence with only A, U, G and C",
    )

    @validator("seq")
    def check_length(cls, v):
        if len(v) > 10000:
            raise ValueError(
                "Sequence must have less than or equal to 10000 nucleotide"
            )
        return v


rna_tag = Tag(
    name="RNA Transcription from the Reverse Complement of a DNA Sequence",
    description="DNA Transcription to mRNA",
)
dna_tag = Tag(
    name="Reverse Complement of a DNA Coding Sequence",
    description="Reverse Complement of a DNA Coding Sequence",
)
cdna_tag = Tag(
    name="The Complementary Double Stranded DNA from mRNA", description="mRNA to cDNA"
)
aminoacid_tag = Tag(
    name="Polypeptide chain comprised of peptide links of amino-acids translated from mRNA",
    description="mRNA to Polypeptide Chain",
)


# 5’-ATGC-3’ in a double stranded DNA has a complement 3’-TACG-5’
# RNA Polymerase enzyme only transcribe 5-to-3 so uses template strand 3’-TACG-5’ for transcription of ’5-AUGC-3’
# *** here’s the catch ***
# in genomics, we often label the DNA’s coding strand (5’-ATGC-3’) which is the non-template strand,
def get_rna_transcription(sequence):
    transcribe = {"A": "U", "T": "A", "G": "C", "C": "G"}
    complement = {"A": "T", "T": "A", "G": "C", "C": "G"}
    sequence = sequence.upper()
    comp_seq = "".join(complement.get(b, b) for b in sequence)
    transcribed_seq = "".join(transcribe.get(b, b) for b in comp_seq)
    pre_mRNA = " 5'-" + transcribed_seq + "-3' "
    return pre_mRNA


# 5’-ATGC-3’ split with DNA_polymerase (its original complement strand was 3’-TACG-5’)
# However, technically strands starts with 5 and DNA polymerase can only synthesize DNA in the 5' to 3' direction
# Therefore, to depict this antisense DNA strand from 5-to-3 (left-to-right) we perform reverse complement
# first we need the reverse of coding strand which is 3’-CGTA-5’
# then we have its complement 5’-GCAT-3’ - Now look at the last sequence in first comment line
def get_dna_template_strand(sequence):
    complement = {"A": "T", "T": "A", "G": "C", "C": "G"}
    sequence = sequence.upper()
    rev_seq = sequence[::-1]
    pair_seq = "".join(complement.get(b, b) for b in rev_seq)
    revcomp_seq = " 5'-" + pair_seq + "-3' "
    return revcomp_seq


# If we have a mRNA sequence 5’-AUGC-3’ then reverse transcriptase enzyme synthesize single stranded 3’-TACG-5’
# Starting from the 5 prime the complementary double stranded DNA would be 5’-ATGC-3’ and 3'-TACG-5'
def get_complementary_dna(sequence):
    Reverse_Transcribe = {"U": "A", "A": "T", "G": "C", "C": "G"}
    complement = {"A": "T", "T": "A", "G": "C", "C": "G"}
    sequence = sequence.upper()
    Rev_Complementary_DNA = "".join(Reverse_Transcribe.get(b, b) for b in sequence)
    # second b is the default value for any sequence letter that is not found in dictionary
    # Complementary_DNA = Rev_Complementary_DNA[::-1]
    CDNA = "".join(complement.get(b, b) for b in Rev_Complementary_DNA)
    Complementary_DNA = (
        " 5'-" + CDNA + "-3' paired with " + "3'-" + Rev_Complementary_DNA + "-5' "
    )
    return Complementary_DNA


def get_translate_mrna(mrna_sequence):
    codon_translation = {
        "UUU": "Phenylalanine",
        "UUC": "Phenylalanine",
        "UUA": "Leucine",
        "UUG": "Leucine",
        "CUU": "Leucine",
        "CUC": "Leucine",
        "CUA": "Leucine",
        "CUG": "Leucine",
        "AUU": "Isoleucine",
        "AUC": "Isoleucine",
        "AUA": "Isoleucine",
        "AUG": "Methionine",
        "GUU": "Valine",
        "GUC": "Valine",
        "GUA": "Valine",
        "GUG": "Valine",
        "UCU": "Serine",
        "UCC": "Serine",
        "UCA": "Serine",
        "UCG": "Serine",
        "CCU": "Proline",
        "CCC": "Proline",
        "CCA": "Proline",
        "CCG": "Proline",
        "ACU": "Threonine",
        "ACC": "Threonine",
        "ACA": "Threonine",
        "ACG": "Threonine",
        "GCU": "Alanine",
        "GCC": "Alanine",
        "GCA": "Alanine",
        "GCG": "Alanine",
        "UAU": "Tyrosine",
        "UAC": "Tyrosine",
        "UAA": "Stop",
        "UAG": "Stop",
        "CAU": "Histidine",
        "CAC": "Histidine",
        "CAA": "Glutamine",
        "CAG": "Glutamine",
        "AAU": "Asparagine",
        "AAC": "Asparagine",
        "AAA": "Lysine",
        "AAG": "Lysine",
        "GAU": "Aspartic Acid",
        "GAC": "Aspartic Acid",
        "GAA": "Glutamic Acid",
        "GAG": "Glutamic Acid",
        "UGU": "Cysteine",
        "UGC": "Cysteine",
        "UGA": "Stop",
        "UGG": "Tryptophan",
        "CGU": "Arginine",
        "CGC": "Arginine",
        "CGA": "Arginine",
        "CGG": "Arginine",
        "AGU": "Serine",
        "AGC": "Serine",
        "AGA": "Arginine",
        "AGG": "Arginine",
        "GGU": "Glycine",
        "GGC": "Glycine",
        "GGA": "Glycine",
        "GGG": "Glycine",
    }

    stop_codons = {"UAA", "UAG", "UGA"}

    mrna_sequence = mrna_sequence.upper().strip()

    if not all(n in "UCAG" for n in mrna_sequence):
        return {"error": "Invalid mRNA sequence. Use only U, C, A, G."}

    if len(mrna_sequence) % 3 != 0:
        return {"error": "mRNA sequence length must be divisible by 3."}

    if not mrna_sequence.startswith("AUG"):
        return {"error": "mRNA sequence must start with AUG (start codon)."}

    polypeptide = []
    for i in range(0, len(mrna_sequence), 3):
        codon = mrna_sequence[i : i + 3]
        if codon in stop_codons:
            break
        amino_acid = codon_translation.get(codon)
        if not amino_acid:
            return {"error": f"Invalid codon {codon} found."}
        polypeptide.append(amino_acid)

    if not polypeptide:
        return {"error": "No amino acids translated before encountering stop codon."}

    return {"polypeptide": polypeptide, "length": len(polypeptide)}


@app.get(
    "/myAPI-CDNA/v1/",
    tags=[cdna_tag],
    responses={
        "200": {
            "description": "ComplemetaryDNA reverse transcription",
            "content": {
                "application/json": {
                    "example": {
                        "Original": "AUGC",
                        "Double_Stranded_CDNA": " 5'-ATGC-3' and 3'-TACG-5' ",
                    }
                }
            },
        },
        "400": {
            "description": "Error",
            "content": {
                "application/json": {"example": {"CDNA error": "No Sequence Provided"}}
            },
        },
    },
)
def myCDNAAPI(query: CDNAQuery):
    sequence = query.seq
    if not sequence:
        return jsonify({"CDNA error": "No Sequenc Provided"}), 400
    result = get_complementary_dna(sequence)
    return jsonify({"Original": sequence, "Double_Stranded_CDNA": result})


@app.get(
    "/myAPI-RNA/v1/",
    tags=[rna_tag],
    responses={
        "200": {
            "description": "RNA transcription",
            "content": {
                "application/json": {
                    "example": {"Original": "ATGC", "RNA_Transcription": "AUGC"}
                }
            },
        },
        "400": {
            "description": "Error",
            "content": {
                "application/json": {"example": {"RNA error": "No Sequence Provided"}}
            },
        },
    },
)
def myRNAAPI(query: RNAQuery):
    sequence = query.seq
    if not sequence:
        return jsonify({"RNA error": "No Sequenc Provided"}), 400
    result = get_rna_transcription(sequence)
    return jsonify({"Original": sequence, "RNA_Transcription": result})


@app.get(
    "/myAPI-DNA/v1/",
    tags=[dna_tag],
    responses={
        "200": {
            "description": "DNA pair complement",
            "content": {
                "application/json": {
                    "example": {"Original": "ATGC", "Reverse_Complement": "GCAT"}
                }
            },
        },
        "400": {
            "description": "Error",
            "content": {
                "application/json": {"example": {"DNA error": "No Sequence Provided"}}
            },
        },
    },
)
def myDNAAPI(query: DNAQuery):
    sequence = query.seq
    if not sequence:
        return jsonify({"DNA error": "No Sequence Provided"}), 400
    result = get_dna_template_strand(sequence)
    return jsonify({"Original": sequence, "Reverse_Complement": result})


# =============v2==============================================================
@app.get(
    "/CDNA/v2/",
    tags=[cdna_tag],
    responses={
        "200": {
            "description": "ComplemetaryDNA reverse transcription",
            "content": {
                "application/json": {
                    "example": {
                        "Original": "AUGC",
                        "Double_Stranded_CDNA": " 5'-ATGC-3' and 3'-TACG-5' ",
                    }
                }
            },
        },
        "400": {
            "description": "Error",
            "content": {
                "application/json": {"example": {"CDNA error": "No Sequence Provided"}}
            },
        },
    },
)
def myCDNAAPI_v2(query: CDNAQuery):
    sequence = query.seq
    if not sequence:
        return jsonify({"CDNA error": "No Sequenc Provided"}), 400
    result = get_complementary_dna(sequence)
    return jsonify({"Original": sequence, "Double_Stranded_CDNA": result})


@app.get(
    "/RNA/v2/",
    tags=[rna_tag],
    responses={
        "200": {
            "description": "RNA transcription",
            "content": {
                "application/json": {
                    "example": {"Original": "ATGC", "RNA_Transcription": "AUGC"}
                }
            },
        },
        "400": {
            "description": "Error",
            "content": {
                "application/json": {"example": {"RNA error": "No Sequence Provided"}}
            },
        },
    },
)
def myRNAAPI_v2(query: RNAQuery):
    sequence = query.seq
    if not sequence:
        return jsonify({"RNA error": "No Sequenc Provided"}), 400
    result = get_rna_transcription(sequence)
    return jsonify({"Original": sequence, "RNA_Transcription": result})


@app.get(
    "/DNA/v2/",
    tags=[dna_tag],
    responses={
        "200": {
            "description": "DNA pair complement",
            "content": {
                "application/json": {
                    "example": {"Original": "ATGC", "Reverse_Complement": "GCAT"}
                }
            },
        },
        "400": {
            "description": "Error",
            "content": {
                "application/json": {"example": {"DNA error": "No Sequence Provided"}}
            },
        },
    },
)
def myDNAAPI_v2(query: DNAQuery):
    sequence = query.seq
    if not sequence:
        return jsonify({"DNA error": "No Sequence Provided"}), 400
    result = get_dna_template_strand(sequence)
    return jsonify({"Original": sequence, "Reverse_Complement": result})


@app.get(
    "/Polypeptide/v2/",
    tags=[aminoacid_tag],
    responses={
        "200": {
            "description": "Chain of peptide links",
            "content": {
                "application/json": {
                    "example": {
                        "Codon": "AUGGCCAAGUAA",
                        "Polypeptide": {
                            "polypeptide": ["Methionine", "Alanine", "Lysine"],
                            "length": 3,
                        },
                    }
                }
            },
        },
        "400": {
            "description": "Error",
            "content": {
                "application/json": {
                    "example": {"Amino error": "No mRNA Sequence Provided"}
                }
            },
        },
    },
)
def myPolypeptideAPI_v2(query: Translation):
    sequence = query.seq
    if not sequence:
        return jsonify({"mRNA error": "No mRNA Sequence Provided"}), 400
    result = get_translate_mrna(sequence)
    return jsonify({"Codon": sequence, "Polypeptide": result})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5604)
