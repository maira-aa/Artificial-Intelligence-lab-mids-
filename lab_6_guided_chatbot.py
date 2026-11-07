
from lab_6_search import Retriever

faqs = [
    {
        "id": "FAQ1",
        "text": "Students can reset a forgotten password by using the password recovery link on the login page.",
        "answer": "Use the password recovery link on the login page to reset your password.",
        "source": "Student Handbook"
    },
    {
        "id": "FAQ2",
        "text": "Assignments must be submitted through the university learning portal before the deadline.",
        "answer": "Submit your assignments through the university learning portal before the deadline.",
        "source": "Assignment Guidelines"
    },
    {
        "id": "FAQ3",
        "text": "Students can contact the IT support department if they face login or technical problems.",
        "answer": "Contact the IT support department for login or technical problems.",
        "source": "IT Support Guide"
    },
    {
        "id": "FAQ4",
        "text": "The university library is open from 8 AM to 5 PM on working days.",
        "answer": "The library is open from 8 AM to 5 PM on working days.",
        "source": "Library Handbook"
    }
]

retriever = Retriever(faqs)

print("University FAQ Chatbot")
print("Type 'exit' to stop.")

while True:
    question = input("\nYou: ").strip()

    if question.lower() == "exit":
        print("Chatbot: Goodbye!")
        break

    if not question:
        print("Chatbot: Please enter a question.")
        continue

    hits = retriever.search(question, k=1)
    
    if hits and hits[0][1] >= 0.15:
        record, score = hits[0]
        print("Chatbot:", record["answer"])
        print("Source:", record["source"])
        print("Confidence score:", round(float(score), 3))
    else:
        print("Chatbot: I could not find a reliable answer.")
        print("Suggested questions:")
        print("- How can I reset my password?")
        print("- How do I submit an assignment?")
        print("- How can I contact IT support?")
