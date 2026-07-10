# Ambiguity & Disambiguation

## Category Overlaps
*   **Electronics vs Study**: A "tablet" could be for entertainment (Electronics) or taking notes (Study).
    *   *Resolution*: Use `secondary_missions` and analyze co-occurring keywords (e.g., "for classes" -> Study).
*   **Home vs Kitchen**: "Storage containers" might overlap.
    *   *Resolution*: Rely on AIKB classification. If ambiguous, map to both categories in the intent response.
*   **Health vs Personal Care**: "Vitamins" vs "Shampoo".

## Broad Intent Overlaps
*   **"Need laptop"**: Could be Gaming, Office, College, or general Work.
    *   *Resolution*: Extract the literal keyword "laptop". Set mission confidence to Low (< 0.5) if no context is provided.

## Confidence Guidelines
*   **High Confidence (0.8 - 1.0)**: Explicit mission stated ("I am going to college").
*   **Medium Confidence (0.5 - 0.7)**: Contextual clues ("Need a laptop and notebooks").
*   **Low Confidence (0.0 - 0.4)**: Generic queries ("Show me laptops").
