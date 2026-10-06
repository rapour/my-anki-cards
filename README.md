# my-anki-cards

Flashcards written as Markdown and built into an Anki package (`.apkg`) on every push to `main`.

## Writing a card

Each `.md` file under `src/` is one card. The question comes first, followed by a line containing only `---`, followed by the answer:

````markdown
What does `SELECT DISTINCT` do?

---

Removes duplicate rows from the result set.

```sql
SELECT DISTINCT country FROM customers;
```
````

- Both sides are Markdown: paragraphs, lists, tables, inline code and fenced code blocks.
- Math uses `$...$` inline and `$$...$$` for blocks, and is rendered by Anki's MathJax.
- The first `---` outside a code block is the separator. Any later `---` in the answer is rendered as a horizontal rule.
- The file name is never shown on the card. Name files however helps you find them.

## Topics

Folders under `src/` are topics, nested as deep as you like. `src/databases/sql/select-distinct.md` becomes:

| Where | Value |
|---|---|
| Deck | `My Anki Cards::databases::sql` |
| Tag | `databases::sql` (spaces in folder names become `_`) |
| Card header | `databases › sql` |

Cards placed directly in `src/` go into the `My Anki Cards` deck and have no topic.

## Getting the deck

### From CI

Every push to `main` runs the **Build deck** workflow. Open the run on the Actions tab and download `my-anki-cards.apkg` from its artifacts. On Android, do this in a browser where you are signed in to GitHub, then open the downloaded file with AnkiDroid.

### Building locally

With [uv](https://docs.astral.sh/uv/):

```sh
uv run --with-requirements requirements.txt scripts/build_deck.py src dist/my-anki-cards.apkg
```

Without uv:

```sh
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/build_deck.py src dist/my-anki-cards.apkg
```

The build fails and names the file when a card has no `---` separator, when either side is empty, or when `src/` holds no cards.

## Re-importing

Each card's identity comes from its path under `src/`. Importing a newer build updates existing cards in place and keeps their review history. Note that:

- **Renaming or moving a file** creates a new card. Delete the old one in Anki.
- **Deleting a file** does not remove the card from Anki, because importing only adds and updates. Delete it in Anki yourself.
