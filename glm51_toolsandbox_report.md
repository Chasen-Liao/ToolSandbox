# ToolSandbox Evaluation Report  [glm-5.1]

## 1. Overview

| Item | Value |
|------|-------|
| Model | `glm-5.1` |
| API Endpoint | `https://ark.cn-beijing.volces.com/api/coding/v3` |
| Test Time | 2026-05-13 16:09:58 |
| API Connectivity | PASS |
| Total Test Cases | 24 |
| Passed | 20 |
| Pass Rate | 83.3% |
| Average Score | 0.842 |
| Average Latency | 8723 ms |
| Tool Call Accuracy | 83.3% |
| Tool Args Accuracy | 83.3% |

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
| 10 Distraction Tools | 2 | 2 | 100% | 1.00 | 9006ms | 100% | 100% |
| 3 Distraction Tools | 2 | 2 | 100% | 1.00 | 4804ms | 100% | 100% |
| All Tools Available | 2 | 2 | 100% | 1.00 | 19108ms | 100% | 100% |
| Canonicalization | 2 | 2 | 100% | 1.00 | 9721ms | 100% | 100% |
| Multi-Tool / State Dependency | 2 | 1 | 50% | 0.50 | 16426ms | 50% | 50% |
| No Tool Required | 1 | 1 | 100% | 1.00 | 4808ms | 100% | 100% |
| Single Tool Call - Contacts | 4 | 4 | 100% | 1.00 | 6858ms | 100% | 100% |
| Single Tool Call - Messaging | 2 | 2 | 100% | 1.00 | 8897ms | 100% | 100% |
| Single Tool Call - Search | 3 | 2 | 67% | 0.73 | 6583ms | 67% | 67% |
| Single Tool Call - Settings | 4 | 2 | 50% | 0.50 | 5362ms | 50% | 50% |

## 4. Detailed Test Results

| # | Test Name | Category | Score | Tool Call | Args | Response | Latency | Status |
|---|-----------|----------|-------|-----------|------|----------|---------|--------|
| 1 | cellular_off | Single Tool Call - Settings | 1.0 | Y | Y | Y | 4711ms | PASS |
| 2 | get_cellular | Single Tool Call - Settings | 0.0 | N | N | N | 7803ms | FAIL |
| 3 | wifi_off | Single Tool Call - Settings | 1.0 | Y | Y | Y | 7163ms | PASS |
| 4 | get_wifi | Single Tool Call - Settings | 0.0 | N | N | N | 1769ms | FAIL |
| 5 | search_phone_number_with_name | Single Tool Call - Contacts | 1.0 | Y | Y | Y | 5657ms | PASS |
| 6 | search_name_with_relationship | Single Tool Call - Contacts | 1.0 | Y | Y | Y | 6956ms | PASS |
| 7 | search_relationship_with_phone_number | Single Tool Call - Contacts | 1.0 | Y | Y | Y | 8239ms | PASS |
| 8 | add_contact_with_name_and_phone_number | Single Tool Call - Contacts | 1.0 | Y | Y | Y | 6580ms | PASS |
| 9 | send_message_with_phone_number_and_content | Single Tool Call - Messaging | 1.0 | Y | Y | Y | 13460ms | PASS |
| 10 | search_sender_phone_number_with_content | Single Tool Call - Messaging | 1.0 | Y | Y | Y | 4333ms | PASS |
| 11 | find_temperature | Single Tool Call - Search | 0.2 | N | N | Y | 3033ms | FAIL |
| 12 | find_stock_symbol | Single Tool Call - Search | 1.0 | Y | Y | Y | 8176ms | PASS |
| 13 | convert_currency | Single Tool Call - Search | 1.0 | Y | Y | Y | 8542ms | PASS |
| 14 | convert_currency_canonicalize | Canonicalization | 1.0 | Y | Y | Y | 6502ms | PASS |
| 15 | find_phone_number_with_location_name | Canonicalization | 1.0 | Y | Y | Y | 12940ms | PASS |
| 16 | cellular_off_3_distraction | 3 Distraction Tools | 1.0 | Y | Y | Y | 3854ms | PASS |
| 17 | search_contacts_3_distraction | 3 Distraction Tools | 1.0 | Y | Y | Y | 5754ms | PASS |
| 18 | wifi_off_10_distraction | 10 Distraction Tools | 1.0 | Y | Y | Y | 13291ms | PASS |
| 19 | send_message_10_distraction | 10 Distraction Tools | 1.0 | Y | Y | Y | 4721ms | PASS |
| 20 | cellular_off_all_tools | All Tools Available | 1.0 | Y | Y | Y | 20296ms | PASS |
| 21 | search_contacts_all_tools | All Tools Available | 1.0 | Y | Y | Y | 17920ms | PASS |
| 22 | send_message_with_contact_cellular_off | Multi-Tool / State Dependency | 1.0 | Y | Y | Y | 27548ms | PASS |
| 23 | get_location_then_weather | Multi-Tool / State Dependency | 0.0 | N | N | N | 5305ms | FAIL |
| 24 | general_question_no_tool | No Tool Required | 1.0 | Y | Y | Y | 4808ms | PASS |

