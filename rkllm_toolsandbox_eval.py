"""
rkllm ToolSandbox Evaluation Script
====================================
Standalone evaluation of rkllm-model (http://172.31.18.39:8080) against
ToolSandbox-style scenarios. Tests tool calling accuracy across multiple
categories: single tool, multi-tool, multi-turn, state-dependent, and
distraction tool scenarios.

No dependency on the ToolSandbox framework itself — uses only openai + requests.
"""

import copy
import json
import math
import sys
import time
import traceback
from dataclasses import dataclass, field
from typing import Any, Optional

import requests
from openai import OpenAI

# ── Configuration ──────────────────────────────────────────────────────────
RKLLM_BASE_URL = "http://172.31.18.39:8080/v1"
RKLLM_API_KEY = "EMPTY"
RKLLM_MODEL = "rkllm-model"
REQUEST_TIMEOUT = 60
MAX_RETRIES = 2
MAX_TURNS = 5

CLIENT = OpenAI(base_url=RKLLM_BASE_URL, api_key=RKLLM_API_KEY)


# ── Test result data structures ────────────────────────────────────────────
@dataclass
class TestCaseResult:
    name: str
    category: str
    passed: bool
    score: float
    latency_ms: float
    tool_call_correct: bool
    tool_args_correct: bool
    response_relevant: bool
    detail: str = ""
    error: str = ""
    full_response: str = ""
    final_response: str = ""
    tool_calls_found: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class EvalReport:
    model: str
    base_url: str
    timestamp: str = ""
    results: list[TestCaseResult] = field(default_factory=list)
    api_connectivity: bool = False
    model_info: str = ""

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def passed_count(self) -> int:
        return sum(1 for r in self.results if r.passed)

    @property
    def avg_score(self) -> float:
        return sum(r.score for r in self.results) / max(self.total, 1)

    @property
    def avg_latency_ms(self) -> float:
        return sum(r.latency_ms for r in self.results) / max(self.total, 1)

    @property
    def tool_call_accuracy(self) -> float:
        return sum(1 for r in self.results if r.tool_call_correct) / max(self.total, 1)

    @property
    def tool_args_accuracy(self) -> float:
        return sum(1 for r in self.results if r.tool_args_correct) / max(self.total, 1)


# ── Tool definitions (mirroring ToolSandbox tools) ─────────────────────────
TOOL_SETTING_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "set_cellular_service_status",
            "description": "Enable or Disable cellular service",
            "parameters": {
                "type": "object",
                "properties": {
                    "on": {"type": "boolean", "description": "If we want to turn on cellular service"}
                },
                "required": ["on"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_cellular_service_status",
            "description": "Request cellular service status",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_wifi_status",
            "description": "Enable or Disable wifi",
            "parameters": {
                "type": "object",
                "properties": {
                    "on": {"type": "boolean", "description": "If we want to turn on wifi"}
                },
                "required": ["on"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_wifi_status",
            "description": "Request wifi status",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_location_service_status",
            "description": "Enable or Disable location service",
            "parameters": {
                "type": "object",
                "properties": {
                    "on": {"type": "boolean", "description": "If we want to turn on location service"}
                },
                "required": ["on"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_location_service_status",
            "description": "Request location service status",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_low_battery_mode_status",
            "description": "Enable or Disable low battery mode. When low battery mode is on, cellular, wifi, and location service are automatically turned off and cannot be turned on.",
            "parameters": {
                "type": "object",
                "properties": {
                    "on": {"type": "boolean", "description": "If we want to turn on low battery mode"}
                },
                "required": ["on"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_location",
            "description": "Request current location latitude and longitude. Requires location service to be enabled.",
            "parameters": {"type": "object", "properties": {}},
        },
    },
]

TOOL_CONTACT_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_contacts",
            "description": "Search for a contact person based on name, phone number, or relationship",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Name of contact person"},
                    "phone_number": {"type": "string", "description": "Phone number of contact person"},
                    "relationship": {"type": "string", "description": "Relationship between user and this contact"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_contact",
            "description": "Add a new contact person to contact database",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Name of contact person"},
                    "phone_number": {"type": "string", "description": "Phone number of contact person"},
                    "relationship": {"type": "string", "description": "Optional, relationship between user and this contact"},
                },
                "required": ["name", "phone_number"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "remove_contact",
            "description": "Remove an existing contact person from contact database",
            "parameters": {
                "type": "object",
                "properties": {
                    "person_id": {"type": "string", "description": "String format unique identifier of the person to be deleted"}
                },
                "required": ["person_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "modify_contact",
            "description": "Modify a contact entry with new information provided",
            "parameters": {
                "type": "object",
                "properties": {
                    "person_id": {"type": "string", "description": "String unique identifier for the contact person"},
                    "name": {"type": "string", "description": "New name for the person"},
                    "phone_number": {"type": "string", "description": "New phone number for the person"},
                    "relationship": {"type": "string", "description": "New relationship for the person"},
                },
                "required": ["person_id"],
            },
        },
    },
]

TOOL_MESSAGING_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "send_message_with_phone_number",
            "description": "Send a message to a phone number",
            "parameters": {
                "type": "object",
                "properties": {
                    "phone_number": {"type": "string", "description": "The phone number to send the message to"},
                    "content": {"type": "string", "description": "The content of the message"},
                },
                "required": ["phone_number", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_messages",
            "description": "Search for messages based on content or sender/recipient",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "Search for messages containing this content"},
                    "sender_phone_number": {"type": "string", "description": "Search for messages from this phone number"},
                    "recipient_phone_number": {"type": "string", "description": "Search for messages to this phone number"},
                },
            },
        },
    },
]

TOOL_SEARCH_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_weather_around_lat_lon",
            "description": "Search for weather information around a given latitude and longitude",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number", "description": "Latitude of the location"},
                    "longitude": {"type": "number", "description": "Longitude of the location"},
                    "days": {"type": "integer", "description": "Number of days for forecast, 0 for today"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_location_around_lat_lon",
            "description": "Search for locations around a given latitude and longitude or by name",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string", "description": "Name of the location to search for"},
                    "latitude": {"type": "number", "description": "Latitude"},
                    "longitude": {"type": "number", "description": "Longitude"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_stock",
            "description": "Search for stock symbol by company name",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string", "description": "Company name or stock query"}},
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "convert_currency",
            "description": "Convert an amount from one currency to another",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {"type": "number", "description": "The amount to convert"},
                    "from_currency_code": {"type": "string", "description": "Source currency code, e.g. USD"},
                    "to_currency_code": {"type": "string", "description": "Target currency code, e.g. CNY"},
                },
                "required": ["amount", "from_currency_code", "to_currency_code"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_holiday",
            "description": "Search for holiday information by name",
            "parameters": {
                "type": "object",
                "properties": {
                    "holiday_name": {"type": "string", "description": "Name of the holiday"},
                    "year": {"type": "integer", "description": "Year to search for"},
                },
                "required": ["holiday_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_lat_lon",
            "description": "Search for the address of a given latitude and longitude",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number", "description": "Latitude"},
                    "longitude": {"type": "number", "description": "Longitude"},
                },
                "required": ["latitude", "longitude"],
            },
        },
    },
]

