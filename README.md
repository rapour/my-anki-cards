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
- The file name is never shown on the card. Name files in whatever way helps you find them.

## Topics

Folders under `src/` are topics, nested as deep as you like. `src/databases/sql/select-distinct.md` becomes:

| Where | Value |
|---|---|
| Deck | `My Anki Cards::databases::sql` |
| Tag | `databases::sql` (spaces in folder names become `_`) |
| Card header | `databases › sql` |

Cards placed directly in `src/` go into the `My Anki Cards` deck and have no topic.

## Getting the deck

### Latest build

Every push to `main` runs the **Build deck** workflow, which replaces the `latest` release. The newest deck is always at:

https://github.com/rapour/my-anki-cards/releases/download/latest/my-anki-cards.apkg

You don't need to sign in to GitHub to download it. For a few seconds during each run the link returns 404 while the release is replaced. See [Importing into Anki](#importing-into-anki) for how to use it on each device.

### A specific commit

Each run also keeps `my-anki-cards.apkg` as an artifact. Open the run on the Actions tab to download it. Downloading artifacts requires signing in to GitHub.

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

## Importing into Anki

The link points straight at the `.apkg` file, so every Anki app imports it the same way: download the file, then open it in Anki.

| Setup | How to import |
|---|---|
| Android (AnkiDroid) | Open the link in your browser. When the download finishes, tap it and choose AnkiDroid. Alternatively, open the ⋮ menu in AnkiDroid's deck list, choose **Import** and pick the file from Downloads. |
| Desktop (Windows, macOS, Linux) | Download the file with your browser. In Anki, choose **File › Import** and pick it. Double-clicking the file also works when Anki is registered to open `.apkg` files. |
| iPhone and iPad (AnkiMobile) | Open the link in Safari and download the file. Find it in Safari's downloads or the Files app, open its share menu and choose AnkiMobile. |
| AnkiWeb | AnkiWeb can't import files. Import on one of the apps above and sync. |

### Several devices

If your devices sync through AnkiWeb, import on one device only and let sync carry the cards to the others. Importing the same deck separately on several synced devices can create duplicate cards.

## Re-importing

To get new and edited cards, download from the same link and import again. If the import screen shows an **Update notes** option, leave it on **If newer**, the default, so edited cards are updated.

Each card's identity comes from its path under `src/`. Importing a newer build updates existing cards in place and keeps their review history. Note that:

- **Renaming or moving a file** creates a new card. Delete the old one in Anki.
- **Deleting a file** does not remove the card from Anki, because importing only adds and updates. Delete it in Anki yourself.