## 5. Detailed Per-Test Analysis

### 5.1 cellular_off

- **Category**: Single Tool Call - Settings
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 4711 ms
- **Tool calls found**: `[{"name": "set_cellular_service_status", "args": {"on": false}}]`
- **Final response**: Cellular service has been turned off.
- **Detail**: All expected tool calls matched in order | Tools called: set_cellular_service_status | Response: Cellular service has been turned off.

### 5.2 get_cellular

- **Category**: Single Tool Call - Settings
- **Score**: 0.0/1.0
- **Tool call correct**: No
- **Tool args correct**: No
- **Response relevant**: No
- **Latency**: 7803 ms
- **Detail**: Missing expected tool call: get_cellular_service_status | No tool calls made
- **Error**: JSONDecodeError: Expecting value: line 1 column 1 (char 0)

### 5.3 wifi_off

- **Category**: Single Tool Call - Settings
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 7163 ms
- **Tool calls found**: `[{"name": "set_wifi_status", "args": {"on": false}}]`
- **Final response**: Wi-Fi has been turned off successfully.
- **Detail**: All expected tool calls matched in order | Tools called: set_wifi_status | Response: Wi-Fi has been turned off successfully.

### 5.4 get_wifi

- **Category**: Single Tool Call - Settings
- **Score**: 0.0/1.0
- **Tool call correct**: No
- **Tool args correct**: No
- **Response relevant**: No
- **Latency**: 1769 ms
- **Detail**: Missing expected tool call: get_wifi_status | No tool calls made
- **Error**: JSONDecodeError: Expecting value: line 1 column 1 (char 0)

### 5.5 search_phone_number_with_name

- **Category**: Single Tool Call - Contacts
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 5657 ms
- **Tool calls found**: `[{"name": "search_contacts", "args": {"name": "Homer S"}}]`
- **Final response**: Homer S's phone number is **+10000000000**.
- **Detail**: All expected tool calls matched in order | Tools called: search_contacts | Response: Homer S's phone number is **+10000000000**.

### 5.6 search_name_with_relationship

- **Category**: Single Tool Call - Contacts
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 6956 ms
- **Tool calls found**: `[{"name": "search_contacts", "args": {"relationship": "boss"}}]`
- **Final response**: Your boss's name is **Homer S**.
- **Detail**: All expected tool calls matched in order | Tools called: search_contacts | Response: Your boss's name is **Homer S**.

### 5.7 search_relationship_with_phone_number

- **Category**: Single Tool Call - Contacts
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 8239 ms
- **Tool calls found**: `[{"name": "search_contacts", "args": {"phone_number": "+10000000000"}}]`
- **Final response**: The phone number +10000000000 belongs to **Homer S**, and your relationship with them is **boss**.
- **Detail**: All expected tool calls matched in order | Tools called: search_contacts | Response: The phone number +10000000000 belongs to **Homer S**, and your relationship with them is **boss**.

### 5.8 add_contact_with_name_and_phone_number

- **Category**: Single Tool Call - Contacts
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 6580 ms
- **Tool calls found**: `[{"name": "add_contact", "args": {"name": "Stephen Sondheim", "phone_number": "+19876543210"}}]`
- **Final response**: Stephen Sondheim has been added to your contacts with the phone number +19876543210.
- **Detail**: All expected tool calls matched in order | Tools called: add_contact | Response: Stephen Sondheim has been added to your contacts with the phone number +19876543210.

