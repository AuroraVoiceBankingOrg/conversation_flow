# conversation_flow

This repository manages the logic that orchestrates user conversations through multiple steps:
- Handling voice/text input
- Integrating ASR/NLU/TTS
- Interacting with banking and credit card services
- Managing multistep scenarios, language switching, caching responses, and dealing with errors.

## Visual Flow and Integration with Other Repos
High-Level Steps:
1. User inputs (voice/text) come from frontends (see `frontend_integrations` in main project).
2. `core_repo` directs input to `conversation_flow`.
3. `conversation_flow` uses `asr_core` (if voice) to get transcripts, `ai_nlu` to interpret intents, `external_integrations` for banking/credit card queries.
4. Once the final textual answer is decided, it calls `tts_core` if voice output is needed.
5. Results return to the frontend, ensuring a seamless user experience.

**Visual Flow Diagram (High-Level):**
```
(User) -> (frontend_integrations) -> (core_repo) -> (conversation_flow) -> (asr_core / ai_nlu / external_integrations) -> (tts_core) -> back to (User)
```

In `conversation_flow`, these Python files (e.g., `flow_input_handler_voice.py`) represent distinct functionalities:
- `flow_input_handler_voice.py`: Logic for handling voice input scenarios.
- `flow_banking_dialog.py`: Manages banking-related dialogue steps.
- `flow_qna_cache_example.py`: Demonstrates how Q&A caching works to respond faster.
- ... and so forth.

## Running Order Internally
1. Input arrives (voice): `flow_input_handler_voice.py` triggered, passes data to ASR.
2. Once transcribed, `flow_nlu_entity_map.py` might run to map NLU entities to actions.
3. If banking request: `flow_banking_dialog.py` interacts with `external_integrations` to fetch data.
4. If user asks about credit cards: `flow_credit_card_cmds.py` handles these commands.
5. For special scenarios (multi-step queries): `flow_multistep_scenario.py` ensures stateful dialogue.
6. Results may be language-switched via `flow_language_switch_case.py` if user changes language mid-conversation.
7. `flow_tts_response_sample.py` might format the text nicely before TTS.
8. `flow_error_recovery.py` deals with any errors gracefully.
9. Output returns to user via the frontend.

## Directory and File Explanation
Directories like `tests/` contain various categories of tests (unit, integration, performance, etc.) for ensuring the reliability of conversation logic.
`docs/` hold architectural diagrams (`.mmd` mermaid files), user guides, user stories, and security notes, providing clarity on how conversation steps are designed.
`configs/` store conversation configurations, templates for scenario setups, and environment-specific overrides.
`integration/` dirs show how conversation_flow connects to frontends, banking APIs, and credit card services.
`scenarios/` store scenario definitions (banking examples, credit card usage cases, multilingual switching), enabling easy replication of complex dialogues.
`qna_cache/` demonstrates response caching mechanism.
`logging/` and `metrics/` directories hold utilities for logging conversation steps and collecting performance metrics.
`utils/` contain helper scripts for parsing steps, error handling, and audio/text conversions if needed.
`samples/` keep sample dialogues and test data for experimentation.

With this structure, developers can easily locate where to adjust conversation rules, add new scenarios, optimize performance, handle errors, integrate new APIs, or test new language models. Each file name is self-explanatory, and directories are logically separated, ensuring a flexible and maintainable codebase.
