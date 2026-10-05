# Pinned skill packages

This is a minimal reproducible evaluation snapshot of 19 designated files, totaling 171,703 bytes, from [dot-skills commit 67bb5a82](https://github.com/SeungheonOh/dot-skills/tree/67bb5a82d3d97c1ee1bbbfaa3e695a604c3a0d56). [manifest.json](manifest.json) records each repository path, Git blob identity, and SHA-256.

The bytes are unchanged from that commit. Updating the repository's main `skill/` tree does not retarget this experiment. A different package version needs a new reviewed configuration and source identity.

Each S attempt receives only its own task's `skill_package.files` from [the source configuration](../pilot-source-config.json), preserving repository-relative paths. C receives none. Guides, approved examples, and helper files are all part of the treatment. These files are supplied material, not held-out evaluation tasks.

The text-merge guide contains cross-links to neighboring workflows. Those links do not authorize fetching or supplying extra skills. Some destinations are intentionally absent from this minimal snapshot; use the pinned repository link above to browse the complete source outside an evaluated attempt. Local link checks explicitly account for the three absent cross-package destinations rather than editing the pinned guide.

No package helper runs as part of the preparation checks. Runtime review must separately consider filesystem writes, dependencies, and timezone support before any future attempt executes a helper.
