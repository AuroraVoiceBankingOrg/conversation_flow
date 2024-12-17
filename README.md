# conversation_flow
Conversation flow: orchestrates input (voice/text) -> ASR -> Q&amp;A cache -> NLU/LLM -> TTS. Integrates with frontends and external integrations (banking, credit cards). Add steps to handle complex queries. Scalable and modular.


# conversation_flow

The `conversation_flow` repository is the core logic hub that orchestrates user interactions within the AI voice assistant ecosystem. It manages how user inputs (voice or text) are processed, passed through Automatic Speech Recognition (ASR), Natural Language Understanding (NLU), and Text-To-Speech (TTS) components, and how external services like banking APIs and credit card operations are integrated into a coherent conversational experience.

## Overview

- **Purpose:**  
  The `conversation_flow` code defines the step-by-step dialogue logic. When a user speaks or types a query, this logic decides what to do next. For example:
  - If voice input arrives, the conversation_flow sends it to `asr_core` to get a transcript.
  - Once text is obtained (either originally from user text input or from ASR output), it uses `ai_nlu` to interpret the user’s intent (e.g., checking bank balance, credit card statements).
  - If the user’s request involves banking data, it calls `external_integrations` to fetch account info, handle credit card scenarios, or run DB queries.
  - After determining a response, it might need to produce spoken output through `tts_core`.

- **Flexibility:**  
  The design is modular. Each file has a clear purpose, and directories are structured to allow easy addition of new scenarios (like adding a new language or a new type of banking transaction).

- **Integration:**  
  It works hand-in-hand with other repositories:
  - `core_repo` for overall orchestration and configuration.
  - `asr_core` for turning voice into text.
  - `ai_nlu` for understanding user intents and extracting relevant information.
  - `tts_core` for returning answers as spoken output.
  - `external_integrations` for linking to multiple databases (MySQL, PostgreSQL, MongoDB, Oracle, Redis, MSSQL, Cassandra, Elasticsearch, Firestore), banking endpoints, accounting systems, and credit card gateways.
  - `frontend_integrations` for examples on how frontends (mobile/web/desktop) connect to this system.

- **Scenarios & Testing:**  
  Within `conversation_flow`, you’ll find directories for scenarios (like `scenarios/banking_examples` or `scenarios/credit_card_examples`) that show how the system handles complex tasks. `tests/` ensures reliability across different conditions, and `test_env/` simulates user queries, multilingual dialogues, and offline modes.

## High-Level Visual Flow

Imagine the user says: *"What's my account balance?"*

**Step-by-Step (High-Level):**

```
(User) --> (frontend_integrations) --> (core_repo) --> (conversation_flow)
    |                                     |
    v                                     v
  If voice: (asr_core) ----> text ----> (ai_nlu) ---> Interpret intent (banking request)
                                              |
                                              v
                                    (external_integrations) --> fetch banking data
                                              |
                                              v
                                    Final text answer (e.g., "Your balance is $500.")
                                              |
                                    (tts_core) if voice output needed
                                              |
                                              v
                                           Return to user
```

1. **User Input:** Comes from `frontend_integrations` (like a mobile app).
2. **core_repo:** Directs input to `conversation_flow`.
3. **conversation_flow:** Uses `asr_core` if voice, then `ai_nlu` to understand the request.
4. **If Banking/Credit Card info needed:** Calls `external_integrations`.
5. **Once answer is ready:** May call `tts_core` to produce spoken output.
6. **Result:** Back to the user through the frontend.

## Internal Visual Flow of `conversation_flow`

Within `conversation_flow` itself, we have specialized Python files that handle specific parts of the conversation. For instance:

```
(flow_input_handler_voice.py) or (flow_input_handler_text.py)
               |
               v
          (flow_nlu_entity_map.py) --> Map entities (e.g. "account", "credit_card")
               |
          If banking-related:
               v
        (flow_banking_dialog.py) or (flow_credit_card_cmds.py)
               |
          If multi-step or multilingual scenario:
               v
     (flow_multistep_scenario.py) and (flow_language_switch_case.py)
               |
           Format response:
               v
       (flow_tts_response_sample.py) --> prepare text for TTS if needed
               |
        Handle errors if any:
               v
        (flow_error_recovery.py)
               |
   Possibly concurrency or offline checks:
               v
(flow_concurrency_checks.py) and (flow_offline_mode_tests.py)
               |
          Return final text or route to TTS
```

