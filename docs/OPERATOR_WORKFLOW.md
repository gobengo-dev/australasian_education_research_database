# OPERATOR_WORKFLOW.md

Status: canonical operator procedure

---

# Session Start

1. Pull latest repository changes.
2. Review:
   - CURRENT_STATE.md
   - ACTIVE_ISSUES.md
   - CHAT_INDEX.md
3. Open the current active PM chat.
4. State:
   - available time
   - intended work session
   - any interruptions or constraints.

---

# During Session

1. Work through bounded milestones.
2. Commit regularly.
3. Record commit hashes when requested by PM.
4. Escalate architectural questions to Architecture chat.

---

# Session End

1. Commit and push changes.
2. Provide PM with:
   - completed work
   - commit hashes
   - unexpected discoveries
   - unresolved issues
3. Update:
   - CURRENT_STATE.md (if state changed)
   - ACTIVE_ISSUES.md (if risks changed)
   - CHAT_INDEX.md (if chat status changed)
4. Retire completed chats if appropriate.

---

# Decision Rule

If unsure:

- operational question → PM
- architectural question → Architecture
- implementation question → Build chat

Do not invent a third path.