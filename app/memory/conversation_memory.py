# Simple in-memory conversation store
conversation_memory = {}

def add_message(user_id, role, message):
    if user_id not in conversation_memory:
        conversation_memory[user_id] = []

    conversation_memory[user_id].append({
        "role": role,
        "content": message
    })

    # keep only last 6 messages
    conversation_memory[user_id] = conversation_memory[user_id][-6:]


def get_history(user_id):
    return conversation_memory.get(user_id, [])