# Anonymization protocol

The artifact is safe for anonymous review because it removes or replaces the following information:

1. Organization names, author names, institutional paths, user names, and emails.
2. Proprietary source file paths and build target names.
3. Raw C/C++ source code and private CI configuration files.
4. Module names are replaced with stable anonymized identifiers such as `mod_0001`.
5. System names are replaced with `system_a`, `system_b`, and `system_c`.
6. Security-sensitive defect descriptions are mapped to coarse categories such as `memory_safety`, `range`, `assertion`, `resource_leak`, and `concurrency`.

The scripts use only relative paths and contain no absolute local path assumptions.
