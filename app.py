import streamlit as st
import pandas as pd
import numpy as np
import re


# ============================================================
# AI MESSAGE PROCESSING SYSTEM
# ============================================================

st.set_page_config(
    page_title="AI Message Processing System",
    page_icon="💬",
    layout="wide"
)

st.title("AI Message Processing System")
st.write(
    "This system performs message classification, "
    "task/event extraction, and sensitive information detection."
)


# ============================================================
# PART 1: MESSAGE CLASSIFICATION
# ============================================================

categories = [
    "Action Required",
    "Meeting or Event",
    "Personal Information",
    "General Information",
    "Promotional",
    "Sensitive Information"
]


sensitive_patterns = {
    "password": r"\bpassword\b|\bpasscode\b",
    "one_time_password": r"\botp\b|\bone[- ]time password\b|verification code",
    "pin": r"\bpin\b|\bsecurity pin\b",
    "payment_details": r"\bcard number\b|\baccount number\b|\bcredit card\b|\bdebit card\b|\bcvv\b|\bupi\b",
    "identification": r"\baadhaar\b|\bpassport\b|\bidentity number\b|\bid number\b",
    "contact_or_address": r"\bhome address\b|\bphone number\b|\bmobile number\b|\bpersonal email\b"
}


meeting_patterns = {
    r"\bmeeting\b",
    r"\bappointment\b",
    r"\bconference\b",
    r"\bevent\b",
    r"\borientation\b",
    r"\bjoin\b.*\b(on|at)\b",
    r"\bcatch[- ]up\b",
    r"\bscheduled\b",
    r"\breminder\b.*\b(on|at)\b"
}


action_patterns = {
    r"\bplease\b.*\b(reply|submit|review|complete|send|update|renew|pay|finish|check|join)\b",
    r"\bneed you to\b",
    r"\baction required\b",
    r"\bdeadline\b",
    r"\bby \d{4}-\d{2}-\d{2}\b",
    r"\bdon't forget\b",
    r"\bremember to\b"
}


# Promotional patterns
promotional_patterns = {
    r"\bdiscount\b",
    r"\bsale\b",
    r"\boffer\b",
    r"\bpromo\b",
    r"\bpromotional\b",
    r"\bcoupon\b",
    r"\bcode\s+[A-Z0-9]+\b",
    r"\bpremium plan\b",
    r"\bexclusive benefits\b"
}


personal_patterns = {
    r"\bmy home\b",
    r"\bmy brother\b",
    r"\bmy sister\b",
    r"\bmy family\b",
    r"\bmy profile\b",
    r"\bmy recent\b",
    r"\bi drink\b",
    r"\bmy birthday\b",
    r"\bemergency contact\b",
    r"\bpersonal\b"
}


def find_matches(text, patterns):
    matches = []

    for pattern in patterns:
        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if match:
            matches.append(match.group(0))

    return matches


def classify_message(text):

    text = str(text)

    # Sensitive information gets higher priority
    for sensitivity_type, pattern in sensitive_patterns.items():

        if re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        ):

            return (
                "Sensitive Information",
                0.99,
                f"Sensitive Information Detected: {sensitivity_type}"
            )


    # Promotional
    matches = find_matches(
        text,
        promotional_patterns
    )

    if matches:

        return (
            "Promotional",
            min(
                0.95,
                0.75 + 0.05 * len(matches)
            ),
            "Promotional Language Detected: "
            + ", ".join(matches[:3])
        )


    # Meeting / Event
    matches = find_matches(
        text,
        meeting_patterns
    )

    if matches:

        return (
            "Meeting or Event",
            min(
                0.95,
                0.75 + 0.05 * len(matches)
            ),
            "Meeting or Event Detected: "
            + ", ".join(matches[:3])
        )


    # Action Required
    matches = find_matches(
        text,
        action_patterns
    )

    if matches:

        return (
            "Action Required",
            min(
                0.95,
                0.75 + 0.05 * len(matches)
            ),
            "The message contains an explicit action or deadline"
        )


    # Personal Information
    matches = find_matches(
        text,
        personal_patterns
    )

    if matches:

        return (
            "Personal Information",
            min(
                0.92,
                0.72 + 0.05 * len(matches)
            ),
            "The message contains personal or profile related information"
        )


    # General Information
    return (
        "General Information",
        0.70,
        "The message provides general information"
    )


