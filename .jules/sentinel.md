## 2026-11-17 - A documented fix is not a verified fix
**Vulnerability:** A prior journal entry described an unsafe deserialization path as removed, but the vulnerable branch was still present and reachable from a main entry point (insecure deserialization, CWE-502).
**Learning:** Journal notes and comments are not remediation; only a code change exercised through the real load path closes the finding. The unsafe branch had survived because safe structured-data loading already existed alongside it, so the old path was easy to miss.
**Prevention:** Remove unsafe deserializers from data-loading code entirely rather than leaving them as a fallback. Prove every removal with a regression test that feeds a payload which would execute on deserialization and asserts it never runs.
