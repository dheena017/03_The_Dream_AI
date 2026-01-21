class Innovator:
    """
    Innovator - Suggests new tasks for the AI to perform.
    """
    def __init__(self, mode="researcher"):
        self.mode = mode

    def run_autonomy(self):
        """
        Suggests tasks when the inbox is empty.
        """
        print(f"💡 Innovator ({self.mode}): Thinking of new tasks...")
        # For now, we can just log that we are thinking.
        # In a real implementation, this would generate tasks and write to tasks.txt
        pass
