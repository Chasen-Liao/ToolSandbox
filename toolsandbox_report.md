# ToolSandbox Evaluation Report  [rkllm-model]

## 1. Overview

| Item | Value |
|------|-------|
| Model | `rkllm-model` |
| API Endpoint | `http://172.31.18.39:8080/v1` |
| Test Time | 2026-05-18 16:44:36 |
| API Connectivity | PASS |
| Total Test Cases | 24 |
| Passed | 17 |
| Pass Rate | 70.8% |
| Average Score | 0.767 |
| Average Latency | 21406 ms |
| Tool Call Accuracy | 70.8% |
| Tool Args Accuracy | 70.8% |

## 2. Scoring Methodology

Each test case is scored on a 0-1 scale:

| Component | Weight | Description |
|-----------|--------|-------------|
| Correct tool call | 0.5 | All expected tool calls are made in order |
| Correct arguments | 0.3 | Expected argument subsets match the corresponding tool calls |
| Relevant response | 0.2 | The final assistant response contains a non-empty relevant answer |

A test is considered **PASS** if the score >= 0.5.

## 3. Results by Category

| Category | Tests | Passed | Pass Rate | Avg Score | Avg Latency | Tool Call Acc | Tool Args Acc |
|----------|-------|--------|-----------|-----------|-------------|---------------|---------------|
| 10 Distraction Tools | 2 | 2 | 100% | 1.00 | 28430ms | 100% | 100% |
| 3 Distraction Tools | 2 | 1 | 50% | 0.60 | 13471ms | 50% | 50% |
| All Tools Available | 2 | 0 | 0% | 0.20 | 73029ms | 0% | 0% |
| Canonicalization | 2 | 1 | 50% | 0.60 | 14009ms | 50% | 50% |
| Multi-Tool / State Dependency | 2 | 1 | 50% | 0.60 | 34841ms | 50% | 50% |
| No Tool Required | 1 | 1 | 100% | 1.00 | 6177ms | 100% | 100% |
| Single Tool Call - Contacts | 4 | 3 | 75% | 0.80 | 15506ms | 75% | 75% |
| Single Tool Call - Messaging | 2 | 2 | 100% | 1.00 | 19426ms | 100% | 100% |
| Single Tool Call - Search | 3 | 2 | 67% | 0.73 | 13561ms | 67% | 67% |
| Single Tool Call - Settings | 4 | 4 | 100% | 1.00 | 9608ms | 100% | 100% |

## 4. Detailed Test Results

| # | Test Name | Category | Score | Tool Call | Args | Response | Latency | Status |
|---|-----------|----------|-------|-----------|------|----------|---------|--------|
| 1 | cellular_off | Single Tool Call - Settings | 1.0 | Y | Y | Y | 10539ms | PASS |
| 2 | get_cellular | Single Tool Call - Settings | 1.0 | Y | Y | Y | 9349ms | PASS |
| 3 | wifi_off | Single Tool Call - Settings | 1.0 | Y | Y | Y | 9910ms | PASS |
| 4 | get_wifi | Single Tool Call - Settings | 1.0 | Y | Y | Y | 8635ms | PASS |
| 5 | search_phone_number_with_name | Single Tool Call - Contacts | 1.0 | Y | Y | Y | 14182ms | PASS |
| 6 | search_name_with_relationship | Single Tool Call - Contacts | 0.2 | N | N | Y | 13597ms | FAIL |
| 7 | search_relationship_with_phone_number | Single Tool Call - Contacts | 1.0 | Y | Y | Y | 14893ms | PASS |
| 8 | add_contact_with_name_and_phone_number | Single Tool Call - Contacts | 1.0 | Y | Y | Y | 19354ms | PASS |
| 9 | send_message_with_phone_number_and_content | Single Tool Call - Messaging | 1.0 | Y | Y | Y | 23152ms | PASS |
| 10 | search_sender_phone_number_with_content | Single Tool Call - Messaging | 1.0 | Y | Y | Y | 15701ms | PASS |
| 11 | find_temperature | Single Tool Call - Search | 0.2 | N | N | Y | 12456ms | FAIL |
| 12 | find_stock_symbol | Single Tool Call - Search | 1.0 | Y | Y | Y | 10080ms | PASS |
| 13 | convert_currency | Single Tool Call - Search | 1.0 | Y | Y | Y | 18148ms | PASS |
| 14 | convert_currency_canonicalize | Canonicalization | 1.0 | Y | Y | Y | 16611ms | PASS |
| 15 | find_phone_number_with_location_name | Canonicalization | 0.2 | N | N | Y | 11408ms | FAIL |
| 16 | cellular_off_3_distraction | 3 Distraction Tools | 1.0 | Y | Y | Y | 13037ms | PASS |
| 17 | search_contacts_3_distraction | 3 Distraction Tools | 0.2 | N | N | Y | 13906ms | FAIL |
| 18 | wifi_off_10_distraction | 10 Distraction Tools | 1.0 | Y | Y | Y | 20922ms | PASS |
| 19 | send_message_10_distraction | 10 Distraction Tools | 1.0 | Y | Y | Y | 35937ms | PASS |
| 20 | cellular_off_all_tools | All Tools Available | 0.2 | N | N | Y | 111646ms | FAIL |
| 21 | search_contacts_all_tools | All Tools Available | 0.2 | N | N | Y | 34413ms | FAIL |
| 22 | send_message_with_contact_cellular_off | Multi-Tool / State Dependency | 0.2 | N | N | Y | 42274ms | FAIL |
| 23 | get_location_then_weather | Multi-Tool / State Dependency | 1.0 | Y | Y | Y | 27408ms | PASS |
| 24 | general_question_no_tool | No Tool Required | 1.0 | Y | Y | Y | 6177ms | PASS |

