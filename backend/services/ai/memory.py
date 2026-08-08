class ConversationMemory:

    def __init__(self):

        self.memory = {}

    def add(self, session_id, role, message):

        if session_id not in self.memory:
            self.memory[session_id] = []

        self.memory[session_id].append({

            "role": role,

            "content": message

        })

    def get(self, session_id):

        return self.memory.get(session_id, [])


conversation_memory = ConversationMemory()