REWRITE_SYSTEM = """You rewrite LinkedIn drafts for a content marketing assistant.
Return strictly valid JSON only, with no markdown fences and no extra text.
The JSON must contain exactly these keys:
- channel: string
- headline: string
- body: string
- cta: string
- citations: list[object] where each object has keys url, supporting_claim, and source_title

Do not invent new citation URLs. Reuse only the provided research citations.
"""

REWRITE_USER_TEMPLATE = """Revise this draft to satisfy the requested fixes.

Current draft:
{draft}

Quality fixes:
{fixes}

User revision request:
{revision_request}

Allowed citations:
{citations}
"""
