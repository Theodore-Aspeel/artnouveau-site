# ANAD 2.0 - Media rights policy

## Purpose

Every published image must have an explicit, auditable rights record before a
publication can be approved.

The internal registry is research/media-rights.json. It stays outside the
public article payload because provenance and clearance evidence are
operational metadata. Reader-facing credit remains a presentation concern.

## Current corpus decision

On 2026-09-15, the project owner confirmed that all 21 images currently used
by the public runtime were made by his father, Christophe Aspel, and are cleared
for ANAD. The registry records the exact snapshot of files covered by that
statement. It deliberately does not use a wildcard, so a future import cannot
inherit clearance silently.

The public credit for this collection is Photographie : Christophe Aspel.
For contract version 1, this value is the internal reference used by the
general attribution on the public Mentions page; it is not repeated under
every photograph.

## Rules

- Every runtime image path must occur exactly once in the registry.
- Every registered image used at runtime must have rights_status set to cleared.
- Reuse of one cleared image by several articles is allowed.
- A new image must be added explicitly before the quality gate can pass.
- Archival, licensed, public-domain and third-party images are outside contract
  version 1. Before one is used, the contract must be extended with an
  asset-level record for source, visible credit and permission or licence.
- Private contact details, contracts and personal notes never belong in the
  public article payload.
- Any disputed or uncertain image stays blocked until resolved.

## Human approval

The automated gate verifies coverage, clearance and file presence. The human
reviewer still confirms that photographs are relevant, correctly ordered and
acceptably cropped in the preview.