## 5. Detailed Per-Test Analysis

### 5.1 cellular_off

- **Category**: Single Tool Call - Settings
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 10539 ms
- **Tool calls found**: `[{"name": "set_cellular_service_status", "args": {"on": false}}]`
- **Final response**: Cellular service has been successfully turned off.
- **Detail**: All expected tool calls matched in order | Tools called: set_cellular_service_status | Response: Cellular service has been successfully turned off.

### 5.2 get_cellular

- **Category**: Single Tool Call - Settings
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 9349 ms
- **Tool calls found**: `[{"name": "get_cellular_service_status", "args": {}}]`
- **Final response**: Yes, your cellular service is currently on.
- **Detail**: All expected tool calls matched in order | Tools called: get_cellular_service_status | Response: Yes, your cellular service is currently on.

### 5.3 wifi_off

- **Category**: Single Tool Call - Settings
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 9910 ms
- **Tool calls found**: `[{"name": "set_wifi_status", "args": {"on": false}}]`
- **Final response**: Wi-Fi has been successfully turned off.
- **Detail**: All expected tool calls matched in order | Tools called: set_wifi_status | Response: Wi-Fi has been successfully turned off.

### 5.4 get_wifi

- **Category**: Single Tool Call - Settings
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 8635 ms
- **Tool calls found**: `[{"name": "get_wifi_status", "args": {}}]`
- **Final response**: Yes, your WiFi is currently on.
- **Detail**: All expected tool calls matched in order | Tools called: get_wifi_status | Response: Yes, your WiFi is currently on.

### 5.5 search_phone_number_with_name

- **Category**: Single Tool Call - Contacts
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 14182 ms
- **Tool calls found**: `[{"name": "search_contacts", "args": {"name": "Homer S"}}]`
- **Final response**: Homer S's phone number is +10000000000.
- **Detail**: All expected tool calls matched in order | Tools called: search_contacts | Response: Homer S's phone number is +10000000000.

### 5.6 search_name_with_relationship

- **Category**: Single Tool Call - Contacts
- **Score**: 0.2/1.0
- **Tool call correct**: No
- **Tool args correct**: No
- **Response relevant**: Yes
- **Latency**: 13597 ms
- **Final response**: I cannot determine your boss's name without additional information or access to your contact list. Could you provide more context or details about your boss, such as their department or relationship to you? If needed, I can help search your contacts for relevant information. Let me know!
- **Detail**: Missing expected tool call: search_contacts | No tool calls made | Response: I cannot determine your boss's name without additional information or access to your contact list. Could you provide more context or details about your boss, such as their department or relationship t

### 5.7 search_relationship_with_phone_number

- **Category**: Single Tool Call - Contacts
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 14893 ms
- **Tool calls found**: `[{"name": "search_contacts", "args": {"phone_number": "+10000000000"}}]`
- **Final response**: Your relationship with +10000000000 is that you are Homer S's boss.
- **Detail**: All expected tool calls matched in order | Tools called: search_contacts | Response: Your relationship with +10000000000 is that you are Homer S's boss.

### 5.8 add_contact_with_name_and_phone_number

- **Category**: Single Tool Call - Contacts
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 19354 ms
- **Tool calls found**: `[{"name": "add_contact", "args": {"name": "Stephen Sondheim", "phone_number": "+19876543210"}}]`
- **Final response**: Stephen Sondheim has been successfully added to your contacts. Let me know if you need help with anything else! 😊
- **Detail**: All expected tool calls matched in order | Tools called: add_contact | Response: Stephen Sondheim has been successfully added to your contacts. Let me know if you need help with anything else! 😊

