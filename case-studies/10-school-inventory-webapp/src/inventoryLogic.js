// Pure functions behind SchoolInventory.jsx. No React, no Firebase, so they can be
// tested with plain `node --test`. The component imports these instead of doing the
// same work inline.

export const CATEGORIES = ["instrumento", "suministro"];
export const STATUSES = ["bueno", "reparacion", "fuera"];
export const NEEDS_ATTENTION = new Set(["reparacion", "fuera"]);

export function filterItems(items, { category = "todos", status = "todos", search = "" } = {}) {
  const q = search.trim().toLowerCase();
  return items.filter((i) => {
    if (category !== "todos" && i.category !== category) return false;
    if (status !== "todos" && i.status !== status) return false;
    if (q && !`${i.name} ${i.type} ${i.location}`.toLowerCase().includes(q)) return false;
    return true;
  });
}

export function computeStats(items) {
  return {
    total: items.length,
    instrumentos: items.filter((i) => i.category === "instrumento").length,
    suministros: items.filter((i) => i.category === "suministro").length,
    atencion: items.filter((i) => NEEDS_ATTENTION.has(i.status)).length,
  };
}

// Returns null when the item isn't valid enough to save. The form relies on this so an
// empty name or a negative quantity never reaches storage.
export function validateItem(item) {
  const errors = [];
  if (!item.name || !item.name.trim()) errors.push("name");
  if (!CATEGORIES.includes(item.category)) errors.push("category");
  if (!STATUSES.includes(item.status)) errors.push("status");
  if (!Number.isInteger(Number(item.quantity)) || Number(item.quantity) < 0) errors.push("quantity");
  return errors;
}

export function upsertItem(items, item) {
  const exists = items.some((i) => i.id === item.id);
  return exists ? items.map((i) => (i.id === item.id ? item : i)) : [...items, item];
}

export function removeItem(items, id) {
  return items.filter((i) => i.id !== id);
}

// Newest entry first, and the entry is attributed to someone even if the coordinator
// never typed a name. "Anónimo" is better than an empty string in an audit trail.
export function addRepairEntry(item, note, by, date = new Date().toISOString()) {
  const clean = (note || "").trim();
  if (!clean) return item;
  const entry = { date, note: clean, by: (by || "").trim() || "Anónimo" };
  return { ...item, repairHistory: [entry, ...(item.repairHistory || [])] };
}
