# wiki-references-normalizer

Stateless normalization of MediaWiki citation wikitext.

This standalone package (`citation_normalizer`) transforms raw wikitext reference strings into a consistent form so that two references with the same meaning but different formatting produce the same output. It is used by [wiki-references-db](../README.md) to deduplicate references before hashing and storage.

## Installation

```bash
cd refs_normalizer
pip install .
```

The only runtime dependency is [`mwparserfromhell`](https://github.com/earwig/mwparserfromhell) ≥ 0.6.

## Quick start

```python
from citation_normalizer import normalize_wikitext

raw = """
{{Cite_web
| url        = http://example.com
| title      = Example
| access-date = 2023-05-19
}}
"""

print(normalize_wikitext(raw))
# {{Cite web|access-date=2023-05-19|title=Example|url=http://example.com}}
```

## What normalization does

`normalize_wikitext` parses a wikitext string and applies the following transformations:

| Transformation                                                                              | Example                                                                                   |
|---------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| **Strip leading/trailing whitespace**                                                       | `\n{{Cite web\|…}}\n` → `{{Cite web\|…}}`                                                 |
| **Capitalize template names**                                                               | `{{cite web}}` → `{{Cite web}}`                                                           |
| **Replace underscores with spaces** in template names, parameter names, and wikilink titles | `[[Honolulu_Star-Bulletin]]` → `[[Honolulu Star-Bulletin]]`                               |
| **Alphabetize named parameters**                                                            | `\|title=...\|author=...` → `\|author=...\|title=...`                                     |
| **Collapse whitespace** in parameter values                                                 | `{{Cite web\n\|url=https://example.com}}` → `{{Cite web\|url=https://example.com}}`       |
| **Strip padding** around parameter names and values                                         | `\| foo = bar ` → `\|foo=bar`                                                             |
| **Normalize `<ref>` tags**                                                                  | `<ref name=foo>\nhttps://example.com</ref>` → `<ref name="foo">https://example.com</ref>` |
| **Ensure a space after list markers** (`*`, `#`, `:`)                                       | `#*Hello` → `#* Hello`                                                                    ||

## API reference

### Normalization (`citation_normalizer.syntax`)

| Function | Description |
|---|---|
| `normalize_wikitext(wikitext: str) -> str` | Normalize a complete wikitext string. Main entry point. |
| `normalize_node(node)` | Normalize a single `mwparserfromhell` node (template, tag, link, etc.). |
| `normalize_template(template)` | Normalize a `Template` node: capitalize name, sort params, collapse whitespace. |
| `normalize_ref_tag(tag)` | Normalize a `<ref>` `Tag` node: strip content whitespace, quote the `name` attribute. |
| `get_sha1(*args) -> str` | SHA-1 hex digest of the concatenated string representations of all arguments. |

### Sanitization (`citation_normalizer.sanitize`)

| Function | Description |
|---|---|
| `sanitize_ref_name(name: str) -> str \| None` | Truncate a `<ref name="…">` value at the first disallowed character. Returns `None` if the result is empty. |
| `sanitize_extracted_name(name: str) -> str \| None` | Same allowlist-based truncation for extracted template/reference names. |
| `normalize_template_name(name: str) -> str` | Lowercase, strip, and replace underscores with spaces in a template name. |

## CLI usage

You can normalize a single wikitext string from the command line:

```bash
python -m citation_normalizer.syntax '{{cite_web | url = http://example.com | title = Test}}'
# {{Cite web|title=Test|url=http://example.com}}
```

## Running tests

```bash
pip install pytest
pytest tests/
```
