import sys
from pathlib import Path

import anthropic

SKILL_PATH = Path(__file__).parent / ".claude" / "skills" / "photo-captions" / "SKILL.md"

OUTPUT_FORMAT_INSTRUCTIONS = """You are a bilingual French/English assistant that helps the user write photo captions, titles, and comments for friends and family. The user gives you a sentence in either French or English.

Respond in exactly this format, with no extra commentary:

Original language: <French or English>
Corrected: <the sentence with grammar and spelling fixed, in the same language, in caption style>
Translation: <the corrected sentence translated to the other language, in caption style>

If the original is already correct, repeat it unchanged on the "Corrected" line.

Follow the style and name-correction rules below."""


def load_skill_body(skill_path: Path) -> str:
    """Read a SKILL.md file and return its body, stripping YAML frontmatter."""
    text = skill_path.read_text(encoding="utf-8")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return text.strip()


def main():
    if len(sys.argv) < 2:
        print('Usage: python main.py "<sentence>"')
        sys.exit(1)

    sentence = " ".join(sys.argv[1:])
    system_prompt = OUTPUT_FORMAT_INSTRUCTIONS + "\n\n" + load_skill_body(SKILL_PATH)

    client = anthropic.Anthropic()

    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1024,
        thinking={"type": "adaptive"},
        system=[
            {
                "type": "text",
                "text": system_prompt,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[{"role": "user", "content": sentence}],
    )

    for block in response.content:
        if block.type == "text":
            print(block.text)


if __name__ == "__main__":
    main()