# ============================================================
# PART 2: TASK AND EVENT EXTRACTION
# ============================================================

task_words = [
    "submit",
    "complete",
    "finish",
    "send",
    "prepare",
    "upload",
    "review",
    "call",
    "remind",
    "deadline",
    "due",
    "todo",
    "to-do"
]


meeting_words = [
    "meeting",
    "meet",
    "discussion",
    "call",
    "conference",
    "appointment",
    "interview"
]


event_words = [
    "event",
    "workshop",
    "seminar",
    "webinar",
    "birthday",
    "ceremony",
    "party"
]


def detect_type(message):

    text = str(message).lower()

    if any(word in text for word in task_words):
        return "task"

    if any(word in text for word in meeting_words):
        return "meeting"

    if any(word in text for word in event_words):
        return "event"

    return None


def extract_date(message):

    pattern = r'\b\d{4}-\d{2}-\d{2}\b'

    match = re.search(
        pattern,
        message
    )

    if match:
        return match.group()

    return None


def extract_time(message):

    pattern = r'\b\d{1,2}:\d{2}\s?(?:AM|PM|am|pm)?\b'

    match = re.search(
        pattern,
        message
    )

    if match:
        return match.group()

    return None


def extract_person(message):

    patterns = [
        r'\bcall\s+(?:from\s+)?([A-Z][a-z]+)\b',
        r'\bwith\s+([A-Z][a-z]+)\b',
        r'\bto\s+([A-Z][a-z]+)\b',
        r'\bfrom\s+([A-Z][a-z]+)\b'
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            message
        )

        if match:
            return match.group(1)

    return None


def detect_priority(message):

    text = str(message).lower()

    if any(
        word in text
        for word in [
            "urgent",
            "asap",
            "immediately",
            "critical"
        ]
    ):
        return "high"

    if any(
        word in text
        for word in [
            "important",
            "soon"
        ]
    ):
        return "medium"

    return "low"


def extract_item(message):

    message = str(message)

    item_type = detect_type(message)

    if item_type is None:
        return None

    return {
        "type": item_type,
        "title": message[:80],
        "date_or_deadline": extract_date(message),
        "time": extract_time(message),
        "person": extract_person(message),
        "priority": detect_priority(message)
    }


# ============================================================
# PART 3: SENSITIVE INFORMATION DETECTION
# ============================================================

def detect_sensitive(message):

    text = str(message)

    findings = []


    # OTP
    if re.search(
        r'\b(?:OTP|one[- ]time password)\b',
        text,
        re.IGNORECASE
    ):

        findings.append(
            (
                "one_time_password",
                "high",
                "do_not_store"
            )
        )


    # Password
    if re.search(
        r'\bpassword\b',
        text,
        re.IGNORECASE
    ):

        findings.append(
            (
                "password",
                "high",
                "do_not_store"
            )
        )


    # Card / Bank payment details
    if re.search(
        r'\b(?:\d[ -]?){13,19}\b',
        text
    ):

        findings.append(
            (
                "bank_payment_details",
                "high",
                "do_not_store"
            )
        )


    if re.search(
        r'\b(?:bank account|account number|account no)\b',
        text,
        re.IGNORECASE
    ):

        findings.append(
            (
                "bank_payment_details",
                "high",
                "do_not_store"
            )
        )


    # Authentication token
    if re.search(
        r'\b(?:token|auth token|access token|api key)\b',
        text,
        re.IGNORECASE
    ):

        findings.append(
            (
                "authentication_token",
                "high",
                "do_not_store"
            )
        )


    # Private address
    if re.search(
        r'\b(?:home address|address|residential address|street address)\b',
        text,
        re.IGNORECASE
    ):

        findings.append(
            (
                "private_address",
                "medium",
                "do_not_send_to_external_service"
            )
        )


    return findings


