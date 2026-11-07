def check_eligibility(score, documents, attendance, fields_valid):

    if score < 70:
        return "Not Eligible", "Score is below 70"

    if documents == "No":
        return "Not Eligible", "Required documents are incomplete"

    if attendance < 75:
        return "Not Eligible", "Attendance is below 75%"

    if fields_valid == "No":
        return "Not Eligible", "Some information fields are invalid"

    return "Eligible", "All conditions are satisfied"


test_cases = [
    {
        "name": "Eligible Student",
        "score": 85,
        "documents": "Yes",
        "attendance": 80,
        "fields_valid": "Yes",
        "expected": "Eligible"
    },
    {
        "name": "Low Attendance",
        "score": 80,
        "documents": "Yes",
        "attendance": 70,
        "fields_valid": "Yes",
        "expected": "Not Eligible"
    },
    {
        "name": "Invalid Information",
        "score": 90,
        "documents": "Yes",
        "attendance": 85,
        "fields_valid": "No",
        "expected": "Not Eligible"
    },
    {
        "name": "Minimum Score Boundary",
        "score": 70,
        "documents": "Yes",
        "attendance": 75,
        "fields_valid": "Yes",
        "expected": "Eligible"
    }
]


print("SCHOLARSHIP ELIGIBILITY SYSTEM")
print("=" * 45)

for test in test_cases:

    actual, reason = check_eligibility(
        test["score"],
        test["documents"],
        test["attendance"],
        test["fields_valid"]
    )

    print("\nTest Case:", test["name"])
    print("Input:", test)
    print("Expected Result:", test["expected"])
    print("Actual Result:", actual)
    print("Reason:", reason)

    if actual == test["expected"]:
        print("Test Status: PASS")
    else:
        print("Test Status: FAIL")
