"""
AI Teacher - Uses external AI models to help Dream AI learn better code
Integrates with OpenAI GPT, Claude, and Google Gemini
"""

import os
import json
import subprocess

class AITeacher:
    """
    Learns from advanced AI models to improve code generation
    Uses GPT-5, Claude, Gemini as teachers
    """
    
    def __init__(self):
        self.openai_key = os.environ.get("OPENAI_API_KEY")
        self.anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
        self.google_key = os.environ.get("GOOGLE_API_KEY")
        
    def ask_gpt(self, question):
        """Ask OpenAI GPT for help"""
        if not self.openai_key:
            return None
            
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.openai_key)
            
            response = client.chat.completions.create(
                model="gpt-4",  # Use gpt-4 or gpt-3.5-turbo
                messages=[
                    {"role": "system", "content": "You are a Python coding expert. Generate clean, working Python code."},
                    {"role": "user", "content": question}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ GPT Error: {e}")
            return None
    
    def ask_claude(self, question):
        """Ask Claude/Anthropic for help"""
        if not self.anthropic_key:
            return None
            
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=self.anthropic_key)
            
            message = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=500,
                messages=[
                    {"role": "user", "content": question}
                ]
            )
            
            return message.content[0].text
        except Exception as e:
            print(f"❌ Claude Error: {e}")
            return None
    
    def ask_gemini(self, question):
        """Ask Google Gemini for help"""
        if not self.google_key:
            return None
            
        try:
            import google.generativeai as genai
            
            genai.configure(api_key=self.google_key)
            model = genai.GenerativeModel('gemini-pro')
            
            response = model.generate_content(question)
            return response.text
        except Exception as e:
            print(f"❌ Gemini Error: {e}")
            return None
    
    def get_best_solution(self, task):
        """
        Ask all available AI teachers and pick the best solution
        Tries: GPT -> Claude -> Gemini
        Returns: Python code string or None
        """
        prompt = f"""Generate a complete, working Python script for this task: {task}

Requirements:
- Must be executable Python code
- Include all necessary imports
- Have a run_task() function
- Include error handling
- Add helpful print statements

Return ONLY the Python code, no explanations."""
        
        # Try GPT first (usually best for code)
        print("🧑‍🏫 Asking GPT for help...")
        solution = self.ask_gpt(prompt)
        if solution and "def run_task" in solution:
            print("✅ GPT provided solution")
            return self._extract_code(solution)
        
        # Try Claude
        print("🧑‍🏫 Asking Claude for help...")
        solution = self.ask_claude(prompt)
        if solution and "def run_task" in solution:
            print("✅ Claude provided solution")
            return self._extract_code(solution)
        
        # Try Gemini
        print("🧑‍🏫 Asking Gemini for help...")
        solution = self.ask_gemini(prompt)
        if solution and "def run_task" in solution:
            print("✅ Gemini provided solution")
            return self._extract_code(solution)
        
        print("⚠️ No AI teachers available or couldn't generate solution")
        return None
    
    def _extract_code(self, text):
        """Extract Python code from AI response (remove markdown formatting)"""
        # Remove markdown code blocks
        if "```python" in text:
            start = text.find("```python") + 9
            end = text.find("```", start)
            return text[start:end].strip()
        elif "```" in text:
            start = text.find("```") + 3
            end = text.find("```", start)
            return text[start:end].strip()
        else:
            # Already clean code
            return text.strip()
    
    def improve_code(self, current_code, task):
        """Ask AI teachers to improve existing code"""
        prompt = f"""Improve this Python code for the task: {task}

Current code:
{current_code}

Make it:
- More efficient
- Better error handling
- Clearer output
- More robust

Return ONLY the improved Python code."""
        
        improved = self.ask_gpt(prompt)
        if improved:
            return self._extract_code(improved)
        
        return current_code  # Return original if improvement fails
    
    def learn_new_skill(self, skill_name):
        """Learn how to implement a new skill from AI teachers"""
        prompt = f"""Create a Python function that can {skill_name}.

Requirements:
- Function named run_task()
- Complete working code
- Error handling
- Useful output

Return complete Python script."""
        
        return self.get_best_solution(skill_name)
