# AGENTS.md

Rules for anyone (human or automated agent) changing this public SDK repository.

1. **Push from clean, single-branch clones only.** Work in a fresh clone of one branch (`git clone --single-branch`). Never push from a working copy that has local-only branches, stashes, uncommitted files or unpushed commits.
2. **Leak audit before every push and every publish.** Run a secret scan over the full history (gitleaks and trufflehog) and a search of the tree, all commits, commit messages and the built package for internal material: non-public routes, internal hostnames, cloud-run style hosts, local file paths, webhook URLs, internal repository or branch names, names of server-side technology, planning labels, and vendor names under NDA. Every count must be 0, or each remaining hit must be reviewed and justified in writing. Do not push or publish otherwise.
3. **Build from the public API specification only.** The SDK is generated and written from the allow-listed public API specification. Never copy from, read, or reference server implementation code, and never mention how the service is implemented.
4. **No external uploads, registrations or submissions without explicit approval.** Publishing to a package registry, registering a namespace, submitting to a directory or any other third-party service needs explicit approval from the maintainer first.
5. **No browser automation of a maintainer's own logged-in browser.**
6. **Least privilege in CI.** Every workflow declares `permissions` explicitly (read-only by default); only the publish job gets `id-token: write`.
7. **Public history only.** Commit messages, code comments, tests and docs must be understandable and appropriate for the public.
