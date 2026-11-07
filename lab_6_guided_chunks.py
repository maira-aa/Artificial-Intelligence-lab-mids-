
from lab_6_task2_chunks import make_chunks

documents = {
    "doc1": "The university library opens at 8 AM. Students can borrow books using their university cards. Books must be returned within fourteen days.",
    "doc2": "Students can reset their passwords through the recovery link. If the link does not work, they should contact technical support.",
    "doc3": "The computer laboratory is open from 9 AM to 5 PM. Students must follow laboratory rules and handle equipment carefully."
}

for strategy in ["0", "10", "sentence"]:
    print("\nStrategy:", strategy)

    chunks = make_chunks(documents, strategy)

    for chunk in chunks:
        print("\nID:", chunk["id"])
        print("Document:", chunk["doc"])
        print("Start:", chunk["start"])
        print("End:", chunk["end"])
        print("Text:", chunk["text"])