This internal flow ensures that each file plays a part. For example:
- `flow_input_handler_voice.py` deals with voice input specifics.
- `flow_banking_dialog.py` handles conversation steps for banking queries.
- `flow_multistep_scenario.py` ensures that if the user asks a follow-up question, the context is maintained.

## Running Order Inside `conversation_flow`

1. **Input Handling:**  
   If voice input arrives, `flow_input_handler_voice.py` is triggered, calling `asr_core`. If text input arrives directly, `flow_input_handler_text.py` is used.
   
2. **NLU and Entity Mapping:**  
   Once we have text, `flow_nlu_entity_map.py` ensures that NLU results (from `ai_nlu`) are translated into the right actions. For instance, if `ai_nlu` says user wants "Check credit card limit," this file ensures we call `flow_credit_card_cmds.py`.
   
3. **Dialog Management:**  
   `flow_banking_dialog.py` or `flow_credit_card_cmds.py` coordinate steps to complete a banking or credit card request. If multiple steps are needed (like verifying identity, then confirming transaction), `flow_multistep_scenario.py` manages stateful logic.
   
   If the user changes languages mid-conversation, `flow_language_switch_case.py` adjusts all further messages to that language, seamlessly integrating multilingual support.
   
4. **Response Formatting and TTS Preparation:**  
   Before responding, `flow_tts_response_sample.py` can ensure the text is well-formatted for speech output. If user wants speech output, we hand text to `tts_core`.
   
5. **Error and Special Conditions Handling:**  
   `flow_error_recovery.py` deals with errors (like missing data from the banking API). If multiple users or sessions must run concurrently, `flow_concurrency_checks.py` ensures stable performance. If external services fail, `flow_offline_mode_tests.py` helps handle that gracefully.
   
6. **Return Final Result:**  
   The final text or speech output goes back to `core_repo` and then to the frontend (via `frontend_integrations`), delivering the answer to the user.

## File Tree Detailed Explanation

Below is a representative file tree structure with brief comments for each file/directory. Each file’s name reflects its purpose, and directories are organized to separate various types of resources (docs, tests, configs, etc.).

