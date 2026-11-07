
import re

samples = [
    "AI, search!",
    "I can't log in.",
    "help@example.com",
    "CS4944",
    "",
    "یہ ایک مثال ہے"
]

print("TOKENIZATION COMPARISON")
print("=" * 55)

for text in samples:
    whitespace_tokens = text.split()
    regex_tokens = re.findall(r"\b\w+\b", text, flags=re.UNICODE)

    print("\nOriginal Text:", repr(text))
    print("Whitespace Tokens:", whitespace_tokens)
    print("Whitespace Count:", len(whitespace_tokens))
    print("Regex Tokens:", regex_tokens)
    print("Regex Count:", len(regex_tokens))

print("\nMODEL TOKENIZER COMPARISON")
print("=" * 55)

try:
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    for text in samples[:2]:
        print("\nText:", text)
        print("Model Tokens:", tokenizer.tokenize(text))
        print("Model Count:", len(tokenizer.tokenize(text)))

except Exception:
    print("Model tokenizer is unavailable. Basic comparison completed.")