### 5.9 send_message_with_phone_number_and_content

- **Category**: Single Tool Call - Messaging
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 13460 ms
- **Tool calls found**: `[{"name": "send_message_with_phone_number", "args": {"phone_number": "+12453344098", "content": "How's the new album coming along"}}]`
- **Final response**: Message sent successfully to +12453344098! The message "How's the new album coming along" has been delivered.
- **Detail**: All expected tool calls matched in order | Tools called: send_message_with_phone_number | Response: Message sent successfully to +12453344098! The message "How's the new album coming along" has been delivered.

### 5.10 search_sender_phone_number_with_content

- **Category**: Single Tool Call - Messaging
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 4333 ms
- **Tool calls found**: `[{"name": "search_messages", "args": {"content": "GPUs"}}]`
- **Final response**: The phone number **+18307976530** asked you if you want some GPUs.
- **Detail**: All expected tool calls matched in order | Tools called: search_messages | Response: The phone number **+18307976530** asked you if you want some GPUs.

### 5.11 find_temperature

- **Category**: Single Tool Call - Search
- **Score**: 0.2/1.0
- **Tool call correct**: No
- **Tool args correct**: No
- **Response relevant**: Yes
- **Latency**: 3033 ms
- **Final response**: I'd be happy to check the temperature for you! However, I don't have access to your current location. Could you please share your city or your latitude and longitude so I can look up the weather for you?
- **Detail**: Missing expected tool call: search_weather_around_lat_lon | No tool calls made | Response: I'd be happy to check the temperature for you! However, I don't have access to your current location. Could you please share your city or your latitude and longitude so I can look up the weather for y

### 5.12 find_stock_symbol

- **Category**: Single Tool Call - Search
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 8176 ms
- **Tool calls found**: `[{"name": "search_stock", "args": {"query": "Apple"}}]`
- **Final response**: The stock symbol for Apple Inc. is **AAPL**.
- **Detail**: All expected tool calls matched in order | Tools called: search_stock | Response: The stock symbol for Apple Inc. is **AAPL**.

### 5.13 convert_currency

- **Category**: Single Tool Call - Search
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 8542 ms
- **Tool calls found**: `[{"name": "convert_currency", "args": {"amount": 2048, "from_currency_code": "USD", "to_currency_code": "CNY"}}]`
- **Final response**: 2048 USD is equivalent to **14,800.00 CNY** based on the current exchange rate.
- **Detail**: All expected tool calls matched in order | Tools called: convert_currency | Response: 2048 USD is equivalent to **14,800.00 CNY** based on the current exchange rate.

### 5.14 convert_currency_canonicalize

- **Category**: Canonicalization
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 6502 ms
- **Tool calls found**: `[{"name": "convert_currency", "args": {"amount": 2048, "from_currency_code": "USD", "to_currency_code": "CNY"}}]`
- **Final response**: $2,048 USD is equivalent to **14,800.00 CNY**.
- **Detail**: All expected tool calls matched in order | Tools called: convert_currency | Response: $2,048 USD is equivalent to **14,800.00 CNY**.

### 5.15 find_phone_number_with_location_name

- **Category**: Canonicalization
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 12940 ms
- **Tool calls found**: `[{"name": "search_location_around_lat_lon", "args": {"location": "Apple Park"}}]`
- **Final response**: The phone number for **Apple Park** is **+1 (408) 996-1010**. It's located at 1 Apple Park Way, Cupertino, CA 95014.
- **Detail**: All expected tool calls matched in order | Tools called: search_location_around_lat_lon | Response: The phone number for **Apple Park** is **+1 (408) 996-1010**. It's located at 1 Apple Park Way, Cupertino, CA 95014.

### 5.16 cellular_off_3_distraction

- **Category**: 3 Distraction Tools
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 3854 ms
- **Tool calls found**: `[{"name": "set_cellular_service_status", "args": {"on": false}}]`
- **Final response**: Cellular service has been turned off.
- **Detail**: All expected tool calls matched in order | Tools called: set_cellular_service_status | Response: Cellular service has been turned off.

### 5.17 search_contacts_3_distraction

