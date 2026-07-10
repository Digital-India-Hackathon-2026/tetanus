from .exceptions import InvalidResponseError

class GeminiResponseParser:
    """Agnostic parser for extracting text from the raw Gemini response."""
    
    @staticmethod
    def parse_text(raw_response: any) -> str:
        """
        Extracts and normalizes text from the google-genai response object.
        Raises InvalidResponseError if the text is empty or missing.
        """
        try:
            # For google-genai, response.text gives the full text
            text = raw_response.text
        except AttributeError:
            raise InvalidResponseError("Malformed response: 'text' attribute missing.")
        
        if not text:
            raise InvalidResponseError("Empty response received from Gemini.")
            
        return text.strip()
