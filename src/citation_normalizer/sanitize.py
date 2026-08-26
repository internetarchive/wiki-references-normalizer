import re

# Characters permitted in a reference name (allowlist).
_LEGAL_REF_NAME_RE = re.compile(r'^[\w .,:;!?\-+#@&=%()\'\[\]/]+$', re.UNICODE)


def sanitize_ref_name(name: str):
    """Truncate a ref name at the first character not in the allowlist."""
    if not name:
        return name
    for i, ch in enumerate(name):
        if not _LEGAL_REF_NAME_RE.match(ch):
            name = name[:i]
            break
    result = name.strip()
    return result if result else None


# Characters permitted in an extracted template/reference name (broad allowlist).
_LEGAL_EXTRACTED_NAME_RE = re.compile(r'^[\w .,:;!?\-+#@&=%()\'\[\]/]+$', re.UNICODE)


def sanitize_extracted_name(name: str):
    """Truncate an extracted name at the first pathological character."""
    if not name:
        return name
    for i, ch in enumerate(name):
        if not _LEGAL_EXTRACTED_NAME_RE.match(ch):
            name = name[:i]
            break
    result = name.strip()
    return result if result else None


def normalize_template_name(name: str) -> str:
    return name.strip().replace("_", " ").lower()
