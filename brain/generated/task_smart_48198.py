import os
import json
import datetime
import sys
from pathlib import Path

def run_task():
    a = 453
    b = 664
    print(f'🧮 Calculating {a} / {b}...')
    result = a / b
    print(f'✅ Result: {result}')

if __name__ == '__main__':
    run_task()