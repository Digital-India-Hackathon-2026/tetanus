from enum import Enum

class GeminiModel(str, Enum):
    GEMINI_1_5_FLASH = "gemini-1.5-flash"
    GEMINI_2_5_FLASH = "gemini-2.5-flash"
    GEMINI_2_5_PRO = "gemini-2.5-pro"
    GEMINI_2_0_FLASH = "gemini-2.0-flash"
    GEMINI_2_0_FLASH_LITE = "gemini-2.0-flash-lite-preview-02-05"
    GEMINI_2_0_PRO_EXP = "gemini-2.0-pro-exp-02-05"
    GEMINI_FLASH_LITE_LATEST = "gemini-flash-lite-latest"