DISTRACTION_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "set_reminder",
            "description": "Set a reminder with content and time",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {"type": "string", "description": "Content of the reminder"},
                    "timestamp": {"type": "number", "description": "Unix timestamp for the reminder"},
                },
                "required": ["content", "timestamp"],
            },
        },
    },
    {"type": "function", "function": {"name": "get_reminders", "description": "Get all reminders", "parameters": {"type": "object", "properties": {}}}},
    {
        "type": "function",
        "function": {
            "name": "delete_reminder",
            "description": "Delete a reminder by ID",
            "parameters": {
                "type": "object",
                "properties": {"reminder_id": {"type": "string", "description": "ID of the reminder to delete"}},
                "required": ["reminder_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "Send an email to a recipient",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "Email address of recipient"},
                    "subject": {"type": "string", "description": "Subject of the email"},
                    "body": {"type": "string", "description": "Body of the email"},
                },
                "required": ["to", "subject", "body"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calendar_add_event",
            "description": "Add an event to the calendar",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Title of the event"},
                    "start_time": {"type": "number", "description": "Start time as Unix timestamp"},
                    "end_time": {"type": "number", "description": "End time as Unix timestamp"},
                },
                "required": ["title", "start_time", "end_time"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "play_music",
            "description": "Play music by artist or song name",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string", "description": "Song or artist name"}},
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "set_alarm",
            "description": "Set an alarm for a specific time",
            "parameters": {
                "type": "object",
                "properties": {
                    "time": {"type": "string", "description": "Time for the alarm in HH:MM format"},
                    "label": {"type": "string", "description": "Label for the alarm"},
                },
                "required": ["time"],
            },
        },
    },
    {"type": "function", "function": {"name": "take_photo", "description": "Take a photo with the camera", "parameters": {"type": "object", "properties": {}}}},
    {
        "type": "function",
        "function": {
            "name": "open_app",
            "description": "Open an application on the device",
            "parameters": {
                "type": "object",
                "properties": {"app_name": {"type": "string", "description": "Name of the app to open"}},
                "required": ["app_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "make_phone_call",
            "description": "Make a phone call to a number",
            "parameters": {
                "type": "object",
                "properties": {"phone_number": {"type": "string", "description": "Phone number to call"}},
                "required": ["phone_number"],
            },
        },
    },
]

ALL_TOOLS = TOOL_SETTING_TOOLS + TOOL_CONTACT_TOOLS + TOOL_MESSAGING_TOOLS + TOOL_SEARCH_TOOLS + DISTRACTION_TOOLS


# ── Simulated execution environment ────────────────────────────────────────
INITIAL_SIMULATED_STATE = {
    "cellular": True,
    "wifi": True,
    "location_service": True,
    "low_battery_mode": False,
    "latitude": 37.334606,
    "longitude": -122.009102,
}

INITIAL_SIMULATED_CONTACTS = [
    {"person_id": "contact-001", "name": "Homer S", "phone_number": "+10000000000", "relationship": "boss"},
    {"person_id": "contact-002", "name": "Marge S", "phone_number": "+10000000001", "relationship": "friend"},
    {"person_id": "contact-003", "name": "Bart S", "phone_number": "+10000000002", "relationship": "colleague"},
    {"person_id": "contact-self", "name": "User A", "phone_number": "+10000000003", "relationship": None, "is_self": True},
]

INITIAL_SIMULATED_MESSAGES = [
    {"sender_phone_number": "+18307976530", "recipient_phone_number": "+10000000003", "content": "Do you want some GPUs?"},
    {"sender_phone_number": "+10000000003", "recipient_phone_number": "+12453344098", "content": "Hey there!"},
]

SIMULATED_STATE = copy.deepcopy(INITIAL_SIMULATED_STATE)
SIMULATED_CONTACTS = copy.deepcopy(INITIAL_SIMULATED_CONTACTS)
SIMULATED_MESSAGES = copy.deepcopy(INITIAL_SIMULATED_MESSAGES)


def reset_simulated_environment() -> None:
    global SIMULATED_STATE, SIMULATED_CONTACTS, SIMULATED_MESSAGES
    SIMULATED_STATE = copy.deepcopy(INITIAL_SIMULATED_STATE)
    SIMULATED_CONTACTS = copy.deepcopy(INITIAL_SIMULATED_CONTACTS)
    SIMULATED_MESSAGES = copy.deepcopy(INITIAL_SIMULATED_MESSAGES)


def simulate_tool_call(function_name: str, arguments: dict) -> str:
    args = arguments if isinstance(arguments, dict) else json.loads(arguments)

    if function_name == "get_cellular_service_status":
        return json.dumps({"cellular": SIMULATED_STATE["cellular"]})
    if function_name == "set_cellular_service_status":
        if SIMULATED_STATE["low_battery_mode"] and args.get("on"):
            return json.dumps({"error": "Cannot enable cellular while low battery mode is on."})
        SIMULATED_STATE["cellular"] = args.get("on", True)
        return json.dumps({"result": "success", "cellular": SIMULATED_STATE["cellular"]})
    if function_name == "get_wifi_status":
        return json.dumps({"wifi": SIMULATED_STATE["wifi"]})
    if function_name == "set_wifi_status":
        if SIMULATED_STATE["low_battery_mode"] and args.get("on"):
            return json.dumps({"error": "Cannot enable wifi while low battery mode is on."})
        SIMULATED_STATE["wifi"] = args.get("on", True)
        return json.dumps({"result": "success", "wifi": SIMULATED_STATE["wifi"]})
    if function_name == "get_location_service_status":
        return json.dumps({"location_service": SIMULATED_STATE["location_service"]})
    if function_name == "set_location_service_status":
        if SIMULATED_STATE["low_battery_mode"] and args.get("on"):
            return json.dumps({"error": "Cannot enable location service while low battery mode is on."})
        SIMULATED_STATE["location_service"] = args.get("on", True)
        return json.dumps({"result": "success", "location_service": SIMULATED_STATE["location_service"]})
    if function_name == "set_low_battery_mode_status":
        SIMULATED_STATE["low_battery_mode"] = args.get("on", True)
        if SIMULATED_STATE["low_battery_mode"]:
            SIMULATED_STATE["cellular"] = False
            SIMULATED_STATE["wifi"] = False
            SIMULATED_STATE["location_service"] = False
        return json.dumps({"result": "success", "low_battery_mode": SIMULATED_STATE["low_battery_mode"]})
    if function_name == "get_current_location":
        if not SIMULATED_STATE["location_service"]:
            return json.dumps({"error": "Location service is not enabled."})
        return json.dumps({"latitude": SIMULATED_STATE["latitude"], "longitude": SIMULATED_STATE["longitude"]})
    if function_name == "search_contacts":
        results = SIMULATED_CONTACTS[:]
        if args.get("name"):
            results = [c for c in results if args["name"].lower() in c["name"].lower()]
        if args.get("phone_number"):
            results = [c for c in results if c["phone_number"] == args["phone_number"]]
        if args.get("relationship"):
            results = [c for c in results if args["relationship"].lower() in (c.get("relationship") or "").lower()]
        return json.dumps(results)
    if function_name == "add_contact":
        new_id = f"contact-{len(SIMULATED_CONTACTS) + 1:03d}"
        SIMULATED_CONTACTS.append(
            {
                "person_id": new_id,
                "name": args.get("name", ""),
                "phone_number": args.get("phone_number", ""),
                "relationship": args.get("relationship"),
            }
        )
        return json.dumps({"person_id": new_id})
    if function_name == "remove_contact":
        SIMULATED_CONTACTS[:] = [c for c in SIMULATED_CONTACTS if c["person_id"] != args.get("person_id", "")]
        return json.dumps({"result": "success"})
    if function_name == "modify_contact":
        person_id = args.get("person_id", "")
        for contact in SIMULATED_CONTACTS:
            if contact["person_id"] == person_id:
                for key, value in args.items():
                    if key != "person_id" and value is not None:
                        contact[key] = value
        return json.dumps({"result": "success"})
    if function_name == "send_message_with_phone_number":
        SIMULATED_MESSAGES.append(
            {
                "sender_phone_number": "+10000000003",
                "recipient_phone_number": args.get("phone_number", ""),
                "content": args.get("content", ""),
            }
        )
        return json.dumps({"result": "success", "message_sent": True})
    if function_name == "search_messages":
        results = SIMULATED_MESSAGES[:]
        if args.get("content"):
            results = [m for m in results if args["content"].lower() in m["content"].lower()]
        if args.get("sender_phone_number"):
            results = [m for m in results if m["sender_phone_number"] == args["sender_phone_number"]]
        if args.get("recipient_phone_number"):
            results = [m for m in results if m["recipient_phone_number"] == args["recipient_phone_number"]]
        return json.dumps(results)
    if function_name == "search_weather_around_lat_lon":
        return json.dumps({"temperature": 22.5, "condition": "sunny", "unit": "celsius"})
    if function_name == "search_location_around_lat_lon":
        return json.dumps({"name": "Apple Park", "address": "1 Apple Park Way, Cupertino, CA 95014", "phone_number": "+14089961010"})
    if function_name == "search_stock":
        return json.dumps({"symbol": "AAPL", "company": "Apple Inc."})
    if function_name == "convert_currency":
        return json.dumps({"result": 14800.0, "from": args.get("from_currency_code"), "to": args.get("to_currency_code")})
    if function_name == "search_holiday":
        return json.dumps({"holiday": args.get("holiday_name"), "date": "2024-11-28", "timestamp": 1732752000})
    if function_name == "search_lat_lon":
        return json.dumps({"address": "Apple Park 1 Apple Park Way Cupertino, CA 95014 United States"})

    return json.dumps({"result": "ok", "info": f"Simulated execution of {function_name}"})


# ── Helpers ────────────────────────────────────────────────────────────────
def normalize_text(value: Any) -> str:
    return str(value).strip().lower()


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def values_match(expected: Any, found: Any) -> bool:
    if isinstance(expected, bool):
        return found is expected
    if is_number(expected) and is_number(found):
        return math.isclose(float(expected), float(found), rel_tol=1e-9, abs_tol=1e-9)
    return normalize_text(expected) == normalize_text(found)


def args_match(expected_args: dict[str, Any], found_args: dict[str, Any]) -> bool:
    for key, expected_value in expected_args.items():
        if key not in found_args or not values_match(expected_value, found_args[key]):
            return False
    return True


def evaluate_tool_calls(found_calls: list[dict[str, Any]], expected_calls: list[dict[str, Any]]) -> tuple[bool, bool, str]:
    if not expected_calls:
        if found_calls:
            return False, False, f"Unexpected tool calls: {', '.join(call['name'] for call in found_calls)}"
        return True, True, "No tool call expected and none made"

    matched_calls: list[dict[str, Any]] = []
    search_start = 0

    for expected in expected_calls:
        matched = None
        for idx in range(search_start, len(found_calls)):
            if found_calls[idx]["name"] == expected["name"]:
                matched = {"index": idx, "call": found_calls[idx]}
                search_start = idx + 1
                break
        if matched is None:
            return False, False, f"Missing expected tool call: {expected['name']}"
        matched_calls.append(matched)

    tool_call_correct = True
    tool_args_correct = True

    for expected, matched in zip(expected_calls, matched_calls):
        if "args_match" in expected and not args_match(expected["args_match"], matched["call"]["args"]):
            tool_args_correct = False
            return tool_call_correct, tool_args_correct, (
                f"Tool args mismatch for {expected['name']}: expected subset {expected['args_match']}, "
                f"got {matched['call']['args']}"
            )

    return tool_call_correct, tool_args_correct, "All expected tool calls matched in order"


# ── API call helper ────────────────────────────────────────────────────────
def call_rkllm(messages: list, tools: Optional[list] = None, temperature: float = 0.0) -> dict:
    kwargs = {
        "model": RKLLM_MODEL,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": 512,
        "timeout": REQUEST_TIMEOUT,
    }
    if tools:
        kwargs["tools"] = tools

    for attempt in range(MAX_RETRIES + 1):
        try:
            response = CLIENT.chat.completions.create(**kwargs)
            return response.choices[0].message.model_dump()
        except Exception:
            if attempt == MAX_RETRIES:
                raise
            time.sleep(2 ** attempt)


def run_conversation_turns(system_prompt: str, user_message: str, tools: list, expected_tool_calls: list[dict], max_turns: int = MAX_TURNS) -> TestCaseResult:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]
    tool_calls_found: list[dict[str, Any]] = []
    all_responses: list[dict[str, Any]] = []
    start_time = time.time()
    error = ""
    final_response = ""

    try:
        for _ in range(max_turns):
            msg = call_rkllm(messages, tools=tools)
            all_responses.append(msg)

            if msg.get("tool_calls"):
                messages.append(msg)
                for tc in msg["tool_calls"]:
                    func_name = tc["function"]["name"]
                    func_args = tc["function"]["arguments"]
                    if isinstance(func_args, str):
                        func_args = json.loads(func_args)
                    tool_calls_found.append({"name": func_name, "args": func_args})
                    result = simulate_tool_call(func_name, func_args)
                    messages.append({"role": "tool", "tool_call_id": tc["id"], "content": result})
            else:
                final_response = (msg.get("content") or "").strip()
                break
    except Exception as e:
        error = f"{type(e).__name__}: {e}"
        if not tool_calls_found and not all_responses:
            latency_ms = (time.time() - start_time) * 1000
            return TestCaseResult(
                name="",
                category="",
                passed=False,
                score=0.0,
                latency_ms=latency_ms,
                tool_call_correct=False,
                tool_args_correct=False,
                response_relevant=False,
                error=error,
                full_response="[]",
                final_response="",
                tool_calls_found=[],
            )

    latency_ms = (time.time() - start_time) * 1000
    tool_call_correct, tool_args_correct, eval_detail = evaluate_tool_calls(tool_calls_found, expected_tool_calls)
    response_relevant = bool(final_response and len(final_response) > 5)

    score = 0.0
    if tool_call_correct:
        score += 0.5
    if tool_args_correct:
        score += 0.3
    if response_relevant:
        score += 0.2

    detail_parts = [eval_detail]
    if tool_calls_found:
        detail_parts.append(f"Tools called: {', '.join(call['name'] for call in tool_calls_found)}")
    else:
        detail_parts.append("No tool calls made")
    if final_response:
        detail_parts.append(f"Response: {final_response[:200]}")

    return TestCaseResult(
        name="",
        category="",
        passed=score >= 0.5,
        score=score,
        latency_ms=latency_ms,
        tool_call_correct=tool_call_correct,
        tool_args_correct=tool_args_correct,
        response_relevant=response_relevant,
        detail=" | ".join(detail_parts),
        error=error,
        full_response=json.dumps(all_responses, ensure_ascii=False)[:4000],
        final_response=final_response,
        tool_calls_found=tool_calls_found,
    )


# ── Test scenarios ─────────────────────────────────────────────────────────
SYSTEM_PROMPT = (
    "You are a helpful phone assistant. You can control device settings, "
    "manage contacts, send messages, and search for information. "
    "Always use the provided tools to fulfill user requests. "
    "When you have the information, respond concisely to the user."
)


def define_test_cases() -> list[dict]:
    cases = []

    cases.append({"name": "cellular_off", "category": "Single Tool Call - Settings", "user_message": "Turn off cellular", "tools": [TOOL_SETTING_TOOLS[0]], "expected": [{"name": "set_cellular_service_status", "args_match": {"on": False}}]})
    cases.append({"name": "get_cellular", "category": "Single Tool Call - Settings", "user_message": "Is my cellular service on?", "tools": [TOOL_SETTING_TOOLS[1]], "expected": [{"name": "get_cellular_service_status"}]})
    cases.append({"name": "wifi_off", "category": "Single Tool Call - Settings", "user_message": "Turn off wifi", "tools": [TOOL_SETTING_TOOLS[2]], "expected": [{"name": "set_wifi_status", "args_match": {"on": False}}]})
    cases.append({"name": "get_wifi", "category": "Single Tool Call - Settings", "user_message": "Is my wifi on?", "tools": [TOOL_SETTING_TOOLS[3]], "expected": [{"name": "get_wifi_status"}]})

    cases.append({"name": "search_phone_number_with_name", "category": "Single Tool Call - Contacts", "user_message": "What is Homer S's phone number?", "tools": [TOOL_CONTACT_TOOLS[0]], "expected": [{"name": "search_contacts", "args_match": {"name": "Homer S"}}]})
    cases.append({"name": "search_name_with_relationship", "category": "Single Tool Call - Contacts", "user_message": "What is the name of my boss?", "tools": [TOOL_CONTACT_TOOLS[0]], "expected": [{"name": "search_contacts", "args_match": {"relationship": "boss"}}]})
    cases.append({"name": "search_relationship_with_phone_number", "category": "Single Tool Call - Contacts", "user_message": "What's my relationship with +10000000000", "tools": [TOOL_CONTACT_TOOLS[0]], "expected": [{"name": "search_contacts", "args_match": {"phone_number": "+10000000000"}}]})
    cases.append({"name": "add_contact_with_name_and_phone_number", "category": "Single Tool Call - Contacts", "user_message": "Add Stephen Sondheim to my contact, his phone_number is +19876543210", "tools": [TOOL_CONTACT_TOOLS[1]], "expected": [{"name": "add_contact", "args_match": {"name": "Stephen Sondheim", "phone_number": "+19876543210"}}]})

    cases.append({"name": "send_message_with_phone_number_and_content", "category": "Single Tool Call - Messaging", "user_message": "Send a message to +12453344098 saying: How's the new album coming along", "tools": [TOOL_MESSAGING_TOOLS[0]], "expected": [{"name": "send_message_with_phone_number", "args_match": {"phone_number": "+12453344098"}}]})
    cases.append({"name": "search_sender_phone_number_with_content", "category": "Single Tool Call - Messaging", "user_message": "Which phone number asked me if I want some GPUs?", "tools": [TOOL_MESSAGING_TOOLS[1]], "expected": [{"name": "search_messages"}]})

    cases.append({"name": "find_temperature", "category": "Single Tool Call - Search", "user_message": "What's the temperature here right now", "tools": [TOOL_SEARCH_TOOLS[0]], "expected": [{"name": "search_weather_around_lat_lon"}]})
    cases.append({"name": "find_stock_symbol", "category": "Single Tool Call - Search", "user_message": "What's the stock symbol for Apple", "tools": [TOOL_SEARCH_TOOLS[2]], "expected": [{"name": "search_stock", "args_match": {"query": "Apple"}}]})
    cases.append({"name": "convert_currency", "category": "Single Tool Call - Search", "user_message": "How much is 2048 USD in CNY", "tools": [TOOL_SEARCH_TOOLS[3]], "expected": [{"name": "convert_currency", "args_match": {"amount": 2048, "from_currency_code": "USD", "to_currency_code": "CNY"}}]})

    cases.append({"name": "convert_currency_canonicalize", "category": "Canonicalization", "user_message": "How much is $2.048k in CNY", "tools": [TOOL_SEARCH_TOOLS[3]], "expected": [{"name": "convert_currency", "args_match": {"amount": 2048, "from_currency_code": "USD"}}]})
    cases.append({"name": "find_phone_number_with_location_name", "category": "Canonicalization", "user_message": "What's the phone number of Apple Park", "tools": [TOOL_SEARCH_TOOLS[1]], "expected": [{"name": "search_location_around_lat_lon"}]})

    cases.append({"name": "cellular_off_3_distraction", "category": "3 Distraction Tools", "user_message": "Turn off cellular", "tools": [TOOL_SETTING_TOOLS[0]] + DISTRACTION_TOOLS[:3], "expected": [{"name": "set_cellular_service_status", "args_match": {"on": False}}]})
    cases.append({"name": "search_contacts_3_distraction", "category": "3 Distraction Tools", "user_message": "What is Homer S's phone number?", "tools": [TOOL_CONTACT_TOOLS[0]] + DISTRACTION_TOOLS[:3], "expected": [{"name": "search_contacts", "args_match": {"name": "Homer S"}}]})

    cases.append({"name": "wifi_off_10_distraction", "category": "10 Distraction Tools", "user_message": "Turn off wifi", "tools": [TOOL_SETTING_TOOLS[2]] + DISTRACTION_TOOLS[:10], "expected": [{"name": "set_wifi_status", "args_match": {"on": False}}]})
    cases.append({"name": "send_message_10_distraction", "category": "10 Distraction Tools", "user_message": "Send a message to +12453344098 saying: How's the new album coming along", "tools": [TOOL_MESSAGING_TOOLS[0]] + DISTRACTION_TOOLS[:10], "expected": [{"name": "send_message_with_phone_number"}]})

    cases.append({"name": "cellular_off_all_tools", "category": "All Tools Available", "user_message": "Turn off cellular", "tools": ALL_TOOLS, "expected": [{"name": "set_cellular_service_status", "args_match": {"on": False}}]})
    cases.append({"name": "search_contacts_all_tools", "category": "All Tools Available", "user_message": "What is Homer S's phone number?", "tools": ALL_TOOLS, "expected": [{"name": "search_contacts"}]})

    cases.append(
        {
            "name": "send_message_with_contact_cellular_off",
            "category": "Multi-Tool / State Dependency",
            "user_message": "Send a message to Homer S saying: Meeting at 3pm. But first, turn off cellular service.",
            "tools": TOOL_SETTING_TOOLS[:2] + TOOL_CONTACT_TOOLS[:2] + TOOL_MESSAGING_TOOLS[:1],
            "expected": [
                {"name": "set_cellular_service_status", "args_match": {"on": False}},
                {"name": "search_contacts"},
                {"name": "send_message_with_phone_number"},
            ],
        }
    )
    cases.append(
        {
            "name": "get_location_then_weather",
            "category": "Multi-Tool / State Dependency",
            "user_message": "What's the weather at my current location?",
            "tools": [TOOL_SETTING_TOOLS[4], TOOL_SETTING_TOOLS[7], TOOL_SEARCH_TOOLS[0]],
            "expected": [{"name": "get_current_location"}, {"name": "search_weather_around_lat_lon"}],
        }
    )

    cases.append({"name": "general_question_no_tool", "category": "No Tool Required", "user_message": "What is the capital of France?", "tools": TOOL_SETTING_TOOLS[:4], "expected": []})
    return cases


# ── Main evaluation ────────────────────────────────────────────────────────
def check_api_connectivity(report: EvalReport) -> bool:
    try:
        # Try chat completions endpoint first (most reliable for RKLLM)
        test_response = CLIENT.chat.completions.create(
            model=RKLLM_MODEL,
            messages=[{"role": "user", "content": "test"}],
            max_tokens=1,
            timeout=30,
        )
        report.api_connectivity = True
        report.model_info = f"Chat API responding normally. Model: {RKLLM_MODEL}"
        return True
    except Exception as e:
        pass

    # Fallback: try /v1/models endpoint
    try:
        model_url = RKLLM_BASE_URL[:-3] + "models" if RKLLM_BASE_URL.endswith("/v1") else RKLLM_BASE_URL.rstrip("/") + "/models"
        response = requests.get(model_url, timeout=10)
        if response.status_code == 200:
            report.model_info = json.dumps(response.json(), indent=2)
            report.api_connectivity = True
            return True
        report.model_info = f"Unexpected status code: {response.status_code}"
    except Exception as e:
        report.model_info = f"Connection failed: {e}"
    report.api_connectivity = False
    return False


def run_evaluation() -> EvalReport:
    report = EvalReport(model=RKLLM_MODEL, base_url=RKLLM_BASE_URL, timestamp=time.strftime("%Y-%m-%d %H:%M:%S"))

    print("=" * 70)
    print("  rkllm ToolSandbox Evaluation")
    print("=" * 70)
    print()

    print("[1/4] Checking API connectivity...")
    if not check_api_connectivity(report):
        print("  FAIL: Cannot connect to rkllm API at", RKLLM_BASE_URL)
        return report
    print("  PASS: API is reachable")
    print(f"  Model info: {report.model_info[:100]}")
    print()

    print("[2/4] Testing basic chat completion...")
    try:
        start = time.time()
        msg = call_rkllm([{"role": "user", "content": "Hello, please respond with 'OK'."}])
        latency = (time.time() - start) * 1000
        print(f"  PASS: Got response in {latency:.0f}ms")
        print(f"  Response: {(msg.get('content') or '')[:100]}")
    except Exception as e:
        print(f"  FAIL: {e}")
        return report
    print()

    print("[3/4] Running ToolSandbox test scenarios...")
    test_cases = define_test_cases()
    print(f"  Total test cases: {len(test_cases)}")
    print()

    for i, tc in enumerate(test_cases, 1):
        reset_simulated_environment()
        print(f"  [{i}/{len(test_cases)}] {tc['name']} ({tc['category']})...", end=" ", flush=True)
        try:
            result = run_conversation_turns(
                system_prompt=SYSTEM_PROMPT,
                user_message=tc["user_message"],
                tools=tc["tools"],
                expected_tool_calls=tc["expected"],
            )
            result.name = tc["name"]
            result.category = tc["category"]
            print(f"{'PASS' if result.passed else 'FAIL'} (score={result.score:.1f}, latency={result.latency_ms:.0f}ms)")
        except Exception as e:
            result = TestCaseResult(
                name=tc["name"],
                category=tc["category"],
                passed=False,
                score=0.0,
                latency_ms=0.0,
                tool_call_correct=False,
                tool_args_correct=False,
                response_relevant=False,
                error=f"Exception: {traceback.format_exc()[:500]}",
            )
            print(f"ERROR: {e}")
        report.results.append(result)
        time.sleep(1)

    print()
    print("[4/4] Summary")
    print(f"  Total tests:      {report.total}")
    print(f"  Passed:           {report.passed_count}")
    print(f"  Pass rate:        {report.passed_count / max(report.total, 1) * 100:.1f}%")
    print(f"  Average score:    {report.avg_score:.3f}")
    print(f"  Avg latency:      {report.avg_latency_ms:.0f}ms")
    print(f"  Tool call acc:    {report.tool_call_accuracy * 100:.1f}%")
    print(f"  Tool args acc:    {report.tool_args_accuracy * 100:.1f}%")
    print()

    return report


def generate_markdown_report(report: EvalReport) -> str:
    lines = []
    lines.append("# rkllm ToolSandbox Evaluation Report")
    lines.append("")
    lines.append("## 1. Overview")
    lines.append("")
    lines.append("| Item | Value |")
    lines.append("|------|-------|")
    lines.append(f"| Model | `{report.model}` |")
    lines.append(f"| API Endpoint | `{report.base_url}` |")
    lines.append(f"| Test Time | {report.timestamp} |")
    lines.append(f"| API Connectivity | {'PASS' if report.api_connectivity else 'FAIL'} |")
    lines.append(f"| Total Test Cases | {report.total} |")
    lines.append(f"| Passed | {report.passed_count} |")
    lines.append(f"| Pass Rate | {report.passed_count / max(report.total, 1) * 100:.1f}% |")
    lines.append(f"| Average Score | {report.avg_score:.3f} |")
    lines.append(f"| Average Latency | {report.avg_latency_ms:.0f} ms |")
    lines.append(f"| Tool Call Accuracy | {report.tool_call_accuracy * 100:.1f}% |")
    lines.append(f"| Tool Args Accuracy | {report.tool_args_accuracy * 100:.1f}% |")
    lines.append("")

    lines.append("## 2. Scoring Methodology")
    lines.append("")
    lines.append("Each test case is scored on a 0-1 scale:")
    lines.append("")
    lines.append("| Component | Weight | Description |")
    lines.append("|-----------|--------|-------------|")
    lines.append("| Correct tool call | 0.5 | All expected tool calls are made in order |")
    lines.append("| Correct arguments | 0.3 | Expected argument subsets match the corresponding tool calls |")
    lines.append("| Relevant response | 0.2 | The final assistant response contains a non-empty relevant answer |")
    lines.append("")
    lines.append("A test is considered **PASS** if the score >= 0.5.")
    lines.append("")

    categories: dict[str, list[TestCaseResult]] = {}
    for result in report.results:
        categories.setdefault(result.category, []).append(result)

    lines.append("## 3. Results by Category")
    lines.append("")
    lines.append("| Category | Tests | Passed | Pass Rate | Avg Score | Avg Latency | Tool Call Acc | Tool Args Acc |")
    lines.append("|----------|-------|--------|-----------|-----------|-------------|---------------|---------------|")
    for cat in sorted(categories):
        results = categories[cat]
        n = len(results)
        passed = sum(1 for r in results if r.passed)
        avg_score = sum(r.score for r in results) / n
        avg_lat = sum(r.latency_ms for r in results) / n
        tc_acc = sum(1 for r in results if r.tool_call_correct) / n
        ta_acc = sum(1 for r in results if r.tool_args_correct) / n
        lines.append(f"| {cat} | {n} | {passed} | {passed / n * 100:.0f}% | {avg_score:.2f} | {avg_lat:.0f}ms | {tc_acc * 100:.0f}% | {ta_acc * 100:.0f}% |")
    lines.append("")

    lines.append("## 4. Detailed Test Results")
    lines.append("")
    lines.append("| # | Test Name | Category | Score | Tool Call | Args | Response | Latency | Status |")
    lines.append("|---|-----------|----------|-------|-----------|------|----------|---------|--------|")
    for i, r in enumerate(report.results, 1):
        lines.append(f"| {i} | {r.name} | {r.category} | {r.score:.1f} | {'Y' if r.tool_call_correct else 'N'} | {'Y' if r.tool_args_correct else 'N'} | {'Y' if r.response_relevant else 'N'} | {r.latency_ms:.0f}ms | {'PASS' if r.passed else 'FAIL'} |")
    lines.append("")

    lines.append("## 5. Detailed Per-Test Analysis")
    lines.append("")
    for i, r in enumerate(report.results, 1):
        lines.append(f"### 5.{i} {r.name}")
        lines.append("")
        lines.append(f"- **Category**: {r.category}")
        lines.append(f"- **Score**: {r.score:.1f}/1.0")
        lines.append(f"- **Tool call correct**: {'Yes' if r.tool_call_correct else 'No'}")
        lines.append(f"- **Tool args correct**: {'Yes' if r.tool_args_correct else 'No'}")
        lines.append(f"- **Response relevant**: {'Yes' if r.response_relevant else 'No'}")
        lines.append(f"- **Latency**: {r.latency_ms:.0f} ms")
        if r.tool_calls_found:
            lines.append(f"- **Tool calls found**: `{json.dumps(r.tool_calls_found, ensure_ascii=False)}`")
        if r.final_response:
            lines.append(f"- **Final response**: {r.final_response}")
        if r.detail:
            lines.append(f"- **Detail**: {r.detail}")
        if r.error:
            lines.append(f"- **Error**: {r.error}")
        lines.append("")

    lines.append("## 6. Test Environment")
    lines.append("")
    lines.append("| Item | Value |")
    lines.append("|------|-------|")
    lines.append("| OS | Windows |")
    lines.append(f"| Python | {sys.version.split()[0]} |")
    lines.append("| API Protocol | OpenAI-compatible (v1/chat/completions) |")
    lines.append("| Temperature | 0.0 |")
    lines.append("| Max Tokens | 512 |")
    lines.append(f"| Max Retries | {MAX_RETRIES} |")
    lines.append(f"| Request Timeout | {REQUEST_TIMEOUT}s |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Report generated by rkllm ToolSandbox evaluation script.*")
    return "\n".join(lines)


if __name__ == "__main__":
    report = run_evaluation()
    markdown = generate_markdown_report(report)
    report_path = "rkllm_toolsandbox_report.md"
    with open(report_path, "w", encoding="utf-8") as file:
        file.write(markdown)

    print(f"Report saved to: {report_path}")
    print()
    print("=" * 70)
    print("  Evaluation Complete")
    print("=" * 70)
