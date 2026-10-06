import argparse
import hashlib
import html
import re
import sys
from pathlib import Path

import genanki
import markdown

ROOT_DECK = "My Anki Cards"

# Anki matches note types by this ID on import. Changing fields or templates
# under the same ID makes Anki create a duplicate note type, so pick a new ID.
MODEL_ID = 1738291046

CSS = """
.card {
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  font-size: 18px;
  line-height: 1.5;
  text-align: left;
  padding: 0 4px;
}
.topic {
  font-size: 12px;
  opacity: 0.6;
  margin-bottom: 12px;
}
code {
  font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
  font-size: 0.9em;
}
:not(pre) > code {
  padding: 1px 4px;
  border-radius: 4px;
  background: rgba(127, 127, 127, 0.15);
}
pre {
  overflow-x: auto;
  padding: 8px 12px;
  border-radius: 6px;
  background: rgba(127, 127, 127, 0.15);
}
table {
  border-collapse: collapse;
}
th, td {
  padding: 4px 8px;
  border: 1px solid rgba(127, 127, 127, 0.4);
}
"""

MODEL = genanki.Model(
    MODEL_ID,
    ROOT_DECK,
    fields=[{"name": "Front"}, {"name": "Back"}, {"name": "Topic"}],
    templates=[
        {
            "name": "Card 1",
            "qfmt": '{{#Topic}}<div class="topic">{{Topic}}</div>{{/Topic}}<div class="front">{{Front}}</div>',
            "afmt": '{{FrontSide}}<hr id="answer"><div class="back">{{Back}}</div>',
        }
    ],
    css=CSS,
)

MARKDOWN = markdown.Markdown(
    extensions=["fenced_code", "tables", "pymdownx.arithmatex"],
    extension_configs={"pymdownx.arithmatex": {"generic": True}},
)

FENCE_OPEN = re.compile(r" {0,3}(`{3,}|~{3,})")


class CardError(Exception):
    pass


def split_card(text):
    lines = text.splitlines()
    fence = ""
    for i, line in enumerate(lines):
        stripped = line.strip()
        if fence:
            if len(stripped) >= len(fence) and set(stripped) == {fence[0]}:
                fence = ""
        elif match := FENCE_OPEN.match(line):
            fence = match[1]
        elif stripped == "---":
            return "\n".join(lines[:i]).strip(), "\n".join(lines[i + 1 :]).strip()
    raise CardError("no '---' line separating front from back")


def render(source):
    return MARKDOWN.reset().convert(source)


def deck_id(name):
    digest = hashlib.sha256(name.encode("utf-8")).digest()
    return (1 << 30) + int.from_bytes(digest[:4], "big") % (1 << 30)


def build(src, out):
    paths = sorted(src.rglob("*.md"))
    if not paths:
        raise CardError(f"{src}: no .md files found")

    decks = {}
    errors = []
    for path in paths:
        relative = path.relative_to(src)
        topics = relative.parent.parts
        try:
            front, back = split_card(path.read_text(encoding="utf-8"))
            if not front or not back:
                raise CardError("front and back must both be non-empty")
        except CardError as error:
            errors.append(f"{path}: {error}")
            continue

        for depth in range(len(topics) + 1):
            name = "::".join((ROOT_DECK, *topics[:depth]))
            deck = decks.setdefault(name, genanki.Deck(deck_id(name), name))

        # The GUID is what lets a re-import update an existing note instead of
        # adding a new one, so it must stay derived from the path alone.
        deck.add_note(
            genanki.Note(
                model=MODEL,
                fields=[render(front), render(back), html.escape(" › ".join(topics))],
                tags=["::".join(topic.replace(" ", "_") for topic in topics)] if topics else [],
                guid=genanki.guid_for(relative.as_posix()),
            )
        )

    if errors:
        raise CardError("\n".join(errors))

    out.parent.mkdir(parents=True, exist_ok=True)
    genanki.Package(list(decks.values())).write_to_file(out)
    print(f"{out}: {len(paths)} cards")


def main():
    parser = argparse.ArgumentParser(description="Build an Anki package from Markdown cards.")
    parser.add_argument("src", type=Path)
    parser.add_argument("out", type=Path)
    args = parser.parse_args()
    try:
        build(args.src, args.out)
    except CardError as error:
        sys.exit(str(error))


if __name__ == "__main__":
    main()