```
conversation_flow/
├── README.md
│   # This document, describing architecture, visual flows, file roles, and integration points.
│
├── flow_input_handler_voice.py
│   # Handles voice input scenarios: receives audio (from ASR) and decides next steps.
├── flow_input_handler_text.py
│   # Handles text input scenarios: direct textual queries from user or other modules.
├── flow_qna_cache_example.py
│   # Shows how Q&A caching works to quickly return answers to repeated questions.
├── flow_banking_dialog.py
│   # Logic specific to banking-related dialogues (check balance, transfer funds).
├── flow_credit_card_cmds.py
│   # Handles credit card-specific commands (payment due, limit checks, lost card).
├── flow_multistep_scenario.py
│   # Manages multi-step conversations, maintaining context over multiple user turns.
├── flow_language_switch_case.py
│   # Handles dynamic switching of conversation language mid-session.
├── flow_tts_response_sample.py
│   # Prepares and formats responses before sending to TTS for spoken output.
├── flow_asr_integration_test.py
│   # Ensures ASR output integrates smoothly into conversation steps.
├── flow_nlu_entity_map.py
│   # Maps NLU entities/intents to correct conversation actions.
├── flow_frontend_sync.py
│   # Syncs conversation states with frontends (mobile/web/desktop).
├── flow_error_recovery.py
│   # Provides strategies to recover from errors (API fail, unknown intent).
├── flow_concurrency_checks.py
│   # Verifies stable performance under multiple simultaneous conversations.
├── flow_offline_mode_tests.py
│   # Tests how conversation behaves if external services (like banking API) are offline.
├── flow_special_locale_handling.py
│   # Handles special locale or region-specific rules in conversations.
│
├── docs/
│   ├── architecture/
│   │   ├── conversation_flow_overview.mmd
│   │   │   # Mermaid diagram depicting conversation flow architecture.
│   │   ├── architecture_notes.txt
│   │   │   # Notes on architectural decisions and trade-offs.
│   │   └── diagram_instructions.md
│   │      # How to modify and generate architecture diagrams.
│   ├── sequence_diagrams/
│   │   ├── asr_to_nlu_flow.mmd
│   │   │   # Sequence diagram from ASR output to NLU input steps.
│   │   ├── tts_integration_seq.mmd
│   │   │   # Diagram of TTS integration steps in conversation.
│   │   └── frontend_interaction_seq.txt
│   │      # Notes on how frontends interact with conversation steps.
│   ├── user_guides/
│   │   ├── getting_started.md
│   │   │   # Steps to get started with modifying conversation_flow code.
│   │   ├── frontend_setup.md
│   │   │   # Guide on hooking conversation logic into frontend UIs.
│   │   └── model_adaptation_guide.md
│   │      # Adapting conversation logic when ASR/TTS/LLM models change.
│   ├── user_stories/
│   │   ├── banking_user_stories.md
│   │   │   # Scenarios where user interacts with banking features.
│   │   ├── credit_card_user_stories.md
│   │   │   # Stories involving credit card operations.
│   │   └── language_switch_user_stories.md
│   │      # Stories about switching languages mid-conversation.
│   └── security/
│       ├── security_threat_model.md
│       │   # Identifies potential security threats in conversation handling.
│       ├── data_privacy.yaml
│       │   # Privacy policies for handling sensitive user data.
│       └── vulnerability_report_template.txt
│          # Template for reporting found vulnerabilities.
│
├── tests/
│   ├── unit/
│   │   ├── test_basic_flow.py
│   │   │   # Tests basic conversation steps handling.
│   │   └── test_input_parsing.py
│   │       # Ensures input parsing logic works correctly.
│   ├── integration/
│   │   ├── test_asr_conversation_integration.py
│   │   │   # Checks if ASR output is correctly utilized in the flow.
│   │   └── test_nlu_entities_integration.py
│   │       # Ensures NLU entities trigger correct actions.
│   ├── performance/
│   │   ├── test_latency.py
│   │   │   # Measures latency of conversation steps.
│   │   └── test_resource_usage.py
│   │       # Checks CPU/RAM usage under load.
│   ├── security/
│   │   ├── test_input_sanitization.py
│   │   │   # Prevents malicious input exploitation.
│   │   └── test_auth_mechanisms.py
│   │       # Tests any authentication layers if present.
│   └── end_to_end/
│       ├── test_full_user_journey.py
│       │   # Simulates a full scenario: user speaks, system responds end-to-end.
│       └── test_complex_multistep_flow.py
│           # Tests a complex scenario requiring multiple turns.
│
├── configs/
│   ├── conversation_config.yaml
│   │   # Core configuration file for conversation rules, fallback behaviors.
│   ├── default_settings.json
│   │   # Default JSON settings for fallback or initial states.
│   ├── env/
│   │   ├── dev_env.yaml
│   │   │   # Dev environment overrides.
│   │   ├── prod_env.yaml
│   │   │   # Production environment settings.
│   │   └── env_notes.txt
│   │       # Notes on differences between environments.
│   └── templates/
│       ├── template_conversation.yaml
│       │   # YAML template for creating new conversation scenarios quickly.
│       └── template_vars.json
│           # Variables for template substitution.
│
├── scripts/
│   ├── run_flow_checks.sh
│   │   # Script to run a set of checks on conversation logic.
│   ├── lint_conversation_flow.py
│   │   # Lints Python code for coding style and errors.
│   └── convert_transcripts.py
│       # Utility to convert transcripts from one format to another.
│   └── tools/
│       ├── scenario_replayer.py
│       │   # Replays recorded scenarios for regression testing.
│       ├── db_cleanup.sh
│       │   # Cleans up test-related DB entries.
│       └── profiling_tool.py
│           # Profiles performance during conversation steps.
│
├── integration/
│   ├── frontend/
│   │   ├── frontend_sync_guide.md
│   │   │   # Guide on syncing conversation states with frontend clients.
│   │   └── mock_frontend_data.json
│   │       # Sample mock data representing frontend states.
│   ├── banking/
│   │   ├── banking_apis.yaml
│   │   │   # YAML listing banking API endpoints for integration.
│   │   └── test_banking_flow_integration.py
│   │       # Tests conversation steps with actual banking endpoints.
│   └── credit_card/
│       ├── credit_card_api_map.yaml
│       │   # Maps credit card gateways and endpoints.
│       └── cc_scenario_tests.py
│           # Tests credit card scenarios in conversation.
│
├── scenarios/
│   ├── banking_examples/
│   │   ├── check_balance_scenario.json
│   │   │   # Scenario: user asks for account balance.
│   │   └── transfer_funds_scenario.yaml
│   │       # Scenario: user initiates a funds transfer.
│   ├── credit_card_examples/
│   │   ├── lost_card_report.json
│   │   │   # Scenario: reporting a lost credit card.
│   │   └── payment_due_query.yaml
│   │       # User asks about credit card payment due date.
│   └── multilingual_cases/
│       ├── lang_switch_en_to_ru.json
│       │   # Scenario switching from English to Russian mid-flow.
│       └── lang_switch_uz_to_en.yaml
│           # Uzbek to English switching scenario.
│
├── qna_cache/
│   ├── examples/
│   │   ├── qna_cache_simple_case.json
│   │   │   # Example of a simple Q&A cache entry.
│   │   └── qna_cache_policies.yaml
│   │       # Policies describing Q&A caching strategies.
│
├── logging/
│   ├── handlers/
│   │   ├── custom_flow_logger.py
│   │   │   # Custom logger for conversation steps to standardize log output.
│   │   └── log_format_config.yaml
│   │       # Config for log formatting rules.
│
├── metrics/
│   ├── collection/
│   │   ├── metrics_collector.py
│   │   │   # Collects metrics (latency, error rates) from conversation steps.
│   │   └── metrics_dashboard_template.json
│   │       # Template for a metrics dashboard visualizing performance.
│
├── utils/
│   ├── conversation_steps/
│   │   ├── step_parser.py
│   │   │   # Parses conversation steps from config to runtime instructions.
│   │   └── step_validator.py
│   │       # Validates integrity and logic of conversation steps.
│   └── error_handling/
│       ├── error_mapper.py
│       │   # Maps certain errors to known recovery strategies.
│       └── error_logging.sh
│           # Shell script to backup error logs for analysis.
│
├── samples/
│   ├── multilanguage_dialogs/
│   │   ├── uz_ru_dialog_sample.json
│   │   │   # Sample dialogue mixing Uzbek and Russian queries.
│   │   └── en_banking_dialog.txt
│   │       # English dialogue related to banking tasks.
│   └── offline_test_data/
│       ├── offline_asr_input.wav
│       │   # Sample WAV for offline testing of ASR integration.
│       └── offline_transcript_ref.json
│           # Reference transcripts for offline tests.
│

```

