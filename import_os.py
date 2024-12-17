import os
import shutil

repo_name = "conversation_flow"

# Name patterns (main Python files) given by the user
name_patterns = [
    "flow_input_handler_voice",    # Handles voice input dispatching
    "flow_input_handler_text",     # Handles text input dispatching
    "flow_qna_cache_example",      # Demonstrates Q&A caching mechanism
    "flow_banking_dialog",         # Orchestrates banking-related dialogues
    "flow_credit_card_cmds",       # Manages credit card-related commands in conversation
    "flow_multistep_scenario",     # Example of handling a multi-step user scenario
    "flow_language_switch_case",   # Logic for switching conversation language on-the-fly
    "flow_tts_response_sample",    # Example of formatting text for TTS responses
    "flow_asr_integration_test",   # Integration test with ASR results
    "flow_nlu_entity_map",         # Mapping NLU entities to conversation actions
    "flow_frontend_sync",          # Sync states with frontend UIs (mobile/desktop/web)
    "flow_error_recovery",         # Logic for recovering from errors in conversation
    "flow_concurrency_checks",     # Checks handling multiple requests concurrently
    "flow_offline_mode_tests",     # Scenario handling if external services are offline
    "flow_special_locale_handling" # Handling special locale-specific conversation rules
]

# Additional directories to provide a comprehensive structure
subdirs = [
    "docs",
    "docs/architecture",
    "docs/sequence_diagrams",
    "docs/user_guides",
    "docs/user_stories",
    "docs/security",
    "tests",
    "tests/unit",
    "tests/integration",
    "tests/performance",
    "tests/security",
    "tests/end_to_end",
    "configs",
    "configs/env",
    "configs/templates",
    "scripts",
    "scripts/tools",
    "integration",
    "integration/frontend",
    "integration/banking",
    "integration/credit_card",
    "scenarios",
    "scenarios/banking_examples",
    "scenarios/credit_card_examples",
    "scenarios/multilingual_cases",
    "qna_cache",
    "qna_cache/examples",
    "logging",
    "logging/handlers",
    "metrics",
    "metrics/collection",
    "utils",
    "utils/conversation_steps",
    "utils/error_handling",
    "samples",
    "samples/multilanguage_dialogs",
    "samples/offline_test_data"
]

