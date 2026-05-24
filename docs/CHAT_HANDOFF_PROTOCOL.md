# CHAT_HANDOFF_PROTOCOL.md

Status: canonical operational coordination protocol
Version: v0.1
Last updated: 2026-05-24

---

# 1. Purpose

This document defines lightweight coordination rules for the multi-chat project environment.

Goals:
- reduce drift
- reduce duplication
- preserve continuity
- minimise restart friction
- maintain operational clarity

---

# 2. Current Chat Structure

## Architecture Chat
Purpose:
- architectural reasoning
- provenance philosophy
- schema philosophy
- governance philosophy
- architectural risk analysis

Authority level:
- constitutional

---

## PM Chat
Purpose:
- operational sequencing
- milestone coordination
- continuity management
- interruption recovery
- scope discipline

Authority level:
- operational

---

## Build Chats
Purpose:
- bounded implementation work

Authority level:
- implementation only

Status:
- not yet established

---

# 3. Canonical Continuity Rule

Canonical continuity exists in:
- operational documents
- scripts
- manifests
- repositories

Not in:
- chat memory
- inferred assumptions
- scattered discussion

---

# 4. Session Start Discipline

At session start:

1. review CURRENT_STATE.md
2. review ACTIVE_ISSUES.md
3. define bounded session goal
4. define completion condition

---

# 5. Session End Discipline

At session end:

Update:
- CURRENT_STATE.md if state changed
- ACTIVE_ISSUES.md if risks changed

Record:
- what changed
- what remains unresolved
- exact next action
- restart instructions if needed

---

# 6. Chat Creation Rule

New chats should only be created when:
- bounded implementation work exists
- operational coordination burden justifies separation
- a specialist task stream genuinely exists

Avoid:
- premature chat proliferation
- governance fragmentation
- duplicated authority

---

# 7. Escalation Rule

Questions involving:
- provenance philosophy
- schema philosophy
- canonicalisation philosophy
- infrastructure philosophy
- major tooling additions
- scope expansion

should be escalated to the Architecture chat.

---

# 8. Operational Principle

The project should optimise for:
- delivery
- recoverability
- bounded complexity
- sustainable solo execution

not:
- governance sophistication
- excessive coordination
- organisational simulation