## Detailed Explanation

- **`flow_input_handler_voice.py` & `flow_input_handler_text.py`:**  
  These are starting points for any user input. If the input is voice, `flow_input_handler_voice.py` initiates the chain by calling `asr_core` to get a transcript. If it's text, `flow_input_handler_text.py` proceeds directly with that text.

- **`flow_nlu_entity_map.py`:**  
  Once text is available, this file ensures that the `ai_nlu` results (intents, entities) correspond to the correct conversation actions. For example, if NLU detects "Check Balance," this file directs the logic towards `flow_banking_dialog.py`.

- **Scenario-specific files like `flow_banking_dialog.py`, `flow_credit_card_cmds.py`:**  
  These manage the steps required for certain domains. `flow_banking_dialog.py` orchestrates queries about account balances or transactions, while `flow_credit_card_cmds.py` handles credit card inquiries. They interact with `external_integrations` to fetch data from banking APIs or credit card gateways.

- **`flow_multistep_scenario.py`:**  
  If a user request spans multiple steps (e.g., user first asks "What's my balance?" then "Transfer $100 to savings"), this file helps maintain context across turns, ensuring a natural conversation flow.

- **`flow_language_switch_case.py`:**  
  Users may switch languages mid-conversation. This file updates all subsequent steps to the new language. Combined with `language_support` configs and `ai_nlu` that can handle multiple languages, this ensures a seamless multilingual experience.

