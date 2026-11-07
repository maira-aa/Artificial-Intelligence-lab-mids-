from lab_6_search import Retriever, show_hits

records = [
    {
        "id": "docs:python",
        "source": "python_guide.txt",
        "text": "Python is a programming language used for web development, automation, data science and artificial intelligence."
    },
    {
        "id": "docs:oop",
        "source": "oop_guide.txt",
        "text": "Object oriented programming organizes code using classes and objects. It supports inheritance, encapsulation and polymorphism."
    },
    {
        "id": "docs:ai",
        "source": "ai_guide.txt",
        "text": "Artificial intelligence allows computer systems to perform tasks that usually require human intelligence."
    }
]

engine = Retriever(records)

show_hits(
    engine.search(
        "classes objects and inheritance",
        k=2
    )
)