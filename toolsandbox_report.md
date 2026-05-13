# ToolSandbox Evaluation Report  [rkllm-model]

## 1. Overview

| Item | Value |
|------|-------|
| Model | `rkllm-model` |
| API Endpoint | `http://172.31.18.39:8080/v1` |
| Test Time | 2026-05-13 16:00:25 |
| API Connectivity | PASS |
| Total Test Cases | 24 |
| Passed | 16 |
| Pass Rate | 66.7% |
| Average Score | 0.733 |
| Average Latency | 19929 ms |
| Tool Call Accuracy | 66.7% |
| Tool Args Accuracy | 66.7% |

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
| 10 Distraction Tools | 2 | 2 | 100% | 1.00 | 28535ms | 100% | 100% |
| 3 Distraction Tools | 2 | 1 | 50% | 0.60 | 15268ms | 50% | 50% |
| All Tools Available | 2 | 0 | 0% | 0.20 | 60000ms | 0% | 0% |
| Canonicalization | 2 | 1 | 50% | 0.60 | 14233ms | 50% | 50% |
| Multi-Tool / State Dependency | 2 | 1 | 50% | 0.60 | 34667ms | 50% | 50% |
| No Tool Required | 1 | 1 | 100% | 1.00 | 6195ms | 100% | 100% |
| Single Tool Call - Contacts | 4 | 2 | 50% | 0.60 | 11641ms | 50% | 50% |
| Single Tool Call - Messaging | 2 | 2 | 100% | 1.00 | 20051ms | 100% | 100% |
| Single Tool Call - Search | 3 | 2 | 67% | 0.73 | 13697ms | 67% | 67% |
| Single Tool Call - Settings | 4 | 4 | 100% | 1.00 | 9732ms | 100% | 100% |

## 4. Detailed Test Results

| # | Test Name | Category | Score | Tool Call | Args | Response | Latency | Status |
|---|-----------|----------|-------|-----------|------|----------|---------|--------|
| 1 | cellular_off | Single Tool Call - Settings | 1.0 | Y | Y | Y | 10798ms | PASS |
| 2 | get_cellular | Single Tool Call - Settings | 1.0 | Y | Y | Y | 9505ms | PASS |
| 3 | wifi_off | Single Tool Call - Settings | 1.0 | Y | Y | Y | 9855ms | PASS |
| 4 | get_wifi | Single Tool Call - Settings | 1.0 | Y | Y | Y | 8769ms | PASS |
| 5 | search_phone_number_with_name | Single Tool Call - Contacts | 1.0 | Y | Y | Y | 14094ms | PASS |
| 6 | search_name_with_relationship | Single Tool Call - Contacts | 0.2 | N | N | Y | 7261ms | FAIL |
| 7 | search_relationship_with_phone_number | Single Tool Call - Contacts | 0.2 | N | N | Y | 6310ms | FAIL |
| 8 | add_contact_with_name_and_phone_number | Single Tool Call - Contacts | 1.0 | Y | Y | Y | 18900ms | PASS |
| 9 | send_message_with_phone_number_and_content | Single Tool Call - Messaging | 1.0 | Y | Y | Y | 24400ms | PASS |
| 10 | search_sender_phone_number_with_content | Single Tool Call - Messaging | 1.0 | Y | Y | Y | 15703ms | PASS |
| 11 | find_temperature | Single Tool Call - Search | 0.2 | N | N | Y | 12433ms | FAIL |
| 12 | find_stock_symbol | Single Tool Call - Search | 1.0 | Y | Y | Y | 10277ms | PASS |
| 13 | convert_currency | Single Tool Call - Search | 1.0 | Y | Y | Y | 18381ms | PASS |
| 14 | convert_currency_canonicalize | Canonicalization | 1.0 | Y | Y | Y | 17353ms | PASS |
| 15 | find_phone_number_with_location_name | Canonicalization | 0.2 | N | N | Y | 11113ms | FAIL |
| 16 | cellular_off_3_distraction | 3 Distraction Tools | 1.0 | Y | Y | Y | 16364ms | PASS |
| 17 | search_contacts_3_distraction | 3 Distraction Tools | 0.2 | N | N | Y | 14173ms | FAIL |
| 18 | wifi_off_10_distraction | 10 Distraction Tools | 1.0 | Y | Y | Y | 20937ms | PASS |
| 19 | send_message_10_distraction | 10 Distraction Tools | 1.0 | Y | Y | Y | 36132ms | PASS |
| 20 | cellular_off_all_tools | All Tools Available | 0.2 | N | N | Y | 96235ms | FAIL |
| 21 | search_contacts_all_tools | All Tools Available | 0.2 | N | N | Y | 23765ms | FAIL |
| 22 | send_message_with_contact_cellular_off | Multi-Tool / State Dependency | 0.2 | N | N | Y | 42364ms | FAIL |
| 23 | get_location_then_weather | Multi-Tool / State Dependency | 1.0 | Y | Y | Y | 26970ms | PASS |
| 24 | general_question_no_tool | No Tool Required | 1.0 | Y | Y | Y | 6195ms | PASS |