- **`flow_tts_response_sample.py`:**  
  Once a textual answer is ready, this file can format it for spoken output, connecting to `tts_core` if the user wants the final response as audio.

- **`flow_error_recovery.py`, `flow_concurrency_checks.py`, `flow_offline_mode_tests.py`, `flow_special_locale_handling.py`:**  
  These handle special conditions. `flow_error_recovery.py` tries to gracefully handle unexpected errors, `flow_concurrency_checks.py` ensures stable performance if multiple users are interacting simultaneously, `flow_offline_mode_tests.py` checks how the system behaves if external services fail, and `flow_special_locale_handling.py` deals with locale-specific conversation nuances (like date formats, currency units).

## Integrations and Configurations

- **`integration` directories** (`frontend`, `banking`, `credit_card`) show how this repository’s logic ties into external services or frontends. For example, `integration/frontend/frontend_sync_guide.md` explains how to keep the conversation state in sync with the mobile/web UI. `integration/banking` and `integration/credit_card` show how conversation steps call external APIs defined in `external_integrations`.

- **`configs/` directories** hold YAML and JSON configs for conversation rules (`conversation_config.yaml`), environment-specific overrides (`dev_env.yaml`, `prod_env.yaml`), and template files (`template_conversation.yaml`) to quickly set up new scenarios.

- **`tests/` directories** categorize tests. `unit` tests check basic logic, `integration` tests ensure that conversation steps integrate well with ASR/NLU, `performance` tests measure latency, `security` tests prevent vulnerabilities, and `end_to_end` tests simulate a full user journey.

- **`docs/`**:  
  Provide extensive documentation. `docs/architecture` has `.mmd` mermaid diagrams, `docs/sequence_diagrams` show step-by-step call sequences, `docs/user_guides` help newcomers get started, `docs/user_stories` show real-world use cases, and `docs/security` detail security considerations.

- **`scenarios/`**:  
  Predefined conversation scenarios (e.g., `check_balance_scenario.json`) help you test or demo certain functionalities quickly. `banking_examples`, `credit_card_examples`, and `multilingual_cases` help developers understand complex cases.

- **`qna_cache/`**:  
  Illustrates how Q&A caching can speed up repeated questions. `qna_cache_simple_case.json` shows a straightforward example, and `qna_cache_policies.yaml` define caching rules.

- **`logging/` and `metrics/`**:  
  Logging handlers and metrics collectors help monitor the system’s health. `custom_flow_logger.py` sets logging formats, and `metrics_collector.py` gathers performance data, enabling you to find bottlenecks or issues.

- **`utils/`**:  
  General utilities. For instance, `utils/conversation_steps/step_parser.py` parses conversation steps defined in configs, while `utils/error_handling/error_mapper.py` maps certain errors to strategies (like asking user to repeat or fallback to a default answer).

- **`samples/`**:  
  Holds sample dialogues (`uz_ru_dialog_sample.json`, `en_banking_dialog.txt`) and offline test data (`offline_asr_input.wav`) to test behavior under specific conditions.

## Conclusion

This repository’s structure, file naming, and directory organization aim to make it straightforward for a new developer or stakeholder to:
- Find where conversation logic is defined and modified.
- Understand how the flow integrates with ASR (`asr_core`), NLU (`ai_nlu`), TTS (`tts_core`), and external APIs (`external_integrations`).
- Locate tests, scenarios, and docs to quickly grasp how to run, test, or modify conversation behavior.



