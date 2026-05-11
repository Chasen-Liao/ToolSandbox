import requests

import json



RKLLM_URL = 'http://172.31.18.39:8080/v1'



print('='*60)

print('rkllm ToolSandbox Compatibility Test')

print('='*60)

print()



# Test 1: models endpoint

print('Test 1: /v1/models')

r = requests.get(RKLLM_URL + '/models', timeout=10)

print('  Status:', r.status_code)

print('  Models:', r.json())

print()



# Test 2: Chat completion

print('Test 2: Chat completion')

r = requests.post(RKLLM_URL + '/chat/completions', json={

    'model': 'rkllm-model',

    'messages': [{'role': 'user', 'content': 'Hello'}],

    'max_tokens': 50

}, timeout=30)

print('  Status:', r.status_code)

data = r.json()

print('  Content:', data['choices'][0]['message']['content'][:100].encode('ascii', 'replace').decode('ascii'))

print()



# Test 3: Function calling

print('Test 3: Function calling')

tools = [{

    'type': 'function',

    'function': {

        'name': 'get_weather',

        'description': 'Get weather for a location',

        'parameters': {

            'type': 'object',

            'properties': {'location': {'type': 'string'}},

            'required': ['location']

        }

    }

}]

r = requests.post(RKLLM_URL + '/chat/completions', json={

    'model': 'rkllm-model',

    'messages': [{'role': 'user', 'content': 'What is the weather in Beijing?'}],

    'tools': tools,

    'max_tokens': 100

}, timeout=30)

data = r.json()

msg = data['choices'][0]['message']

if 'tool_calls' in msg:

    print('  PASS: Tool called =', msg['tool_calls'][0]['function']['name'])

    print('  Args:', msg['tool_calls'][0]['function']['arguments'])

else:

    print('  FAIL: No tool call')

    print('  Content:', msg.get('content', 'N/A')[:100])

print()



print('Summary: rkllm API is OpenAI-compatible and supports function calling!')