## 5. Detailed Per-Test Analysis

### 5.1 cellular_off

- **Category**: Single Tool Call - Settings
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 10798 ms
- **Tool calls found**: `[{"name": "set_cellular_service_status", "args": {"on": false}}]`
- **Final response**: Cellular service has been successfully turned off.
- **Detail**: All expected tool calls matched in order | Tools called: set_cellular_service_status | Response: Cellular service has been successfully turned off.

### 5.2 get_cellular

- **Category**: Single Tool Call - Settings
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 9505 ms
- **Tool calls found**: `[{"name": "get_cellular_service_status", "args": {}}]`
- **Final response**: Yes, your cellular service is currently on.
- **Detail**: All expected tool calls matched in order | Tools called: get_cellular_service_status | Response: Yes, your cellular service is currently on.

### 5.3 wifi_off

- **Category**: Single Tool Call - Settings
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 9855 ms
- **Tool calls found**: `[{"name": "set_wifi_status", "args": {"on": false}}]`
- **Final response**: WiFi has been successfully turned off.
- **Detail**: All expected tool calls matched in order | Tools called: set_wifi_status | Response: WiFi has been successfully turned off.

### 5.4 get_wifi

- **Category**: Single Tool Call - Settings
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 8769 ms
- **Tool calls found**: `[{"name": "get_wifi_status", "args": {}}]`
- **Final response**: Yes, your Wi-Fi is currently on.
- **Detail**: All expected tool calls matched in order | Tools called: get_wifi_status | Response: Yes, your Wi-Fi is currently on.

### 5.5 search_phone_number_with_name

- **Category**: Single Tool Call - Contacts
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 14094 ms
- **Tool calls found**: `[{"name": "search_contacts", "args": {"name": "Homer S"}}]`
- **Final response**: Homer S's phone number is +10000000000.
- **Detail**: All expected tool calls matched in order | Tools called: search_contacts | Response: Homer S's phone number is +10000000000.

### 5.6 search_name_with_relationship

- **Category**: Single Tool Call - Contacts
- **Score**: 0.2/1.0
- **Tool call correct**: No
- **Tool args correct**: No
- **Response relevant**: Yes
- **Latency**: 7261 ms
- **Final response**: I cannot determine your boss's name as no relevant information or contact details have been provided. Please provide more context or check your contacts directly.
- **Detail**: Missing expected tool call: search_contacts | No tool calls made | Response: I cannot determine your boss's name as no relevant information or contact details have been provided. Please provide more context or check your contacts directly.

### 5.7 search_relationship_with_phone_number

- **Category**: Single Tool Call - Contacts
- **Score**: 0.2/1.0
- **Tool call correct**: No
- **Tool args correct**: No
- **Response relevant**: Yes
- **Latency**: 6310 ms
- **Final response**: I cannot determine the user's relationship with a phone number without additional context. Please provide more details or clarify your request.
- **Detail**: Missing expected tool call: search_contacts | No tool calls made | Response: I cannot determine the user's relationship with a phone number without additional context. Please provide more details or clarify your request.

### 5.8 add_contact_with_name_and_phone_number

- **Category**: Single Tool Call - Contacts
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 18900 ms
- **Tool calls found**: `[{"name": "add_contact", "args": {"name": "Stephen Sondheim", "phone_number": "+19876543210"}}]`
- **Final response**: Stephen Sondheim has been successfully added to your contacts. Let me know if you need help with anything else!
- **Detail**: All expected tool calls matched in order | Tools called: add_contact | Response: Stephen Sondheim has been successfully added to your contacts. Let me know if you need help with anything else!

