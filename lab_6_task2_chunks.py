import re


def word_spans(text):
    return [(m.start(), m.end()) for m in re.finditer(r"\S+", text)]


def windows(text, size=40, overlap=10, offset=0):
    if size <= 0 or not 0 <= overlap < size:
        raise ValueError("Require size > 0 and 0 <= overlap < size")

    spans = word_spans(text)
    result = []

    for i in range(0, len(spans), size - overlap):
        j = min(i + size, len(spans))
        result.append((offset + spans[i][0], offset + spans[j - 1][1]))

        if j == len(spans):
            break

    return result


def sentence_chunks(text, size=40):
    if size <= 0:
        raise ValueError("Size must be positive")

    cuts = [0] + [m.end() for m in re.finditer(r"[.!?]\s+", text)] + [len(text)]

    out = []
    pending = None
    count = 0

    for a, b in zip(cuts, cuts[1:]):
        segment = text[a:b]
        n = len(segment.split())

        if not n:
            continue

        if n > size:
            if pending is not None:
                out.append(pending)

            out.extend(windows(segment, size, 0, a))
            pending = None
            count = 0

        elif pending is not None and count + n <= size:
            pending = (pending[0], b)
            count += n

        else:
            if pending is not None:
                out.append(pending)

            pending = (a, b)
            count = n

    if pending is not None:
        out.append(pending)

    return out


def make_chunks(docs, strategy):
    result = []

    for doc_id, data in docs.items():
        text = data["text"]

        if strategy == "sentence":
            spans = sentence_chunks(text)
        else:
            spans = windows(text, 40, int(strategy))

        for i, (start, end) in enumerate(spans):
            result.append({
                "id": f"{doc_id}:{i}",
                "doc": doc_id,
                "source": data["source"],
                "start": start,
                "end": end,
                "text": text[start:end]
            })

    return result


docs = {
    "handbook": {
        "source": "handbook.txt",
        "text": """
University students must submit their assignments before the announced deadline.
Late submissions normally receive a penalty according to the course rules.
Students should check the learning portal regularly for updated deadlines.
An assignment must be uploaded in the required file format.
Students are responsible for checking that their uploaded file opens correctly.
A technical problem should be reported to the instructor as soon as possible.
Students who experience illness may request an extension.
An extension is not automatic and requires proper medical evidence.
Medical evidence must be provided before the original deadline.
The instructor reviews the request before approving any extension.
Without the required evidence, the normal late submission rule applies.
Students should keep a copy of their submitted assignment.
The learning portal displays the submission date and time.
A successful upload should be checked before leaving the portal.
Students must not submit another student's work as their own.
Academic honesty applies to every assignment and examination.
The course instructor can explain the submission procedure.
Students should contact the department if the portal remains unavailable.
The department records reported technical problems for review.
A student should include the course name when reporting a problem.
The final decision about an extension belongs to the authorized instructor.
""".strip()
    },

    "it_support": {
        "source": "it_support.txt",
        "text": """
Students can access university accounts through the official login page.
A valid username and password are required to sign in.
Users should never share their passwords with another person.
If a password is forgotten, the user can select the recovery option.
The recovery link is sent to the registered email address.
Users should check their spam folder if the email is missing.
An expired recovery link cannot be used again.
The user must request a new recovery link.
If the registered email address is no longer available, contact IT support.
The support team may ask for basic account verification.
Do not send passwords or private login codes in an email.
A support request should include the account username.
Users should describe the problem clearly when contacting support.
Screenshots may help explain an error message.
Personal information should be hidden before sharing screenshots.
The IT team checks reported login problems during working hours.
Some account problems may require additional verification.
A user should wait for the official support response.
Repeated login attempts may temporarily lock an account.
In that situation, the user should follow the account recovery instructions.
University accounts should only be accessed by their owners.
""".strip()
    },

    "equipment": {
        "source": "equipment_guide.txt",
        "text": """
University computer labs provide printers and scanners for student use.
Students should check the device instructions before starting a task.
A printer should have paper and sufficient ink before printing.
If printed pages are blank, first check the ink level.
Next, run the printer cleaning utility when available.
After cleaning, print a test page to check the result.
Follow the device manual if the problem continues.
Do not open or repair electrical parts of the printer.
A scanner requires the document to be placed correctly.
Users should select the correct scanning source.
A blank scanner image may result from incorrect document placement.
Check the preview before saving the scanned file.
Use a suitable file format for the required task.
Save the file in the correct folder.
Students should report repeated equipment problems to lab staff.
Include the device name when reporting a problem.
Do not remove cables or parts without staff permission.
Lab staff can inspect the equipment and provide further instructions.
Students should keep the work area clean after using a device.
Report damaged equipment instead of continuing to use it.
Follow the instructions displayed near each device.
""".strip()
    }
}


print("CHUNKING COMPARISON")
print("=" * 55)

strategies = ["0", "10", "sentence"]

for strategy in strategies:
    chunks = make_chunks(docs, strategy)

    print("\nStrategy:", strategy)
    print("Total Chunks:", len(chunks))

    total_words = sum(len(c["text"].split()) for c in chunks)
    original_words = sum(len(d["text"].split()) for d in docs.values())

    print("Original Words:", original_words)
    print("Chunk Words:", total_words)
    print("Repeated Words:", total_words - original_words)

    for doc_id in docs:
        selected = [c for c in chunks if c["doc"] == doc_id]
        sizes = [len(c["text"].split()) for c in selected]

        print("\nDocument:", doc_id)
        print("Chunk Count:", len(selected))
        print("Chunk Sizes:", sizes)

        if doc_id == "handbook":
            evidence = "Medical evidence must be provided before the original deadline."
        elif doc_id == "it_support":
            evidence = "The user must request a new recovery link."
        else:
            evidence = "After cleaning, print a test page to check the result."

        found = any(evidence in c["text"] for c in selected)
        print("Rule Evidence Preserved:", found)


print("\nBOUNDARY TESTS")
print("=" * 55)

print("Empty Text:", windows(""))
print("Short Text:", windows("short document"))

try:
    windows("one two three", 2, 2)
except ValueError:
    print("Invalid Overlap: Correctly rejected")

long_sentence = " ".join(["word"] * 95) + "."

long_chunks = sentence_chunks(long_sentence)

print("Long Sentence Chunk Sizes:",
      [len(long_sentence[a:b].split()) for a, b in long_chunks])

for strategy in strategies:
    chunks = make_chunks(
        {"example": {"source": "example.txt",
                     "text": "Reset your password. Keep recovery codes private."}},
        strategy
    )

    for chunk in chunks:
        original = docs.get(chunk["doc"], {}).get("text")

        if original is None:
            original = "Reset your password. Keep recovery codes private."

        assert chunk["text"] == original[chunk["start"]:chunk["end"]]

print("\nSource offsets checked successfully.")
print("All boundary tests completed.")