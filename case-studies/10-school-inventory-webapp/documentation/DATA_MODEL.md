# Data model

One collection, one document per item. Kept flat; a school inventory doesn't need relations.

| Field | Type | Meaning |
|---|---|---|
| id | string (UUID) | Stable key, generated client-side |
| name | string | Required. What the thing is called |
| category | `instrumento` or `suministro` | Drives the stats row and the category filter |
| type | string | Free text, e.g. "Bb", "14in" |
| quantity | integer ≥ 0 | Validated before save |
| location | string | Where it lives |
| status | `bueno`, `reparacion`, `fuera` | `reparacion` and `fuera` count as "needs attention" |
| assignedTo | string | Who has it, if anyone |
| notes | string | Free text |
| repairHistory | array of `{date, note, by}` | Newest first. `by` defaults to "Anónimo" so no entry is unattributed |
| createdAt | ISO timestamp | Set once |

Persistence is a Firebase document per item; the config is not in this repo. The pure logic in `src/inventoryLogic.js` is what decides what gets persisted.
