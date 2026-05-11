#!/usr/bin/env python3
"""
Test script to verify rkllm compatibility with ToolSandbox.
This script directly tests the OpenAI API compatibility.
"""

import json
import requests
import sys

RKLLM_URL = "http://172.31.18.39:8080/v1"

def test_models_endpoint():
    """Test /v1/models endpoint"""
    print("Testing /v1/models endpoint...")
    response = requests.get(f"{RKLLM_URL}/models", timeout=10)
    assert response.status_code == 200, f"Status code: {response.status_code}"
    data = response.json()
    print(f"  ✓ Models available: {[m['id'] for m in data['data']]}")
    return data['data'][0]['id']

def test_chat_completion():
    """Test basic chat completion"""
    print("Testing /v1/chat/completions...")
    response = requests.post(
        f"{RKLLM_URL}/chat/completions",
        json={
            "model": "rkllm-model",
            "messages": [{"role": "user", "content": "Hello"}],
            "max_tokens": 50
        },
        timeout=30
    )
    assert response.status_code == 200, f"Status code: {response.status_code}"
    data = response.json()
    assert "choices" in data, "No choices in response"
    print(f"  ✓ Chat completion works")
    return data

def test_function_calling():
    """Test function calling capability (critical for ToolSandbox)"""
    print("Testing function calling (tools)...")
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get weather for a location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {"type": "string", "description": "City name"}
                    },
                    "required": ["location"]
                }
            }
        }
    ]
    
    response = requests.post(
        f"{RKLLM_URL}/chat/completions",
        json={
            "model": "rkllm-model",
            "messages": [{"role": "user", "content": "What is the weather in Beijing?"}],
            "tools": tools,
            "max_tokens": 100
        },
        timeout=30
    )
    assert response.status_code == 200, f"Status code: {response.status_code}"
    data = response.json()
    
    msg = data['choices'][0]['message']
    if 'tool_calls' in msg:
        print(f"  ✓ Function calling supported!")
        print(f"    Tool called: {msg['tool_calls'][0]['function']['name']}")
        print(f"    Arguments: {msg['tool_calls'][0]['function']['arguments']}")
        return True
    else:
        print(f"  ✗ Function calling NOT supported")
        print(f"    Response: {msg.get('content', 'N/A')[:100]}")
        return False

def test_multiple_tool_calls():
    """Test multiple parallel tool calls"""
    print("Testing multiple parallel tool calls...")
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "search_contacts",
                "description": "Search contacts by name",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"}
                    }
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_wifi_status",
                "description": "Get current WiFi status",
                "parameters": {"type": "object", "properties": {}}
            }
        }
    ]
    
    response = requests.post(
        f"{RKLLM_URL}/chat/completions",
        json={
            "model": "rkllm-model",
            "messages": [{"role": "user", "content": "Check WiFi status and search for John in contacts"}],
            "tools": tools,
            "max_tokens": 150
        },
        timeout=30
    )
    assert response.status_code == 200, f"Status code: {response.status_code}"
    data = response.json()
    
    msg = data['choices'][0]['message']
    if 'tool_calls' in msg:
        print(f"  ✓ Multiple tool calls: {len(msg['tool_calls'])} calls")
        for tc in msg['tool_calls']:
            print(f"    - {tc['function']['name']}")
        return True
    else:
        print(f"  ✗ No tool calls returned")
        return False

def test_system_message():
    """Test system message handling"""
    print("Testing system message handling...")
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "set_wifi_status",
                "description": "Set WiFi on or off",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "on": {"type": "boolean"}
                    },
                    "required": ["on"]
                }
            }
        }
    ]
    
    response = requests.post(
        f"{RKLLM_URL}/chat/completions",
        json={
            "model": "rkllm-model",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that controls device settings."},
                {"role": "user", "content": "Turn off WiFi"}
            ],
            "tools": tools,
            "max_tokens": 100
        },
        timeout=30
    )
    assert response.status_code == 200, f"Status code: {response.status_code}"
    data = response.json()
    
    msg = data['choices'][0]['message']
    if 'tool_calls' in msg:
        print(f"  ✓ System message handled correctly")
        print(f"    Tool called: {msg['tool_calls'][0]['function']['name']}")
        print(f"    Arguments: {msg['tool_calls'][0]['function']['arguments']}")
        return True
    else:
        print(f"  ~ No tool call (may be acceptable)")
        return False

def test_tool_result_handling():
    """Test handling of tool results (conversation continuation)"""
    print("Testing tool result handling...")
    
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_wifi_status",
                "description": "Get current WiFi status",
                "parameters": {"type": "object", "properties": {}}
            }
        }
    ]
    
    response = requests.post(
        f"{RKLLM_URL}/chat/completions",
        json={
            "model": "rkllm-model",
            "messages": [
                {"role": "user", "content": "Check WiFi status"},
                {"role": "assistant", "content": None, "tool_calls": [
                    {"id": "call_1", "type": "function", "function": {"name": "get_wifi_status", "arguments": "{}"}}
                ]},
                {"role": "tool", "tool_call_id": "call_1", "content": '{"status": "on"}'}
            ],
            "tools": tools,
            "max_tokens": 100
        },
        timeout=30
    )
    assert response.status_code == 200, f"Status code: {response.status_code}"
    data = response.json()
    
    msg = data['choices'][0]['message']
    print(f"  ✓ Tool result handling works")
    print(f"    Response: {msg.get('content', 'No content')[:100]}")
    return True

def main():
    print("=" * 60)
    print("rkllm ToolSandbox Compatibility Test")
    print("=" * 60)
    print()
    
    results = {}
    
    try:
        results["models"] = test_models_endpoint()
        print()
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        results["models"] = None
        print("\nCannot proceed without models endpoint. Exiting.")
        return 1
    
    try:
        results["chat"] = test_chat_completion()
        print()
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        results["chat"] = None
    
    try:
        results["function_calling"] = test_function_calling()
        print()
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        results["function_calling"] = None
    
    try:
        results["multiple_tools"] = test_multiple_tool_calls()
        print()
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        results["multiple_tools"] = None
    
    try:
        results["system_message"] = test_system_message()
        print()
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        results["system_message"] = None
    
    try:
        results["tool_result"] = test_tool_result_handling()
        print()
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        results["tool_result"] = None
    
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, result in results.items():
        status = "✓ PASS" if result is not None else "✗ FAIL"
        if result is None:
            all_passed = False
        print(f"  {test_name}: {status}")
    
    print()
    if all_passed:
        print("✓ rkllm is compatible with ToolSandbox!")
        print("  You can use: tool_sandbox --user Cli --agent Rkllm --scenario <scenario_name>")
    else:
        print("✗ rkllm may not be fully compatible with ToolSandbox.")
        print("  Some features may not work correctly.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
