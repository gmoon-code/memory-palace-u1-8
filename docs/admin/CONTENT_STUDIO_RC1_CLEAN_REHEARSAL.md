# Content Studio RC1 Clean Install and Recovery Rehearsal

This gate exercises the frozen Content Studio `1.0.0-rc1` implementation from a clean temporary copy. It does not modify the frozen implementation, production `main`, AP Biology curriculum files, or the public student runtime.

## Exact release under test

- Frozen implementation commit `cdf4bb2a1ea91415dd1634323ac5ab40ccba863f`
- Frozen implementation tree `133a3bc9b00c2149662d4e6dba8517f0706b585c`
- Production baseline `6d561f19a19b07b9a386442d327db3ca12299bef`
- Release candidate `1.0.0-rc1`

The rehearsal expands the exact tracked-file manifest for the frozen implementation, creates a clean `git archive` copy, and verifies every extracted tracked path, file size, and Git blob identity before starting Content Studio.

## Rehearsal sequence

The automated gate then performs the following sequence entirely inside the temporary copy.

1. Confirm there is no local credential file or pre-existing private database state.
2. Run the real first-use owner setup and verify the plaintext password is never written to local configuration.
3. Confirm loopback binding and all publication, GitHub publication, and merge locks are off.
4. Start Content Studio on a dynamically selected `127.0.0.1` port.
5. Sign in through the real owner-authentication route and obtain the CSRF token.
6. Create and save a harmless working-copy edit for a real Unit 8 scene.
7. Restart the local server and confirm the draft survives the process restart.
8. Run Content Health and the allowlisted `checkpoint_databases` repair action through the authenticated CSRF-protected API.
9. Confirm controlled publication, GitHub delivery, and merge remain disabled, then verify a publication-candidate request is rejected while local zero-cost mode is active.
10. Stop Content Studio and create a local backup with its SHA-256 sidecar.
11. Restart Content Studio, deliberately change the rehearsal draft after the backup, and stop the server again.
12. Restore the validated backup and restart Content Studio.
13. Sign in again and verify the rehearsal draft has returned to the exact pre-backup state.
14. Re-run health and publication-lock checks after recovery.
15. Run the frozen Windows-launcher, updater-safety, and Health/Repair acceptance helpers inside the clean copy.
16. Compare AP Biology content and student frontend bytes from before and after the rehearsal and require an exact match.

## Safety boundaries

The gate uses temporary local files only. Publication remains disabled throughout the runtime rehearsal. No GitHub publication or merge request is made. No real teacher credentials are used. The rehearsal password exists only inside the temporary CI workspace and is verified absent from the generated configuration file.

The zero-cost requirement remains mandatory. The rehearsal uses no hosting account, cloud database, paid API, billing account, payment method, or paid persistent storage.

## Automated command

The release gate is

```bash
python scripts/qa_content_studio_rc1_clean_rehearsal.py
```

A passing run must end with `CONTENT STUDIO RC1 CLEAN INSTALL/RECOVERY REHEARSAL PASS`.