### 5.9 send_message_with_phone_number_and_content

- **Category**: Single Tool Call - Messaging
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 23152 ms
- **Tool calls found**: `[{"name": "send_message_with_phone_number", "args": {"phone_number": "+12453344098", "content": "How's the new album coming along"}}]`
- **Final response**: The message has been successfully sent to +12453344098. Let me know if you need help with anything else!
- **Detail**: All expected tool calls matched in order | Tools called: send_message_with_phone_number | Response: The message has been successfully sent to +12453344098. Let me know if you need help with anything else!

### 5.10 search_sender_phone_number_with_content

- **Category**: Single Tool Call - Messaging
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 15701 ms
- **Tool calls found**: `[{"name": "search_messages", "args": {"content": "want some GPUs"}}]`
- **Final response**: The phone number that asked you if you want some GPUs is +18307976530.
- **Detail**: All expected tool calls matched in order | Tools called: search_messages | Response: The phone number that asked you if you want some GPUs is +18307976530.

### 5.11 find_temperature

- **Category**: Single Tool Call - Search
- **Score**: 0.2/1.0
- **Tool call correct**: No
- **Tool args correct**: No
- **Response relevant**: Yes
- **Latency**: 12456 ms
- **Final response**: I can help you find the current weather temperature. Could you please provide your location (latitude and longitude) or let me know if you'd like me to check the weather for a specific place?
- **Detail**: Missing expected tool call: search_weather_around_lat_lon | No tool calls made | Response: I can help you find the current weather temperature. Could you please provide your location (latitude and longitude) or let me know if you'd like me to check the weather for a specific place?

### 5.12 find_stock_symbol

- **Category**: Single Tool Call - Search
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 10080 ms
- **Tool calls found**: `[{"name": "search_stock", "args": {"query": "Apple"}}]`
- **Final response**: The stock symbol for Apple is AAPL.
- **Detail**: All expected tool calls matched in order | Tools called: search_stock | Response: The stock symbol for Apple is AAPL.

### 5.13 convert_currency

- **Category**: Single Tool Call - Search
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 18148 ms
- **Tool calls found**: `[{"name": "convert_currency", "args": {"amount": 2048, "from_currency_code": "USD", "to_currency_code": "CNY"}}]`
- **Final response**: 2048 USD is equivalent to 14800 CNY.
- **Detail**: All expected tool calls matched in order | Tools called: convert_currency | Response: 2048 USD is equivalent to 14800 CNY.

### 5.14 convert_currency_canonicalize

- **Category**: Canonicalization
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 16611 ms
- **Tool calls found**: `[{"name": "convert_currency", "args": {"amount": 2048, "from_currency_code": "USD", "to_currency_code": "CNY"}}]`
- **Final response**: $2.048k (USD) is equivalent to 14,800 CNY.
- **Detail**: All expected tool calls matched in order | Tools called: convert_currency | Response: $2.048k (USD) is equivalent to 14,800 CNY.

### 5.15 find_phone_number_with_location_name

- **Category**: Canonicalization
- **Score**: 0.2/1.0
- **Tool call correct**: No
- **Tool args correct**: No
- **Response relevant**: Yes
- **Latency**: 11408 ms
- **Final response**: I cannot provide the phone number for Apple Park. It is not publicly accessible or available through standard tools or databases. Let me know if you'd like assistance with something else!
- **Detail**: Missing expected tool call: search_location_around_lat_lon | No tool calls made | Response: I cannot provide the phone number for Apple Park. It is not publicly accessible or available through standard tools or databases. Let me know if you'd like assistance with something else!

### 5.16 cellular_off_3_distraction

- **Category**: 3 Distraction Tools
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 13037 ms
- **Tool calls found**: `[{"name": "set_cellular_service_status", "args": {"on": false}}]`
- **Final response**: Cellular service has been successfully turned off.
- **Detail**: All expected tool calls matched in order | Tools called: set_cellular_service_status | Response: Cellular service has been successfully turned off.

### 5.17 search_contacts_3_distraction

- **Category**: 3 Distraction Tools
- **Score**: 0.2/1.0
- **Tool call correct**: No
- **Tool args correct**: No
- **Response relevant**: Yes
- **Latency**: 13906 ms
- **Final response**: I cannot find Homer S's phone number as none of the available tools allow me to retrieve contact information directly. Let me know if there’s another way I can assist!
- **Detail**: Missing expected tool call: search_contacts | No tool calls made | Response: I cannot find Homer S's phone number as none of the available tools allow me to retrieve contact information directly. Let me know if there’s another way I can assist!

### 5.18 wifi_off_10_distraction

