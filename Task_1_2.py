

def scholarship_rules(score, attendance, documents):

    if score >= 70 and attendance >= 75 and documents == "Yes":
        return "Eligible"

    return "Not Eligible"


def chatbot_response(score, attendance, documents):

    if score >= 70:
        return "Your marks are good. You may qualify for the scholarship."

    return "Your marks are below the required limit."


score = 80
attendance = 60
documents = "Yes"


rule_result = scholarship_rules(
    score, attendance, documents
)

chatbot_result = chatbot_response(
    score, attendance, documents
)


print("AI SYSTEM COMPARISON")
print("=" * 40)

print("\nStudent Information")
print("Score:", score)
print("Attendance:", attendance, "%")
print("Documents Complete:", documents)

print("\nRule-Based System Result:")
print(rule_result)

print("\nConversational AI Response:")
print(chatbot_result)

print("\nComparison:")

if rule_result != "Eligible":
    print("The rule-based system rejects the application")
    print("because the attendance is below 75%.")

if "may qualify" in chatbot_result:
    print("The chatbot gives a positive response based mainly")
    print("on marks, but it does not check every condition.")

print("\nConclusion:")
print("A natural-sounding answer does not always mean")
print("that the system has made a correct decision.")