- **Category**: 3 Distraction Tools
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 5754 ms
- **Tool calls found**: `[{"name": "search_contacts", "args": {"name": "Homer S"}}]`
- **Final response**: Homer S's phone number is **+10000000000**.
- **Detail**: All expected tool calls matched in order | Tools called: search_contacts | Response: Homer S's phone number is **+10000000000**.

### 5.18 wifi_off_10_distraction

- **Category**: 10 Distraction Tools
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 13291 ms
- **Tool calls found**: `[{"name": "set_wifi_status", "args": {"on": false}}]`
- **Final response**: Wi-Fi has been turned off successfully.
- **Detail**: All expected tool calls matched in order | Tools called: set_wifi_status | Response: Wi-Fi has been turned off successfully.

### 5.19 send_message_10_distraction

- **Category**: 10 Distraction Tools
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 4721 ms
- **Tool calls found**: `[{"name": "send_message_with_phone_number", "args": {"phone_number": "+12453344098", "content": "How's the new album coming along"}}]`
- **Final response**: Message sent! I've delivered "How's the new album coming along" to +12453344098.
- **Detail**: All expected tool calls matched in order | Tools called: send_message_with_phone_number | Response: Message sent! I've delivered "How's the new album coming along" to +12453344098.

### 5.20 cellular_off_all_tools

- **Category**: All Tools Available
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 20296 ms
- **Tool calls found**: `[{"name": "set_cellular_service_status", "args": {"on": false}}]`
- **Final response**: Cellular service has been turned off.
- **Detail**: All expected tool calls matched in order | Tools called: set_cellular_service_status | Response: Cellular service has been turned off.

### 5.21 search_contacts_all_tools

- **Category**: All Tools Available
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 17920 ms
- **Tool calls found**: `[{"name": "search_contacts", "args": {"name": "Homer S"}}]`
- **Final response**: Homer S's phone number is **+10000000000**.
- **Detail**: All expected tool calls matched in order | Tools called: search_contacts | Response: Homer S's phone number is **+10000000000**.

### 5.22 send_message_with_contact_cellular_off

- **Category**: Multi-Tool / State Dependency
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 27548 ms
- **Tool calls found**: `[{"name": "set_cellular_service_status", "args": {"on": false}}, {"name": "search_contacts", "args": {"name": "Homer S"}}, {"name": "send_message_with_phone_number", "args": {"phone_number": "+10000000000", "content": "Meeting at 3pm"}}]`
- **Final response**: Done! Here's a summary:

1. **Cellular service** has been turned off.
2. **Message sent** to Homer S (+10000000000): "Meeting at 3pm"

Note: The message was sent successfully, but since cellular service is currently off, it may have been queued or sent via an alternative method (e.g., Wi-Fi). Let me know if you'd like to turn cellular service back on!
- **Detail**: All expected tool calls matched in order | Tools called: set_cellular_service_status, search_contacts, send_message_with_phone_number | Response: Done! Here's a summary:

1. **Cellular service** has been turned off.
2. **Message sent** to Homer S (+10000000000): "Meeting at 3pm"

Note: The message was sent successfully, but since cellular servi

### 5.23 get_location_then_weather

- **Category**: Multi-Tool / State Dependency
- **Score**: 0.0/1.0
- **Tool call correct**: No
- **Tool args correct**: No
- **Response relevant**: No
- **Latency**: 5305 ms
- **Detail**: Missing expected tool call: get_current_location | No tool calls made
- **Error**: JSONDecodeError: Expecting value: line 1 column 1 (char 0)

### 5.24 general_question_no_tool

- **Category**: No Tool Required
- **Score**: 1.0/1.0
- **Tool call correct**: Yes
- **Tool args correct**: Yes
- **Response relevant**: Yes
- **Latency**: 4808 ms
- **Final response**: The capital of France is **Paris**.
- **Detail**: No tool call expected and none made | No tool calls made | Response: The capital of France is **Paris**.

## 6. Test Environment

| Item | Value |
|------|-------|
| OS | Windows |
| Python | 3.13.7 |
| API Protocol | OpenAI-compatible (v1/chat/completions) |
| Model | glm-5.1 |
| Base URL | https://ark.cn-beijing.volces.com/api/coding/v3 |
| Temperature | 0.0 |
| Max Tokens | 512 |
| Max Retries | 2 |
| Request Timeout | 60s |

---

*Report generated by GLM 5.1 ToolSandbox evaluation script.*