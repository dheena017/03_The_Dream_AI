#!/usr/bin/env python3
"""
Test the Self-Evolution System
Demonstrates how the AI improves itself
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from brain.evolution.self_evolution import SelfEvolutionEngine
from brain.bridge import Bridge

def test_self_improvement_task():
    """Test self-improvement task detection and processing"""
    
    print("\n" + "="*70)
    print("🧠 DREAM AI - SELF-EVOLUTION SYSTEM TEST")
    print("="*70 + "\n")
    
    # Test tasks
    test_tasks = [
        "Improve SmartDeveloper with image processing skill",
        "Add machine learning capability to pattern recognition",
        "Optimize memory database for faster queries",
        "Enhance brain orchestration algorithm",
        "Calculate 25 * 100",  # Regular task (not self-improvement)
        "Create a file named test.txt",  # Regular task
    ]
    
    engine = SelfEvolutionEngine()
    
    print("📋 TESTING TASK DETECTION:\n")
    
    for i, task in enumerate(test_tasks, 1):
        is_self_improvement = engine.analyzer.is_self_improvement_task(task)
        status = "🧬 SELF-IMPROVEMENT" if is_self_improvement else "📝 REGULAR TASK"
        print(f"{i}. {status}")
        print(f"   Task: {task}\n")
    
    print("\n" + "="*70)
    print("🔬 PROCESSING A SELF-IMPROVEMENT TASK")
    print("="*70 + "\n")
    
    # Pick a self-improvement task and process it
    improvement_task = "Improve SmartDeveloper with image processing skill"
    
    print(f"📋 Task: {improvement_task}\n")
    
    result = engine.process_self_improvement_task(improvement_task)
    
    print("\n✅ SELF-EVOLUTION PROCESS COMPLETE")
    print(f"📄 Documentation saved to: {result['summary_document']['filename']}\n")
    
    # Show the generated documentation
    with open(result['summary_document']['filename'], 'r') as f:
        print("📖 GENERATED DOCUMENTATION:\n")
        print(f.read())


def test_with_bridge():
    """Test self-evolution through the Bridge"""
    
    print("\n" + "="*70)
    print("🌉 TESTING THROUGH BRIDGE (REST API)")
    print("="*70 + "\n")
    
    bridge = Bridge()
    
    # Test self-improvement task
    task1 = "Add optimization to brain orchestration system"
    print(f"Testing self-improvement task:\n   {task1}\n")
    
    result1 = bridge.process_task(task1)
    print(f"\nResult Type: {result1.get('type', 'regular')}")
    
    # Test regular task
    task2 = "Calculate 42 * 7"
    print(f"\n\nTesting regular task:\n   {task2}\n")
    
    result2 = bridge.process_task(task2)
    print(f"\nResult Type: {result2.get('type', 'regular')}")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Test Self-Evolution System')
    parser.add_argument('--engine', action='store_true', help='Test evolution engine directly')
    parser.add_argument('--bridge', action='store_true', help='Test through Bridge')
    parser.add_argument('--all', action='store_true', help='Run all tests')
    
    args = parser.parse_args()
    
    if args.engine or args.all:
        test_self_improvement_task()
    
    if args.bridge or args.all:
        test_with_bridge()
    
    if not (args.engine or args.bridge or args.all):
        print("Run with --help to see options")
        test_self_improvement_task()
