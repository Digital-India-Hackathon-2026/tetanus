from jinja2 import Environment, StrictUndefined, meta
from typing import Dict, Any, List
from .exceptions import PromptValidationError

class TemplateEngine:
    """
    Abstract wrapper for the prompt rendering engine.
    Currently backed by Jinja2 with strict validation and autoescaping disabled.
    """
    def __init__(self):
        # StrictUndefined ensures missing variables crash the render instead of silently inserting blanks
        self.env = Environment(
            undefined=StrictUndefined,
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True
        )

    def extract_variables(self, template_str: str) -> List[str]:
        """Extracts all variable names required by the template."""
        ast = self.env.parse(template_str)
        return list(meta.find_undeclared_variables(ast))

    def render(self, template_str: str, context: Dict[str, Any]) -> str:
        """
        Renders the template with the provided context dictionary.
        Raises PromptValidationError if variables are missing.
        """
        try:
            template = self.env.from_string(template_str)
            return template.render(**context)
        except Exception as e:
            # Catch Jinja2 UndefinedError or Syntax errors
            raise PromptValidationError(f"Template rendering failed: {str(e)}")
