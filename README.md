# 🧬 CDaaR-API – Central Dogma as a REST API

![TRANSLATION](./images/T003.png)

**CDaaR (Central Dogma as a REST API)** is a Flask-based educational web service that models the molecular transcription and translation on cellular environments fundamental to genetics and genomics — including DNA reverse complementation, RNA transcription, reverse transcription to cDNA, and mRNA translation into polypeptides. Built for bioinformatics pipelines, teaching, and data validation, this API reflects on engineered natural selection, as intersection of biology with computing.

🔗 **Live Demo**: [https://dev15.miveh-nejad.info/](https://dev15.miveh-nejad.info/)

---

## 🚀 API Endpoints

- 🧬 **/DNA/v2/**: Get the reverse complement of a DNA strand.
- 🧫 **/RNA/v2/**: Transcribe DNA to pre-mRNA using canonical base-pairing.
- 🔄 **/CDNA/v2/**: Reverse transcribe mRNA into complementary double-stranded DNA.
- 🧿 **/Polypeptide/v2/**: Translate mRNA into a polypeptide chain of amino acids.

All endpoints:
- Enforce strict nucleotide validation using `Pydantic` models
- Limit input length to 10,000 characters
- Return biologically meaningful orientation (5’ → 3’ and 3’ → 5’)

---

## Example Use Case

```http
GET /RNA/v2/?seq=ATGC

Response:
{
  "Original": "ATGC",
  "RNA_Transcription": " 5'-AUGC-3' "
}

GET /Polypeptide/v2/?seq=AUGGCCAAGUAA

Response:
{
  "Codon": "AUGGCCAAGUAA",
  "Polypeptide": {
    "polypeptide": ["Methionine", "Alanine", "Lysine"],
    "length": 3
  }
}


📦 Installation

git clone git@github.com:<your-username>/CDAAR-API.git
cd CDAAR-API
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python Translation_transcription.py

⚙️ API Documentation
This project uses flask-openapi3 with built-in support for:

Swagger UI
Redoc
RapiDoc
Scalar

Once running, navigate to:

http://localhost:5604/docs (Swagger)

http://localhost:5604/redoc (Redoc)

✅ Testing
Run tests using pytest:


pytest tests/
You can also run PEP8 formatting checks:

black --check .
GitHub Actions CI is configured to run tests and black checks automatically on each push.

🧠 Credits
Developed by Kayvan Mivehnejad as a synthesis of bioinformatics knowledge and Python RESTful service design.

This API is inspired by educational needs, genomics pipelines, and the desire to bring the Central Dogma to life in data-driven platforms.

📄 License
This project is licensed under the MIT License. See LICENSE for details.
