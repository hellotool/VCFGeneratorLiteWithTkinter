---
name: prepare-release
description: Prepares a new release by updating version with uv, merging bilingual CHANGELOG entries into the new version section, and clearing the Unreleased section. Invoke when user asks to prepare a release or bump version.
---

# Prepare Release

This skill prepares a new release for the project.

## Algorithm

1. **Parse input**: Get the target version from user input (either a specific version like `6.1.0` or a bump type: `major`, `minor`, `patch`).

2. **Update version**: Run `uv version <VERSION>` or `uv version --bump <BUMP_TYPE>` to update `pyproject.toml`.

3. **Read CHANGELOG files**:
   - Read `CHANGELOG.md` (English).
   - Read `CHANGELOG.zh-CN.md` (Chinese).
   - If either file is missing or malformed, abort with an error.

4. **Find Unreleased section**:
   - In `CHANGELOG.md`, look for `## [Unreleased]`.
   - In `CHANGELOG.zh-CN.md`, look for `## [未发布]`.
   - If either section is missing, abort with an error.

5. **Extract Unreleased content**:
   - From `CHANGELOG.md`, capture all content between `## [Unreleased]` and the next `## [` heading.
   - From `CHANGELOG.zh-CN.md`, capture all content between `## [未发布]` and the next `## [` heading.
   - If both sections are empty (no content beyond the header), skip CHANGELOG merging.

6. **Create merged version section**:
   - Use today's date in `YYYY-MM-DD` format.
   - Merge all content from both `CHANGELOG.md` and `CHANGELOG.zh-CN.md` Unreleased sections into a unified list.
   - Translate the merged content into English for `CHANGELOG.md`.
   - Translate the merged content into Chinese for `CHANGELOG.zh-CN.md`.
   - Insert `## [VERSION] - YYYY-MM-DD` followed by the translated content in both files.

7. **Clear Unreleased section**:
   - In `CHANGELOG.md`, remove the Unreleased section's content (the content extracted in step 5), keeping only the header `## [Unreleased]`.
   - In `CHANGELOG.zh-CN.md`, remove the Unreleased section's content (the content extracted in step 5), keeping only the header `## [未发布]`.

8. **Validate**: Run the following commands:
   ```bash
   uv run poe format
   uv run poe check
   uv run poe test
   ```
   - If any command fails, abort and report the failure.

9. **Check for existing version**: If a section for the target version already exists, abort with an error.

## Usage

- Specific version: `uv version 6.1.0`
- Bump patch: `uv version --bump patch`
- Bump minor: `uv version --bump minor`
- Bump major: `uv version --bump major`

## Notes

- Version format follows PEP 440 (e.g., `6.0.0`, `6.0.1`, `6.1.0`).
- Do NOT commit changes after running this skill (per project rules).
