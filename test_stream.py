import asyncio
from graph import app_graph

def test():
    for msg, metadata in app_graph.stream({"messages": [("user", "Hi")]}, stream_mode="messages"):
        print(f"Content: {repr(msg.content)}")
        print(f"Type: {getattr(msg, 'type', None)}")
        print(f"Match: {getattr(msg, 'type', '') == 'ai'}")

test()
