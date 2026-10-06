# Flow — Model install, verify, convert, delete (F5)

- Trigger: Install on the Models screen, the starter pack, or "Install <model>" on a task screen.
- Covers: AC-40, AC-41, AC-42, AC-43, AC-44, AC-52.

## Steps
1. System shows download size, disk after conversion and free space → user confirms.
2. Worker downloads the pinned revision from Hugging Face, file by file, resumable.
3. Worker verifies each file's sha256 against the catalogue.
4. Worker converts or quantizes to the chosen variant when the variant needs it.
5. System verifies the converted variant, then deletes the originals (AC-43).
6. State becomes ready; tasks that need the model unlock.

## Branches and failure paths
- Shared component (T5, VAE) already installed → not downloaded again; its used-by list grows.
- Hugging Face unreachable or rate-limited → backoff, then ModelScope; both failing → failed + Retry.
- Pause / quit → resumes from the completed files (AC-41).
- Checksum mismatch → the file is discarded and never used; failed + Retry (AC-42).
- Disk full mid-download or mid-conversion → stops cleanly, partial output removed, cause shown.
- Delete → removes the variant; shared components only when no installed model uses them (AC-44).
- Change variant → installs the new one before removing the old one, space permitting.
- Remote revision differs from the pinned one after an app update → "update available", offered
  with its size, never automatic (AC-52).
