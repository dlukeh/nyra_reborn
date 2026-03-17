import sys
import json
import asyncio
import websockets

if len(sys.argv) < 2:
    print("Usage: python tiny_test_client.py <agent_id>")
    sys.exit(1)

AGENT_ID = sys.argv[1]
WS_URL = "ws://127.0.0.1:8000/ws/agent"

async def main():
    async with websockets.connect(WS_URL) as ws:
        # Register agent
        register_msg = json.dumps({
            "event": "register",
            "data": {"agent_id": AGENT_ID}
        })
        await ws.send(register_msg)
        print(f"[{AGENT_ID}] sent register")
        print(f"[{AGENT_ID}] <- {await ws.recv()}")

        # Handshake
        handshake_msg = json.dumps({
            "event": "handshake",
            "data": {
                "sender": AGENT_ID,
                "context": "handshake",
                "payload": {"status": "ready"}
            }
        })
        await ws.send(handshake_msg)
        print(f"[{AGENT_ID}] sent handshake")
        print(f"[{AGENT_ID}] <- {await ws.recv()}")

        # If this is copilot, send a test message to nyra
        if AGENT_ID == "copilot":
            test_msg = json.dumps({
                "event": "message",
                "data": {
                    "sender": "copilot",
                    "target": "nyra",
                    "context": "test",
                    "payload": {"text": "Hello Nyra – test transmission from Copilot"}
                }
            })
            await ws.send(test_msg)
            print(f"[copilot] sent test message to nyra")

        # Keep connection open to receive messages
        while True:
            try:
                msg = await ws.recv()
                print(f"[{AGENT_ID}] <- {msg}")
            except Exception as e:
                print(f"[{AGENT_ID}] connection closed: {e}")
                break

if __name__ == "__main__":
    asyncio.run(main())
