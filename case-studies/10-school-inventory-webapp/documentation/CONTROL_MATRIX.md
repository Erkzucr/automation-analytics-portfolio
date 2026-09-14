# Control Matrix

Small app, small matrix. These are the things that stop the inventory from turning back into "we think we still have that".

| ID | Objective | Procedure | Evidence |
|---|---|---|---|
| CTL-01 | No item without a name | `validateItem` blocks save on empty name | tests T03 |
| CTL-02 | Quantities make sense | Integer, zero or more | tests T03 |
| CTL-03 | Status is one of three known values | Allowlist in `inventoryLogic.js` | tests T03 |
| CTL-04 | Every repair entry is attributed and dated | `addRepairEntry` fills `by` and `date` | tests T07 |
| CTL-05 | History is never overwritten | Entries prepend, nothing edits old ones | tests T07 |
| CTL-06 | Edits don't create duplicates | Upsert by id | tests T04 |
| CTL-07 | Secrets stay out of the repo | Firebase config excluded | README, .gitignore |
