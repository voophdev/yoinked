from pathlib import Path


class Router:
    def __init__(self, rules: dict):
        self.rules = rules

    def get_destination(self, file_name: str) -> dict:
        extension = Path(file_name).suffix.lower().lstrip(".")

        best_match = None
        best_priority = float("inf")
        best_rule_name = None
        best_match_type = None

        for rule_name, rule in self.rules.items():
            if rule_name == "default":
                continue

            priority = rule.get("priority", 100)

            # 1. filename match (strong signal)
            if self._matches_filename(file_name, rule):
                if priority < best_priority:
                    best_match = rule
                    best_priority = priority
                    best_rule_name = rule_name
                    best_match_type = "filename"
                continue

            # 2. extension match
            if extension in rule.get("extensions", []):
                if priority < best_priority:
                    best_match = rule
                    best_priority = priority
                    best_rule_name = rule_name
                    best_match_type = "extension"

        if best_match:
            return {
                "destination": best_match["move_to"],
                "rule": best_rule_name,
                "match": best_match_type
            }

        default_rule = self.rules.get("default", {})

        return {
            "destination": default_rule.get("move_to", "Unsorted/"),
            "rule": "default",
            "match": "default"
        }

    def _matches_filename(self, file_name: str, rule: dict) -> bool:
        keywords = rule.get("filename_contains", [])
        file_lower = file_name.lower()

        return any(keyword.lower() in file_lower for keyword in keywords)