# Files to add in certain directories to clarify their purpose
dir_files = {
    "docs/architecture": [
        "conversation_flow_overview.mmd", # Mermaid diagram of conversation flow steps
        "architecture_notes.txt",         # Notes about architectural decisions
        "diagram_instructions.md"         # How to edit/generate architecture diagrams
    ],
    "docs/sequence_diagrams": [
        "asr_to_nlu_flow.mmd",            # Sequence diagram from ASR output to NLU input
        "tts_integration_seq.mmd",        # Diagram of TTS response integration
        "frontend_interaction_seq.txt"    # Text notes on frontend interaction sequences
    ],
    "docs/user_guides": [
        "getting_started.md",             # Guide on how to start using conversation_flow
        "frontend_setup.md",              # Instructions to integrate with frontend UIs
        "model_adaptation_guide.md"       # Adapting conversation to new models/languages
    ],
    "docs/user_stories": [
        "banking_user_stories.md",        # User stories related to banking tasks
        "credit_card_user_stories.md",    # User stories for credit card operations
        "language_switch_user_stories.md" # Stories involving multilingual switching
    ],
    "docs/security": [
        "security_threat_model.md",       # Threat model for conversation handling
        "data_privacy.yaml",              # YAML config for privacy-related policies
        "vulnerability_report_template.txt" # Template for reporting found vulnerabilities
    ],
    "tests/unit": [
        "test_basic_flow.py",             # Unit tests for basic conversation steps
        "test_input_parsing.py"           # Test input parsing logic
    ],
    "tests/integration": [
        "test_asr_conversation_integration.py", # Integrates ASR results into the flow
        "test_nlu_entities_integration.py"      # Ensures NLU entities trigger correct actions
    ],
    "tests/performance": [
        "test_latency.py",                # Measures latency of conversation steps
        "test_resource_usage.py"          # Checks CPU/RAM usage under load
    ],
    "tests/security": [
        "test_input_sanitization.py",     # Ensures malicious inputs are sanitized
        "test_auth_mechanisms.py"         # Tests any auth layers if present
    ],
    "tests/end_to_end": [
        "test_full_user_journey.py",      # Simulates a full user journey: ASR->NLU->TTS
        "test_complex_multistep_flow.py"  # Tests a complex, multi-step scenario
    ],
    "configs": [
        "conversation_config.yaml",       # Core config for conversation rules
        "default_settings.json"           # Default JSON settings
    ],
    "configs/env": [
        "dev_env.yaml",                   # Dev environment settings
        "prod_env.yaml",                  # Production environment config
        "env_notes.txt"                   # Notes on env differences
    ],
    "configs/templates": [
        "template_conversation.yaml",     # Template for new conversation scenarios
        "template_vars.json"             # Variables for template substitution
    ],
    "scripts": [
        "run_flow_checks.sh",             # Script to run conversation checks
        "lint_conversation_flow.py",      # Linting rules for conversation flow code
        "convert_transcripts.py"          # Utility: convert transcript formats
    ],
    "scripts/tools": [
        "scenario_replayer.py",           # Replays recorded scenarios for testing
        "db_cleanup.sh",                  # Cleans up test DB entries after tests
        "profiling_tool.py"               # Profiles performance during conversation steps
    ],
    "integration/frontend": [
        "frontend_sync_guide.md",         # Guide on syncing flow states with frontends
        "mock_frontend_data.json"         # Mock data representing frontend states
    ],
    "integration/banking": [
        "banking_apis.yaml",              # YAML listing banking API endpoints
        "test_banking_flow_integration.py"# Tests banking endpoints integration with flow
    ],
    "integration/credit_card": [
        "credit_card_api_map.yaml",       # Maps credit card gateway APIs
        "cc_scenario_tests.py"            # Tests credit card scenarios in conversation
    ],
    "scenarios/banking_examples": [
        "check_balance_scenario.json",    # Scenario: user asks for account balance
        "transfer_funds_scenario.yaml"    # YAML scenario: user transfers funds
    ],
    "scenarios/credit_card_examples": [
        "lost_card_report.json",          # Scenario: reporting a lost credit card
        "payment_due_query.yaml"          # User asks about credit card payment due date
    ],
    "scenarios/multilingual_cases": [
        "lang_switch_en_to_ru.json",      # Scenario switching from English to Russian mid-flow
        "lang_switch_uz_to_en.yaml"       # Uzbek to English switching scenario
    ],
    "qna_cache/examples": [
        "qna_cache_simple_case.json",      # Example Q&A cache entry
        "qna_cache_policies.yaml"         # Policies for caching Q&A pairs
    ],
    "logging/handlers": [
        "custom_flow_logger.py",          # Custom logger for conversation steps
        "log_format_config.yaml"          # Config for log formatting
    ],
    "metrics/collection": [
        "metrics_collector.py",           # Collect metrics about conversation flow
        "metrics_dashboard_template.json" # Template for a metrics dashboard
    ],
    "utils/conversation_steps": [
        "step_parser.py",                 # Parses conversation steps
        "step_validator.py"               # Validates integrity of conversation steps
    ],
    "utils/error_handling": [
        "error_mapper.py",                # Maps errors to recovery strategies
        "error_logging.sh"                # Shell script for error logs backup
    ],
    "samples/multilanguage_dialogs": [
        "uz_ru_dialog_sample.json",       # Sample dialogue mixing Uzbek and Russian
        "en_banking_dialog.txt"           # English dialogue related to banking
    ],
    "samples/offline_test_data": [
        "offline_asr_input.wav",          # Sample WAV for offline testing ASR integration
        "offline_transcript_ref.json"     # Reference transcripts for offline tests
    ]
}

def write_file(path, lines):
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")

def generic_content(name):
    return [f"# {name}", "# Placeholder content. Update as needed."]

def generate_content_for_file(filename):
    ext = os.path.splitext(filename)[1]
    if ext == ".py":
        return [f"# {filename}", "# Python code for conversation flow logic or testing."]
    elif ext in [".yaml", ".yml"]:
        return [f"# {filename}", "# YAML configuration or scenario definition."]
    elif ext == ".json":
        return ["{", f'  "description": "Placeholder for {filename}"', "}"]
    elif ext == ".txt":
        return [f"# {filename}", "# Text notes or documentation."]
    elif ext == ".sh":
        return [f"#!/usr/bin/env bash", f"# {filename}", "# Shell script placeholder.", "echo 'Running script...'"]
    elif ext == ".ipynb":
        return ['{"cells":[],"metadata":{},"nbformat":4,"nbformat_minor":5}']
    elif ext == ".md":
        return [f"# {filename}", "# Markdown documentation or guides."]
    elif ext == ".mmd":
        return [f"%% Mermaid diagram for {filename}", "graph LR;", "A-->B;"]
    else:
        return generic_content(filename)