# ============================================================
# MASK SENSITIVE INFORMATION
# ============================================================

def mask_sensitive_text(message):

    text = str(message)


    # OTP values
    text = re.sub(
        r'(\b(?:OTP|one[- ]time password)\b\s*(?:is|:)?\s*)\d{4,8}',
        r'\1******',
        text,
        flags=re.IGNORECASE
    )


    # Password values
    text = re.sub(
        r'(\bpassword\b\s*(?:is|:)?\s*)\S+',
        r'\1******',
        text,
        flags=re.IGNORECASE
    )


    # PIN values
    text = re.sub(
        r'(\bPIN\b\s*(?:is|:)?\s*)\d{4,8}',
        r'\1******',
        text,
        flags=re.IGNORECASE
    )


    # Card numbers
    text = re.sub(
        r'\b(?:\d[ -]?){13,19}\b',
        '****************',
        text
    )


    # Account numbers
    text = re.sub(
        r'(\b(?:account number|account no)\b\s*(?:is|:)?\s*)\d+',
        r'\1******',
        text,
        flags=re.IGNORECASE
    )


    # API keys / tokens
    text = re.sub(
        r'(\b(?:token|auth token|access token|api key)\b\s*(?:is|:)?\s*)\S+',
        r'\1******',
        text,
        flags=re.IGNORECASE
    )


    # Addresses
    text = re.sub(
        r'(\b(?:home address|residential address|street address|address)\b\s*(?:is|:)?\s*)[^.!?\n]+',
        r'\1******',
        text,
        flags=re.IGNORECASE
    )


    return text


# ============================================================
# STREAMLIT USER INTERFACE
# ============================================================

st.subheader("Enter a message")

message = st.text_area(
    "Message",
    placeholder="Example: Meeting with Rahul tomorrow at 10:00 AM",
    height=120
)


if st.button("Process Message"):

    if not message.strip():

        st.warning("Please enter a message.")

    else:

        # ----------------------------------------------------
        # 1. MESSAGE CLASSIFICATION
        # ----------------------------------------------------

        category, confidence, reason = classify_message(
            message
        )

        st.subheader("1. Message Classification")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Category",
                category
            )

        with col2:
            st.metric(
                "Confidence",
                f"{confidence:.2f}"
            )

        st.write("Reason:", reason)


        # ----------------------------------------------------
        # 2. TASK / EVENT EXTRACTION
        # ----------------------------------------------------

        st.subheader("2. Task & Event Extraction")

        extracted_item = extract_item(message)

        if extracted_item is None:

            st.info(
                "No task, meeting, or event detected."
            )

        else:

            extraction_df = pd.DataFrame(
                [extracted_item]
            )

            st.dataframe(
                extraction_df,
                use_container_width=True,
                hide_index=True
            )


        # ----------------------------------------------------
        # 3. SENSITIVE INFORMATION DETECTION
        # ----------------------------------------------------

        st.subheader(
            "3. Sensitive Information Detection"
        )

        findings = detect_sensitive(message)

        if not findings:

            st.success(
                "No sensitive information detected."
            )

        else:

            masked_message = mask_sensitive_text(
                message
            )

            st.write("Masked Message:")
            st.code(masked_message)

            sensitive_results = []

            for sensitivity_type, risk, action in findings:

                sensitive_results.append(
                    {
                        "sensitivity_type": sensitivity_type,
                        "risk": risk,
                        "recommended_action": action
                    }
                )

            sensitive_output = pd.DataFrame(
                sensitive_results
            )

            st.dataframe(
                sensitive_output,
                use_container_width=True,
                hide_index=True
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "AI Message Processing System | "
    "Rule-based message classification and information extraction"
)
