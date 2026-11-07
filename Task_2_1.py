class ClassroomAgent:

    def act(self, temp, occupied):

        if not occupied:
            return "ECO"

        if temp > 26:
            return "COOL"

        if temp < 20:
            return "WARM"

        return "IDLE"


agent = ClassroomAgent()

percepts = [
    (29, True),
    (29, True),
    (20, True),
    (26, True),
    (19, True),
    (29, False)
]

print("REFLEX CLASSROOM AGENT")

for step, percept in enumerate(percepts, 1):

    mode = agent.act(*percept)

    print(
        step,
        "Temperature:", percept[0],
        "Occupied:", percept[1],
        "Target Mode:", mode
    )
