import { test } from "node:test";
import assert from "node:assert/strict";
import { filterItems, computeStats, validateItem, upsertItem, removeItem, addRepairEntry } from "../src/inventoryLogic.js";

const items = [
  { id: "a", name: "Trompeta", category: "instrumento", type: "Bb", quantity: 3, location: "Bodega", status: "bueno", repairHistory: [] },
  { id: "b", name: "Redoblante", category: "instrumento", type: "14in", quantity: 2, location: "Salón 2", status: "reparacion", repairHistory: [] },
  { id: "c", name: "Parches", category: "suministro", type: "14in", quantity: 10, location: "Bodega", status: "fuera", repairHistory: [] },
];

test("filter by category, status and free text", () => {
  assert.equal(filterItems(items, { category: "instrumento" }).length, 2);
  assert.equal(filterItems(items, { status: "reparacion" })[0].id, "b");
  assert.deepEqual(filterItems(items, { search: "bodega" }).map((i) => i.id), ["a", "c"]);
  assert.equal(filterItems(items, { search: "14IN", category: "suministro" }).length, 1);
});

test("stats count what the header shows", () => {
  assert.deepEqual(computeStats(items), { total: 3, instrumentos: 2, suministros: 1, atencion: 2 });
});

test("validation blocks empty name, bad status and negative quantity", () => {
  assert.deepEqual(validateItem({ name: " ", category: "instrumento", status: "bueno", quantity: 1 }), ["name"]);
  assert.deepEqual(validateItem({ name: "Tuba", category: "instrumento", status: "perdido", quantity: -1 }), ["status", "quantity"]);
  assert.deepEqual(validateItem(items[0]), []);
});

test("upsert edits in place or appends, and never duplicates an id", () => {
  const edited = upsertItem(items, { ...items[0], quantity: 4 });
  assert.equal(edited.length, 3);
  assert.equal(edited[0].quantity, 4);
  const added = upsertItem(items, { ...items[0], id: "d" });
  assert.equal(added.length, 4);
});

test("remove drops exactly one item", () => {
  assert.deepEqual(removeItem(items, "b").map((i) => i.id), ["a", "c"]);
});

test("repair log is newest first, attributed, and ignores blank notes", () => {
  const once = addRepairEntry(items[1], "Cambio de parche", "", "2026-01-01T00:00:00.000Z");
  const twice = addRepairEntry(once, "Ajuste de tensores", "Coordinador", "2026-02-01T00:00:00.000Z");
  assert.equal(twice.repairHistory.length, 2);
  assert.equal(twice.repairHistory[0].note, "Ajuste de tensores");
  assert.equal(twice.repairHistory[1].by, "Anónimo");
  assert.equal(addRepairEntry(twice, "   ", "x").repairHistory.length, 2);
});
