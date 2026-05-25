import sys
import anthropic

SYSTEM_PROMPT = """You are a bilingual French/English assistant. The user gives you a sentence in either French or English.

Respond in exactly this format, with no extra commentary:

Original language: <French or English>
Corrected: <the sentence with grammar and spelling fixed, in the same language>
Translation: <the corrected sentence translated to the other language>

If the original is already correct, repeat it unchanged on the "Corrected" line."""


def main():
    if len(sys.argv) < 2:
        print('Usage: python main.py "<sentence>"')
        sys.exit(1)

    sentence = " ".join(sys.argv[1:])
    client = anthropic.Anthropic()

    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1024,
        thinking={"type": "adaptive"},
        system=[
            {
                "type": "text",
                "text": SYSTEM_PROMPT,
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