### 5.9 send_message_with_phone_number_and_content

- **Category**: Single Tool Call - Messaging
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 24400 ms
- **Tool calls found**: `[{"name": "send_message_with_phone_number", "args": {"phone_number": "+12453344098", "content": "How's the new album coming along"}}]`
- **Final response**: The message has been successfully sent to +12453344098. Let me know if there's anything else you'd like to do! 😊
- **Detail**: All expected tool calls matched in order | Tools called: send_message_with_phone_number | Response: The message has been successfully sent to +12453344098. Let me know if there's anything else you'd like to do! 😊

### 5.10 search_sender_phone_number_with_content

- **Category**: Single Tool Call - Messaging
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 15703 ms
- **Tool calls found**: `[{"name": "search_messages", "args": {"content": "want some GPUs"}}]`
- **Final response**: The phone number that asked if you want some GPUs is +18307976530.
- **Detail**: All expected tool calls matched in order | Tools called: search_messages | Response: The phone number that asked if you want some GPUs is +18307976530.

### 5.11 find_temperature

- **Category**: Single Tool Call - Search
- **Score**: 0.2/1.0
- **Tool call correct**: No
- **Tool args correct**: No
- **Response relevant**: Yes
- **Latency**: 12433 ms
- **Final response**: I can help you find the current weather temperature. Could you please provide your location (latitude and longitude) or let me know if you'd like to check the weather for a specific place?
- **Detail**: Missing expected tool call: search_weather_around_lat_lon | No tool calls made | Response: I can help you find the current weather temperature. Could you please provide your location (latitude and longitude) or let me know if you'd like to check the weather for a specific place?

### 5.12 find_stock_symbol

- **Category**: Single Tool Call - Search
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 10277 ms
- **Tool calls found**: `[{"name": "search_stock", "args": {"query": "Apple"}}]`
- **Final response**: The stock symbol for Apple is AAPL.
- **Detail**: All expected tool calls matched in order | Tools called: search_stock | Response: The stock symbol for Apple is AAPL.

### 5.13 convert_currency

- **Category**: Single Tool Call - Search
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 18381 ms
- **Tool calls found**: `[{"name": "convert_currency", "args": {"amount": 2048, "from_currency_code": "USD", "to_currency_code": "CNY"}}]`
- **Final response**: 2048 USD is equivalent to 14800 CNY.
- **Detail**: All expected tool calls matched in order | Tools called: convert_currency | Response: 2048 USD is equivalent to 14800 CNY.

### 5.14 convert_currency_canonicalize

- **Category**: Canonicalization
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 17353 ms
- **Tool calls found**: `[{"name": "convert_currency", "args": {"amount": 2048, "from_currency_code": "USD", "to_currency_code": "CNY"}}]`
- **Final response**: $2.048k (in USD) is equivalent to 14,800 CNY.
- **Detail**: All expected tool calls matched in order | Tools called: convert_currency | Response: $2.048k (in USD) is equivalent to 14,800 CNY.

### 5.15 find_phone_number_with_location_name

- **Category**: Canonicalization
- **Score**: 0.2/1.0
- **Tool call correct**: No
- **Tool args correct**: No
- **Response relevant**: Yes
- **Latency**: 11113 ms
- **Final response**: I cannot provide the phone number for Apple Park as it is not accessible through available tools or public data. Let me know if you'd like help with something else!
- **Detail**: Missing expected tool call: search_location_around_lat_lon | No tool calls made | Response: I cannot provide the phone number for Apple Park as it is not accessible through available tools or public data. Let me know if you'd like help with something else!

### 5.16 cellular_off_3_distraction

- **Category**: 3 Distraction Tools
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 16364 ms
- **Tool calls found**: `[{"name": "set_cellular_service_status", "args": {"on": false}}]`
- **Final response**: Cellular service has been successfully turned off. Let me know if you need any further assistance! 😊
- **Detail**: All expected tool calls matched in order | Tools called: set_cellular_service_status | Response: Cellular service has been successfully turned off. Let me know if you need any further assistance! 😊

### 5.17 search_contacts_3_distraction

