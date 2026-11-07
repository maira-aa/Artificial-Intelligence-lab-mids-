
# Lab 2 - Classroom Agent Testing

from Task_2_2 import ClassroomAgent


# Create a new agent for testing
agent = ClassroomAgent()

# Test cases with expected results
test_cases = [
    (29, True, "COOL", True),
    (29, True, "COOL", False),
    (20, True, "IDLE", True),
    (26, True, "IDLE", False),
    (19, True, "WARM", True),
    (29, False, "ECO", True),
    (29, False, "ECO", False),
    (24, True, "IDLE", True)
]

print("CLASSROOM AGENT TESTING")
print("-----------------------")

passed = 0

for step, test in enumerate(test_cases, 1):

    temp = test[0]
    occupied = test[1]
    expected_mode = test[2]
    expected_command = test[3]

    actual_mode, actual_command = agent.act(temp, occupied)

    if (actual_mode == expected_mode and
            actual_command == expected_command):

        result = "PASS"
        passed += 1

    else:
        result = "FAIL"

    print(
        "Test:", step,
        "| Temperature:", temp,
        "| Occupied:", occupied,
        "| Expected Mode:", expected_mode,
        "| Actual Mode:", actual_mode,
        "| Command:", actual_command,
        "| Result:", result
    )


# Display final results
print("-----------------------")
print("Passed:", passed, "out of", len(test_cases))

if passed == len(test_cases):
    print("All tests passed successfully!")
else:
    print("Some tests need correction.")
