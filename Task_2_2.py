class ClassroomAgent:

    def __init__(self):
        self.previous_mode = None

    def act(self, temp, occupied):


        if not occupied:
            target_mode = "ECO"

        elif temp > 26:
            target_mode = "COOL"

        elif temp < 20:
            target_mode = "WARM"

        else:
            target_mode = "IDLE"

        if target_mode != self.previous_mode:
            send_command = True
        else:
            send_command = False

        self.previous_mode = target_mode

        return target_mode, send_command


agent = ClassroomAgent()

percepts = [
    (29, True),
    (29, True),
    (20, True),
    (26, True),
    (19, True),
    (29, False),
    (29, False),
    (24, True)
]

print("STATEFUL CLASSROOM AGENT")
print("------------------------")

for step, percept in enumerate(percepts, 1):

    previous_mode = agent.previous_mode

    target_mode, send_command = agent.act(
        percept[0], percept[1]
    )

    if send_command:
        command_status = "Send"
    else:
        command_status = "No command"

    print(
        "Step:", step,
        "| Previous Mode:", previous_mode,
        "| Temperature:", percept[0],
        "| Occupied:", percept[1],
        "| Target Mode:", target_mode,
        "| Command:", command_status
    )