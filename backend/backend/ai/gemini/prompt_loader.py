import os
from pathlib import Path

class PromptLoader:
    """Generic loader for retrieving prompts from the file system."""
    
    def __init__(self, base_dir: str = None):
        if base_dir is None:
            # Default to backend/ai/prompts
            self.base_dir = Path(__file__).resolve().parent.parent / "prompts"
        else:
            self.base_dir = Path(base_dir)
            
    def load_prompt(self, filename: str) -> str:
        """
        Loads the content of a prompt file.
        Does not perform any domain logic or string interpolation.
        """
        filepath = self.base_dir / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Prompt file not found: {filepath}")
            
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
