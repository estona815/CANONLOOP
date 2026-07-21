# Security

Credentials are server-only, excluded from Git, and redacted from errors. Use a bucket-scoped
Backblaze application key rather than a master key. The API validates uploads, object keys,
archive paths, prompt length, cost confirmation, retry limits, and allowed origins. Report
security issues privately to the repository owner rather than opening a public issue.

