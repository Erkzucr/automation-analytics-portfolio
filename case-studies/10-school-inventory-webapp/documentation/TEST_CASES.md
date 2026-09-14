# Test cases

Automated ones run with `node --test tests/*.test.js` and in CI. Manual ones are what I check in the browser before a release, because the UI isn't unit-tested.

## Automated (tests/inventoryLogic.test.js)

| ID | Scenario | Expected result |
|---|---|---|
| T01 | Filter by category, status and free text (case-insensitive) | Only matching items |
| T02 | Stats row | total, instrumentos, suministros, atencion match the data |
| T03 | Save with empty name, unknown status or negative quantity | Validation errors, nothing persisted |
| T04 | Edit an existing item | Replaced in place, count unchanged, id never duplicated |
| T05 | Add a new item | Appended |
| T06 | Delete | Exactly that id removed |
| T07 | Add repair note | Newest first, attributed, blank note ignored |

## Manual

| ID | Scenario | Expected result |
|---|---|---|
| M01 | Two coordinators edit different items at the same time | Both edits persist |
| M02 | Reload the page | Coordinator name remembered, data reloaded from Firebase |
| M03 | Search while a category filter is active | Both filters apply |
| M04 | Delete confirmation | Item only disappears after confirming |
