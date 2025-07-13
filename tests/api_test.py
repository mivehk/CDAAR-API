import pytest
import requests

BASE_URL = "https://dev15.miveh-nejad.info"


def test_rna_transcription():
    response = requests.get(f"{BASE_URL}/RNA/v2/", params={"seq": "ATGC"})
    assert response.status_code == 200
    data = response.json()
    assert data["Original"] == "ATGC"
    assert "RNA_Transcription" in data
    assert "AUGC" in data["RNA_Transcription"]


def test_dna_reverse_complement():
    response = requests.get(f"{BASE_URL}/DNA/v2/", params={"seq": "ATGC"})
    assert response.status_code == 200
    data = response.json()
    assert data["Original"] == "ATGC"
    assert data["Reverse_Complement"].startswith(" 5'-GCAT")


def test_cdna_synthesis():
    response = requests.get(f"{BASE_URL}/CDNA/v2/", params={"seq": "AUGC"})
    assert response.status_code == 200
    data = response.json()
    assert data["Original"] == "AUGC"
    assert "Double_Stranded_CDNA" in data


def test_polypeptide_translation_success():
    response = requests.get(
        f"{BASE_URL}/Polypeptide/v2/", params={"seq": "AUGGCCAAGUAA"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["Codon"] == "AUGGCCAAGUAA"
    assert "polypeptide" in data["Polypeptide"]
    assert data["Polypeptide"]["length"] == 3


def test_polypeptide_translation_invalid_start():
    response = requests.get(
        f"{BASE_URL}/Polypeptide/v2/", params={"seq": "GUGGCCAAGUAA"}
    )
    assert response.status_code == 200  # still 200, but should contain error
    data = response.json()
    assert "error" in data["Polypeptide"]
    assert "start codon" in data["Polypeptide"]["error"]


def test_polypeptide_translation_bad_chars():
    response = requests.get(f"{BASE_URL}/Polypeptide/v2/", params={"seq": "AUGXYZ"})
    assert response.status_code == 422
    data = response.json()
    assert isinstance(data, list)
    assert any("pattern" in error.get("msg", "").lower() for error in data)


def test_polypeptide_translation_non_triplet():
    response = requests.get(f"{BASE_URL}/Polypeptide/v2/", params={"seq": "AUGG"})
    assert response.status_code == 200
    data = response.json()
    assert "error" in data["Polypeptide"]
    assert "divisible by 3" in data["Polypeptide"]["error"]
