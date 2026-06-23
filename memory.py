chat_memory = []


def save_chat(question, answer):
    chat_memory.append({
        "question": question,
        "answer": answer
    })


def get_chat_memory():
    return chat_memory