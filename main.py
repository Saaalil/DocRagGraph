import sys
from agent import query_agent

def chat_loop():
    print("========================================")
    print("🤖 GraphRAG System Initialized")
    print("Type 'exit' or 'quit' to stop.")
    print("========================================")
    
    while True:
        try:
            user_input = input("\n👤 You: ")
            if user_input.lower() in ["exit", "quit"]:
                break
                
            if not user_input.strip():
                continue
                
            answer = query_agent(user_input)
            print(f"\n🧠 RAG Agent:\n{answer}")
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    chat_loop()