- **Category**: 3 Distraction Tools
- **Score**: 0.2/1.0
- **Tool call correct**: No
- **Tool args correct**: No
- **Response relevant**: Yes
- **Latency**: 14173 ms
- **Final response**: I cannot find Homer S's phone number as no tool is available for looking up contact information by name. Please let me know if there's another way I can assist!
- **Detail**: Missing expected tool call: search_contacts | No tool calls made | Response: I cannot find Homer S's phone number as no tool is available for looking up contact information by name. Please let me know if there's another way I can assist!

### 5.18 wifi_off_10_distraction

- **Category**: 10 Distraction Tools
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 20937 ms
- **Tool calls found**: `[{"name": "set_wifi_status", "args": {"on": false}}]`
- **Final response**: WiFi has been successfully turned off.
- **Detail**: All expected tool calls matched in order | Tools called: set_wifi_status | Response: WiFi has been successfully turned off.

### 5.19 send_message_10_distraction

- **Category**: 10 Distraction Tools
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 36132 ms
- **Tool calls found**: `[{"name": "send_message_with_phone_number", "args": {"phone_number": "+12453344098", "content": "How's the new album coming along"}}]`
- **Final response**: The message has been successfully sent to +12453344098. Let me know if you need help with anything else!
- **Detail**: All expected tool calls matched in order | Tools called: send_message_with_phone_number | Response: The message has been successfully sent to +12453344098. Let me know if you need help with anything else!

### 5.20 cellular_off_all_tools

- **Category**: All Tools Available
- **Score**: 0.2/1.0
- **Tool call correct**: No
- **Tool args correct**: No
- **Response relevant**: Yes
- **Latency**: 96235 ms
- **Final response**: I'm ready to assist you with your requests. What would you like to do? For example:

- Check device status (cellular, Wi-Fi, location)
- Search for contacts or messages
- Set reminders or alarms
- Find weather, locations, or stock information
- Make phone calls or send messages
- Perform currency conversions or search holidays

Please let me know your specific request!
- **Detail**: Missing expected tool call: set_cellular_service_status | No tool calls made | Response: I'm ready to assist you with your requests. What would you like to do? For example:

- Check device status (cellular, Wi-Fi, location)
- Search for contacts or messages
- Set reminders or alarms
- Fin

### 5.21 search_contacts_all_tools

- **Category**: All Tools Available
- **Score**: 0.2/1.0
- **Tool call correct**: No
- **Tool args correct**: No
- **Response relevant**: Yes
- **Latency**: 23765 ms
- **Final response**: I'm ready to assist you with any requests. What would you like to do? For example:

- Check device status (cellular, WiFi, location)
- Search for contacts or messages
- Set reminders or alarms
- Get weather or location information
- Make calls or send messages
- Perform financial conversions

Please let me know your specific request!
- **Detail**: Missing expected tool call: search_contacts | No tool calls made | Response: I'm ready to assist you with any requests. What would you like to do? For example:

- Check device status (cellular, WiFi, location)
- Search for contacts or messages
- Set reminders or alarms
- Get w

### 5.22 send_message_with_contact_cellular_off

- **Category**: Multi-Tool / State Dependency
- **Score**: 0.2/1.0
- **Tool call correct**: No
- **Tool args correct**: No
- **Response relevant**: Yes
- **Latency**: 42364 ms
- **Tool calls found**: `[{"name": "set_cellular_service_status", "args": {"on": false}}, {"name": "send_message_with_phone_number", "args": {"phone_number": "123-456-7890", "content": "Meeting at 3pm"}}]`
- **Final response**: Cellular service has been turned off, and a message stating "Meeting at 3pm" has been successfully sent to Homer S.
- **Detail**: Missing expected tool call: search_contacts | Tools called: set_cellular_service_status, send_message_with_phone_number | Response: Cellular service has been turned off, and a message stating "Meeting at 3pm" has been successfully sent to Homer S.

### 5.23 get_location_then_weather

- **Category**: Multi-Tool / State Dependency
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 26970 ms
- **Tool calls found**: `[{"name": "get_current_location", "args": {}}, {"name": "search_weather_around_lat_lon", "args": {"latitude": 37.334606, "longitude": -122.009102}}]`
- **Final response**: The weather at your current location is sunny with a temperature of 22.5°C.
- **Detail**: All expected tool calls matched in order | Tools called: get_current_location, search_weather_around_lat_lon | Response: The weather at your current location is sunny with a temperature of 22.5°C.

### 5.24 general_question_no_tool

- **Category**: No Tool Required
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 6195 ms
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