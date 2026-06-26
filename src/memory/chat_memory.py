class ChatMemory:

    def __init__(self):
        self.history = []

    def add_message(self, role, message):
        self.history.append({
            "role": role,
            "message": message
        })

    def get_history(self):

        conversation = ""

        for chat in self.history:
            conversation += f"{chat['role']}: {chat['message']}\n"

        return conversation

    def clear_history(self):
        self.history = []