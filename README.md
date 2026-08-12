# Message Intelligence & Privacy System

An intelligent message-processing system that analyzes messages and performs three main tasks:

1. Message Classification
2. Task & Event Extraction
3. Sensitive Information Detection and Masking

The system processes unstructured messages and converts them into structured outputs while protecting sensitive information.

---

## Features

### 1. Message Classification

The system analyzes each message and assigns it to the appropriate message category based on its content.

The classification process helps identify the purpose or nature of a message and organize messages into structured categories.

---

### 2. Task and Event Extraction

The system extracts actionable information from messages and creates structured task/event records.

The extracted information includes:

- Message ID
- Type
- Title
- Deadline
- Time
- Person
- Priority
- Source Message ID

Example structure:

{
  "item_id": "TASK_014",
  "type": "task",
  "title": "Submit internship report",
  "deadline": "2026-08-15",
  "time": null,
  "person": null,
  "priority": "high",
  "source_message_id": "MSG_118"
}

If a person is not mentioned in the message, the person field is left blank/null.

---

### 3. Sensitive Information Detection and Masking

The system detects messages that may contain sensitive information.

The implemented sensitive-information categories include:

- Password
- One-Time Password (OTP)
- Bank/Payment Details
- Authentication Token
- Private Address
- Personal Identification Details
- Private Contact Details

Detected sensitive information is classified according to its risk level.

The system also generates a masked version of sensitive content so that sensitive values are not exposed in logs, screenshots, or demonstrations.

Example:

Original:
Your OTP is 483921

Masked:
Your OTP is ******

Sensitive information should not be included in generated logs, screenshots, or video demonstrations.

---

## How Message Classification Works

The input messages are loaded into a Pandas DataFrame.

The system processes the message text and identifies relevant patterns and keywords.

Based on the detected information, the message is assigned to the appropriate category.

The resulting information is stored in structured DataFrames and output files.

---

## How Tasks and Events Are Extracted

The system scans messages for task- and event-related information such as:

- Deadlines
- Dates
- Times
- Meeting/event information
- People involved
- Action-oriented instructions

The extracted information is stored in structured records.

For example:

"Please join the AI workshop on 2026-09-08, 15:00 at Conference Room 2."

can be converted into a structured event containing the date, time, event information, and source message ID.

If no person is explicitly identified, the person field remains blank/null.

---

## How Sensitive Information Is Detected

Sensitive information is detected using Python regular expressions (`re`) and pattern-based rules.

The system checks message text for patterns associated with sensitive information such as:

- Passwords
- OTPs
- Payment/card information
- Authentication tokens
- Private addresses
- Other selected personal details

When sensitive information is detected, the system records:

- Message ID
- Sensitivity type
- Risk level
- Masked text
- Recommended action

---

## Risk Levels

Sensitive information is assigned a risk level based on its category.

The system uses risk levels such as:

- High – highly sensitive information that should not be stored
- Medium – sensitive personal information requiring additional protection

Recommended actions may include:

- do_not_store
- ask_for_confirmation
- do_not_send_to_external_service

---

## Technologies Used

The project is implemented using Python.

Main libraries used:

- Python
- Pandas
- NumPy
- Regular Expressions (`re`)

---

## Project Structure

Message-Intelligence-System/
│
├── main_notebook.ipynb
├── requirements.txt
├── README.md
│
├── outputs/
│   ├── message_classification.csv
│   ├── task_events.csv
│   └── sensitivity_detection.csv
│
└── demo/
    └── screenshots/

Note: Output filenames may differ depending on the final generated files.

---

## Generated Structured Outputs

The project generates structured output files for the different processing stages.

These include outputs for:

- Message classification
- Task and event extraction
- Sensitive information detection

The original input dataset is intentionally not included in this public repository.

---

## Privacy and Security

The original dataset is not included in the public GitHub repository.

Sensitive values must not be exposed in:

- GitHub
- Logs
- Screenshots
- Video demonstrations
- Public documentation

Only masked or safe examples should be used for demonstrations.

---

## Assumptions and Limitations

### Assumptions

- Messages contain enough textual information for extraction.
- Dates and times follow recognizable formats.
- Sensitive information can be identified using predefined patterns.
- A person is extracted only when the message provides enough information to identify one.

### Limitations

- The system is primarily rule-based and pattern-based.
- It may not detect every possible variation of sensitive information.
- Ambiguous messages may not always provide enough information for accurate extraction.
- Natural-language variations that do not match the predefined patterns may be missed.
- The system does not guarantee complete protection against all forms of sensitive information.

---

## AI Tool Usage Declaration

AI tools were used during development for assistance with:

- Understanding and debugging code
- Improving implementation approaches
- Explaining programming concepts
- Reviewing and refining parts of the project

The final implementation was reviewed and executed by the project developer.

---

## Demonstration

### Loom Video



https://drive.google.com/file/d/1FyLvUsJbLf4fjgYq-PCm8BEmvV1mvQBr/view?usp=sharing

### Cloud Demo

https://message-intelligence-systems.streamlit.app/


---

## Important Privacy Notice

The original dataset must not be uploaded to this public GitHub repository.

Only source code, documentation, generated safe outputs, and non-sensitive demonstration material should be publicly available.
