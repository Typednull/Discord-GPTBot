import spacy
from spacy.matcher import Matcher
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

def parse_response_to_json(response_text):
    logger.debug("Parsing response text: %s", response_text)

    doc = nlp(response_text)
    matcher = Matcher(nlp.vocab)
    
    # Define patterns for the matcher
    patterns = [
    {"label": "create_channel", "pattern": [{"LOWER": "create"}, {"LOWER": {"IN": ["a", "an"]}, "OP": "?"}, {"LOWER": {"IN": ["text", "voice"]}, "OP": "?"}, {"LOWER": "channel"}, {"LOWER": {"IN": ["named", "called"]}, "OP": "?"}, {"IS_QUOTE": True, "OP": "+"}, {"LOWER": {"IN": ["in", "under"]}, "OP": "?"}, {"LOWER": "category"}, {"IS_QUOTE": True, "OP": "+"}]},
    {"label": "assign_role", "pattern": [{"LOWER": "assign"}, {"LOWER": {"IN": ["the"]}, "OP": "?"}, {"LOWER": "role"}, {"IS_QUOTE": True, "OP": "+"}, {"LOWER": "to"}, {"LOWER": {"IN": ["user", "member"]}}, {"IS_QUOTE": True, "OP": "+"}]},
    {"label": "delete_channel", "pattern": [{"LOWER": "delete"}, {"LOWER": {"IN": ["a", "an"]}, "OP": "?"}, {"LOWER": {"IN": ["text", "voice"]}, "OP": "?"}, {"LOWER": "channel"}, {"LOWER": {"IN": ["named", "called"]}, "OP": "?"}, {"IS_QUOTE": True, "OP": "+"}]},
    {"label": "rename_channel", "pattern": [{"LOWER": "rename"}, {"LOWER": {"IN": ["a", "an"]}, "OP": "?"}, {"LOWER": {"IN": ["text", "voice"]}, "OP": "?"}, {"LOWER": "channel"}, {"LOWER": {"IN": ["named", "called"]}, "OP": "?"}, {"IS_QUOTE": True, "OP": "+"}, {"LOWER": "to"}, {"IS_QUOTE": True, "OP": "+"}]},
    {"label": "add_user", "pattern": [{"LOWER": "add"}, {"LOWER": {"IN": ["user", "member"]}}, {"LOWER": {"IN": ["to", "in"]}, "OP": "?"}, {"LOWER": {"IN": ["channel", "group"]}, "OP": "?"}, {"IS_QUOTE": True, "OP": "+"}]},
    {"label": "remove_user", "pattern": [{"LOWER": "remove"}, {"LOWER": {"IN": ["user", "member"]}}, {"LOWER": {"IN": ["from", "in"]}, "OP": "?"}, {"LOWER": {"IN": ["channel", "group"]}, "OP": "?"}, {"IS_QUOTE": True, "OP": "+"}]}
    # Add more patterns as needed
]

    for pattern in patterns:
        matcher.add(pattern["label"], [pattern["pattern"]])

    matches = matcher(doc)
    command_details = {"action": "unknown", "parameters": {}}

    for match_id, start, end in matches:
        action = nlp.vocab.strings[match_id]
        span = doc[start:end]
        logger.debug("Match found for %s: %s", action, span.text)

        # Extract parameters using entity recognition
        entities = [(ent.text, ent.label_) for ent in span.ents]
        command_details = {
            "action": action,
            "parameters": {"entities": entities}  # Store entities as parameters
        }

    if command_details["action"] == "unknown":
        logger.debug("No valid command parsed.")
        return {"error": "Invalid command"}

    return command_details

def interpret_command(command_text):
    response_text = command_text
    return response_text

# Example usage:
command_text = "Nexys create a channel in Text Channels called Test"
response_text = interpret_command(command_text)
command_details = parse_response_to_json(response_text)
logger.info("Parsed command details: %s", command_details)