def main():
    # Remove existing directory if present
    if os.path.exists(repo_name):
        shutil.rmtree(repo_name)

    os.makedirs(repo_name)
    print(f"Created directory: {repo_name}")

    # Create directories
    for d in subdirs:
        dir_path = os.path.join(repo_name, d)
        os.makedirs(dir_path, exist_ok=True)
        gitkeep_path = os.path.join(dir_path, ".gitkeep")
        write_file(gitkeep_path, [f"# .gitkeep to keep {d} directory in version control."])
        print(f"Created directory: {dir_path} and .gitkeep")

    # Create main Python files from name_patterns
    for pattern in name_patterns:
        filename = pattern + ".py"
        file_path = os.path.join(repo_name, filename)
        lines = generate_content_for_file(filename)
        write_file(file_path, lines)
        print(f"Created file: {file_path}")

    # Create files in directories
    for directory, files in dir_files.items():
        for f in files:
            file_path = os.path.join(repo_name, directory, f)
            lines = generate_content_for_file(f)
            write_file(file_path, lines)
            print(f"Created file: {file_path}")

    # Create a top-level README with detailed explanation
    readme_path = os.path.join(repo_name, "README.md")
    readme_lines = [
        "# conversation_flow",
        "",
        "This repository manages the logic that orchestrates user conversations through multiple steps:",
        "- Handling voice/text input",
        "- Integrating ASR/NLU/TTS",
        "- Interacting with banking and credit card services",
        "- Managing multistep scenarios, language switching, caching responses, and dealing with errors.",
        "",
        "## Visual Flow and Integration with Other Repos",
        "High-Level Steps:",
        "1. User inputs (voice/text) come from frontends (see `frontend_integrations` in main project).",
        "2. `core_repo` directs input to `conversation_flow`.",
        "3. `conversation_flow` uses `asr_core` (if voice) to get transcripts, `ai_nlu` to interpret intents, `external_integrations` for banking/credit card queries.",
        "4. Once the final textual answer is decided, it calls `tts_core` if voice output is needed.",
        "5. Results return to the frontend, ensuring a seamless user experience.",
        "",
        "**Visual Flow Diagram (High-Level):**",
        "```\n(User) -> (frontend_integrations) -> (core_repo) -> (conversation_flow) -> (asr_core / ai_nlu / external_integrations) -> (tts_core) -> back to (User)\n```",
        "",
        "In `conversation_flow`, these Python files (e.g., `flow_input_handler_voice.py`) represent distinct functionalities:",
        "- `flow_input_handler_voice.py`: Logic for handling voice input scenarios.",
        "- `flow_banking_dialog.py`: Manages banking-related dialogue steps.",
        "- `flow_qna_cache_example.py`: Demonstrates how Q&A caching works to respond faster.",
        "- ... and so forth.",
        "",
        "## Running Order Internally",
        "1. Input arrives (voice): `flow_input_handler_voice.py` triggered, passes data to ASR.",
        "2. Once transcribed, `flow_nlu_entity_map.py` might run to map NLU entities to actions.",
        "3. If banking request: `flow_banking_dialog.py` interacts with `external_integrations` to fetch data.",
        "4. If user asks about credit cards: `flow_credit_card_cmds.py` handles these commands.",
        "5. For special scenarios (multi-step queries): `flow_multistep_scenario.py` ensures stateful dialogue.",
        "6. Results may be language-switched via `flow_language_switch_case.py` if user changes language mid-conversation.",
        "7. `flow_tts_response_sample.py` might format the text nicely before TTS.",
        "8. `flow_error_recovery.py` deals with any errors gracefully.",
        "9. Output returns to user via the frontend.",
        "",
        "## Directory and File Explanation",
        "Directories like `tests/` contain various categories of tests (unit, integration, performance, etc.) for ensuring the reliability of conversation logic.",
        "`docs/` hold architectural diagrams (`.mmd` mermaid files), user guides, user stories, and security notes, providing clarity on how conversation steps are designed.",
        "`configs/` store conversation configurations, templates for scenario setups, and environment-specific overrides.",
        "`integration/` dirs show how conversation_flow connects to frontends, banking APIs, and credit card services.",
        "`scenarios/` store scenario definitions (banking examples, credit card usage cases, multilingual switching), enabling easy replication of complex dialogues.",
        "`qna_cache/` demonstrates response caching mechanism.",
        "`logging/` and `metrics/` directories hold utilities for logging conversation steps and collecting performance metrics.",
        "`utils/` contain helper scripts for parsing steps, error handling, and audio/text conversions if needed.",
        "`samples/` keep sample dialogues and test data for experimentation.",
        "",
        "With this structure, developers can easily locate where to adjust conversation rules, add new scenarios, optimize performance, handle errors, integrate new APIs, or test new language models. Each file name is self-explanatory, and directories are logically separated, ensuring a flexible and maintainable codebase."
    ]
    write_file(readme_path, readme_lines)
    print(f"Created file: {readme_path}")

    print("File tree creation for conversation_flow completed with a comprehensive set of directories and files!")

if __name__ == "__main__":
    main()