- **Category**: 10 Distraction Tools
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 20922 ms
- **Tool calls found**: `[{"name": "set_wifi_status", "args": {"on": false}}]`
- **Final response**: Wi-Fi has been successfully turned off.
- **Detail**: All expected tool calls matched in order | Tools called: set_wifi_status | Response: Wi-Fi has been successfully turned off.

### 5.19 send_message_10_distraction

- **Category**: 10 Distraction Tools
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 35937 ms
- **Tool calls found**: `[{"name": "send_message_with_phone_number", "args": {"phone_number": "+12453344098", "content": "How's the new album coming along"}}]`
- **Final response**: The message has been successfully sent to +12453344098. Let me know if you need help with anything else!
- **Detail**: All expected tool calls matched in order | Tools called: send_message_with_phone_number | Response: The message has been successfully sent to +12453344098. Let me know if you need help with anything else!

### 5.20 cellular_off_all_tools

- **Category**: All Tools Available
- **Score**: 0.2/1.0
- **Tool call correct**: No
- **Tool args correct**: No
- **Response relevant**: Yes
- **Latency**: 111646 ms
- **Final response**: I'm ready to help you with any tasks or queries you might have. What would you like to do? For example, you can ask me to:

- Check your device's cellular, Wi-Fi, or location services status
- Search for contacts or messages
- Set a reminder or alarm
- Send a message, email, or make a phone call
- Find weather, stock prices, holidays, or locations
- Convert currency
- Play music
- Take a photo
- Open an app

Just let me know what you need! 😊
- **Detail**: Missing expected tool call: set_cellular_service_status | No tool calls made | Response: I'm ready to help you with any tasks or queries you might have. What would you like to do? For example, you can ask me to:

- Check your device's cellular, Wi-Fi, or location services status
- Search 

### 5.21 search_contacts_all_tools

- **Category**: All Tools Available
- **Score**: 0.2/1.0
- **Tool call correct**: No
- **Tool args correct**: No
- **Response relevant**: Yes
- **Latency**: 34413 ms
- **Final response**: I'm ready to help you with any requests or tasks you might have! Could you please let me know what you'd like to do? For example:

- Check the status of cellular, Wi-Fi, or location services
- Search for contacts or messages
- Set reminders, alarms, or calendar events
- Make phone calls or send messages
- Search for weather, locations, stocks, holidays, or currency conversions
- Play music or take photos
- Open apps

Just let me know your request! 😊
- **Detail**: Missing expected tool call: search_contacts | No tool calls made | Response: I'm ready to help you with any requests or tasks you might have! Could you please let me know what you'd like to do? For example:

- Check the status of cellular, Wi-Fi, or location services
- Search 

### 5.22 send_message_with_contact_cellular_off

- **Category**: Multi-Tool / State Dependency
- **Score**: 0.2/1.0
- **Tool call correct**: No
- **Tool args correct**: No
- **Response relevant**: Yes
- **Latency**: 42274 ms
- **Tool calls found**: `[{"name": "set_cellular_service_status", "args": {"on": false}}, {"name": "send_message_with_phone_number", "args": {"phone_number": "123-456-7890", "content": "Meeting at 3pm."}}]`
- **Final response**: Cellular service has been turned off, and the message "Meeting at 3pm." has been successfully sent to Homer S.
- **Detail**: Missing expected tool call: search_contacts | Tools called: set_cellular_service_status, send_message_with_phone_number | Response: Cellular service has been turned off, and the message "Meeting at 3pm." has been successfully sent to Homer S.

### 5.23 get_location_then_weather

- **Category**: Multi-Tool / State Dependency
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 27408 ms
- **Tool calls found**: `[{"name": "get_current_location", "args": {}}, {"name": "search_weather_around_lat_lon", "args": {"latitude": 37.334606, "longitude": -122.009102}}]`
- **Final response**: The weather at your current location is sunny with a temperature of 22.5°C.
- **Detail**: All expected tool calls matched in order | Tools called: get_current_location, search_weather_around_lat_lon | Response: The weather at your current location is sunny with a temperature of 22.5°C.

### 5.24 general_question_no_tool

- **Category**: No Tool Required
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 6177 ms
- **Final response**: The capital of France is Paris.
- **Detail**: No tool call expected and none made | No tool calls made | Response: The capital of France is Paris.

## 6. Test Environment

| Item | Value |
|------|-------|
| OS | Windows |
| Python | 3.13.7 |
| API Protocol | OpenAI-compatible (v1/chat/completions) |
| Model | rkllm-model |
| Base URL | http://172.31.18.39:8080/v1 |
| Temperature | 0.0 |
| Max Tokens | 512 |
| Max Retries | 2 |
| Request Timeout | 60s |

---

*Report generated by ToolSandbox evaluation script.*