# TMT Translation SDK (UNOFFICIAL)

A python client using the TMT Translation API, providing convenient methods to translate text between English, Nepali, and Tamang. Built for the Google Google TMT Hackathon 2026 (and cause using api directly is boring af).

# Documentation
- [Usage](docs/usage.md) - How to use the translation client and its methods.
- [Sentence Normalization](docs/sentence-normalization.md) - Helper functions to clean and split rough text into logical sentences for better translation results.
- [Examples](docs/examples.md) - Practical copy-paste examples for common SDK workflows.
    > The API is designed to translate one sentence at a time, so for best results, use the sentence normalization helper to clean and split your text into logical sentences before translation.

# Installation

I recommend using UV for a clean environment, but you can also install the package directly with pip:

```bash
uv add tmt-translation-sdk
```
```bash
pip install tmt-translation-sdk
``` 
# Note
- I made this in a rush for the hackathon, so expect some rough edges and room for improvement. Feedback and contributions are welcome!
- The API is designed for sentence-by-sentence translation, so for best results, use the sentence normalization helper to clean and split your text into logical sentences before translation.