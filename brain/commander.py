import time
import sys

# The file where the Innovator looks for new work
TASK_INBOX = "brain/tasks.txt"

def send_order(order):
    """Injects a high-priority task into the AI's brain."""
    
    # Format the task so the Innovator recognizes it immediately
    formatted_task = f"USER_ORDER: {order}"
    
    try:
        with open(TASK_INBOX, "a") as f:
            f.write(formatted_task + "\n")
            
        print(f"✅ Order Sent: '{order}'")
        print("   (The Innovator should pick this up in ~10 seconds)")
        
    except Exception as e:
        print(f"❌ Failed to send order: {e}")

if __name__ == "__main__":
    # Check if user provided an argument (e.g., python commander.py "Do this")
    if len(sys.argv) > 1:
        user_order = " ".join(sys.argv[1:])
        send_order(user_order)
    else:
        # Interactive mode
        print("🤖 DREAM AI COMMANDER")
        print("   Type your order below (or 'exit' to quit)")
        print("   ------------------------------------------")
        
        while True:
            command = input("👉 Your Command: ").strip()
            if command.lower() in ['exit', 'quit']:
                break
            if command:
                send_order(command)
                time.sleep(1)