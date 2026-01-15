#!/bin/bash
# Test the Dream AI with various tasks

echo "🧪 Testing Dream AI Intelligence..."
echo ""

echo "Test 1: Math Calculation"
curl -s -X POST http://localhost:3000/command \
  -H "Content-Type: application/json" \
  -d '{"task": "Calculate 123 + 456"}' | python3 -c "
import sys, json
data = json.load(sys.stdin)
print('📊 Result:', data['status'].get('execution', 'No execution'))
"
echo ""

echo "Test 2: Google Search"
curl -s -X POST http://localhost:3000/command \
  -H "Content-Type: application/json" \
  -d '{"task": "Search for latest AI news"}' | python3 -c "
import sys, json
data = json.load(sys.stdin)
status = data['status']
print('📊 Status:', status['status'])
print('📁 Script:', status.get('script', 'N/A'))
if status.get('execution'):
    lines = status['execution'].split('\n')[:5]
    for line in lines:
        print('  ', line)
"
echo ""

echo "Test 3: Custom Task"
curl -s -X POST http://localhost:3000/command \
  -H "Content-Type: application/json" \
  -d '{"task": "Write a script to check disk space"}' | python3 -c "
import sys, json
data = json.load(sys.stdin)
status = data['status']
print('📊 Status:', status['status'])
print('📁 Script:', status.get('script', 'N/A'))
"
echo ""

echo "✅ Testing complete!"
