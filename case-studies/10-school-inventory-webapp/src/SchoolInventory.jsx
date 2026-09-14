import { useState, useEffect } from "react";
import { filterItems, computeStats, validateItem, upsertItem, removeItem, addRepairEntry } from "./inventoryLogic.js";
import { Search, Plus, Music4, Package, Wrench, User, X, Trash2, Pencil, AlertTriangle, Check, History, ChevronRight } from "lucide-react";

const STATUS = {
  bueno: { label: "Bueno", dot: "bg-emerald-600", chip: "bg-emerald-50 text-emerald-800 border-emerald-200" },
  regular: { label: "Regular", dot: "bg-amber-500", chip: "bg-amber-50 text-amber-800 border-amber-200" },
  reparacion: { label: "Necesita reparación", dot: "bg-rose-600", chip: "bg-rose-50 text-rose-800 border-rose-200" },
  fuera: { label: "Fuera de servicio", dot: "bg-stone-500", chip: "bg-stone-100 text-stone-700 border-stone-300" },
};

const CATS = {
  instrumento: { label: "Instrumento", icon: Music4 },
  suministro: { label: "Suministro", icon: Package },
};

const emptyItem = () => ({
  id: crypto.randomUUID(),
  name: "",
  category: "instrumento",
  type: "",
  quantity: 1,
  location: "",
  status: "bueno",
  assignedTo: "",
  notes: "",
  repairHistory: [],
  createdAt: new Date().toISOString(),
});

export default function SchoolInventory() {
  const [items, setItems] = useState(null);
  const [error, setError] = useState(null);
  const [coordinator, setCoordinator] = useState("");
  const [askingName, setAskingName] = useState(false);
  const [nameDraft, setNameDraft] = useState("");

  const [search, setSearch] = useState("");
  const [catFilter, setCatFilter] = useState("todos");
  const [statusFilter, setStatusFilter] = useState("todos");

  const [selected, setSelected] = useState(null);
  const [editing, setEditing] = useState(null);
  const [repairDraft, setRepairDraft] = useState("");
  const [confirmDelete, setConfirmDelete] = useState(null);

  useEffect(() => {
    (async () => {
      try {
        const res = await window.storage.get("inventory-items", true);
        setItems(res ? JSON.parse(res.value) : []);
      } catch {
        setItems([]);
      }
      try {
        const name = await window.storage.get("coordinator-name", false);
        if (name) setCoordinator(name.value);
        else setAskingName(true);
      } catch {
        setAskingName(true);
      }
    })();
  }, []);

  async function persist(next) {
    setItems(next);
    try {
      const res = await window.storage.set("inventory-items", JSON.stringify(next), true);
      if (!res) setError("No se pudo guardar. Intenta de nuevo.");
      else setError(null);
    } catch {
      setError("No se pudo guardar. Intenta de nuevo.");
    }
  }

  async function saveName() {
    const n = nameDraft.trim();
    if (!n) return;
    setCoordinator(n);
    setAskingName(false);
    try {
      await window.storage.set("coordinator-name", n, false);
    } catch {}
  }

  function openNew() {
    setEditing(emptyItem());
    setSelected(null);
  }

  function openEdit(item) {
    setEditing({ ...item });
  }

  async function saveItem(e) {
    e.preventDefault();
    if (validateItem(editing).length) return;
    await persist(upsertItem(items, editing));
    setSelected(editing);
    setEditing(null);
  }

  async function deleteItem(id) {
    await persist(removeItem(items, id));
    setConfirmDelete(null);
    setSelected(null);
  }

  async function addRepair() {
    if (!repairDraft.trim() || !selected) return;
    const updated = addRepairEntry(selected, repairDraft, coordinator);
    await persist(upsertItem(items, updated));
    setSelected(updated);
    setRepairDraft("");
  }

  if (items === null) {
    return (
      <div className="w-full p-10 text-center text-stone-500" style={{ fontFamily: "Georgia, serif" }}>
        Cargando inventario…
      </div>
    );
  }

  const filtered = filterItems(items, { category: catFilter, status: statusFilter, search });
  const stats = computeStats(items);

  return (
    <div className="w-full bg-stone-50 text-stone-800" style={{ fontFamily: "system-ui, sans-serif" }}>
      {/* Header */}
      <div className="bg-emerald-900 text-emerald-50 px-6 py-5">
        <div className="flex items-center justify-between flex-wrap gap-3">
          <div>
            <h1 className="text-2xl" style={{ fontFamily: "Georgia, serif" }}>Inventario de la escuela</h1>
            <p className="text-emerald-200 text-sm mt-0.5">Instrumentos y suministros · datos compartidos con todos los coordinadores</p>
          </div>
          <div className="text-sm text-emerald-200">
            {coordinator ? (
              <button onClick={() => setAskingName(true)} className="flex items-center gap-1.5 hover:text-white">
                <User size={14} /> {coordinator}
              </button>
            ) : (
              <button onClick={() => setAskingName(true)} className="underline hover:text-white">Identifícate</button>
            )}
          </div>
        </div>
      </div>

      {askingName && (
        <div className="bg-amber-50 border-b border-amber-200 px-6 py-3 flex items-center gap-3 flex-wrap">
          <span className="text-sm text-amber-900">¿Cómo te llamas? Así se registra quién hace cada cambio.</span>
          <input
            value={nameDraft}
            onChange={(e) => setNameDraft(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && saveName()}
            placeholder="Tu nombre"
            className="border border-amber-300 rounded px-2 py-1 text-sm bg-white"
          />
          <button onClick={saveName} className="bg-amber-600 text-white text-sm px-3 py-1 rounded hover:bg-amber-700">Guardar</button>
        </div>
      )}

      {error && (
        <div className="bg-rose-50 border-b border-rose-200 px-6 py-2 text-sm text-rose-700 flex items-center gap-2">
          <AlertTriangle size={14} /> {error}
        </div>
      )}

      {/* Stats */}
      <div className="px-6 py-4 grid grid-cols-2 sm:grid-cols-4 gap-3">
        <StatCard label="Artículos" value={stats.total} />
        <StatCard label="Instrumentos" value={stats.instrumentos} />
        <StatCard label="Suministros" value={stats.suministros} />
        <StatCard label="Necesitan atención" value={stats.atencion} accent={stats.atencion > 0} />
      </div>

      {/* Toolbar */}
      <div className="px-6 pb-3 flex flex-wrap items-center gap-2">
        <div className="relative flex-1 min-w-[180px]">
          <Search size={15} className="absolute left-2.5 top-1/2 -translate-y-1/2 text-stone-400" />
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Buscar por nombre, tipo o ubicación"
            className="w-full border border-stone-300 rounded-md pl-8 pr-3 py-1.5 text-sm bg-white"
          />
        </div>
        <div className="flex gap-1 bg-white border border-stone-300 rounded-md p-0.5">
          {["todos", "instrumento", "suministro"].map((c) => (
            <button
              key={c}
              onClick={() => setCatFilter(c)}
              className={`px-2.5 py-1 text-xs rounded ${catFilter === c ? "bg-emerald-800 text-white" : "text-stone-600 hover:bg-stone-100"}`}
            >
              {c === "todos" ? "Todos" : CATS[c].label + "s"}
            </button>
          ))}
        </div>
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="border border-stone-300 rounded-md text-xs px-2 py-1.5 bg-white text-stone-600"
        >
          <option value="todos">Todos los estados</option>
          {Object.entries(STATUS).map(([k, v]) => (
            <option key={k} value={k}>{v.label}</option>
          ))}
        </select>
        <button
          onClick={openNew}
          className="ml-auto flex items-center gap-1 bg-emerald-800 text-white text-sm px-3 py-1.5 rounded-md hover:bg-emerald-900"
        >
          <Plus size={15} /> Agregar artículo
        </button>
      </div>

      {/* Grid */}
      <div className="px-6 pb-8">
        {filtered.length === 0 ? (
          <div className="text-center text-stone-400 py-16 text-sm border border-dashed border-stone-300 rounded-lg bg-white">
            {items.length === 0 ? "Aún no hay artículos. Agrega el primero." : "Nada coincide con ese filtro."}
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
            {filtered.map((item) => {
              const Icon = CATS[item.category].icon;
              const st = STATUS[item.status];
              return (
                <button
                  key={item.id}
                  onClick={() => setSelected(item)}
                  className="text-left bg-white border border-stone-200 rounded-lg p-4 hover:border-emerald-700 hover:shadow-sm transition-colors"
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="flex items-center gap-2 min-w-0">
                      <Icon size={16} className="text-emerald-800 shrink-0" />
                      <span className="font-medium text-stone-800 truncate" style={{ fontFamily: "Georgia, serif" }}>{item.name}</span>
                    </div>
                    <span className={`shrink-0 text-[11px] px-1.5 py-0.5 rounded-full border ${st.chip}`}>{st.label}</span>
                  </div>
                  <div className="mt-2 text-xs text-stone-500 space-y-0.5">
                    {item.type && <div>{item.type}</div>}
                    <div>Cantidad: {item.quantity} · {item.location || "Sin ubicación"}</div>
                    {item.assignedTo && <div className="flex items-center gap-1"><User size={11} /> {item.assignedTo}</div>}
                  </div>
                </button>
              );
            })}
          </div>
        )}
      </div>

      {/* Detail panel */}
      {selected && !editing && (
        <Modal onClose={() => setSelected(null)}>
          <div className="flex items-start justify-between gap-3">
            <div>
              <div className="text-xs text-stone-400">{CATS[selected.category].label}</div>
              <h2 className="text-xl" style={{ fontFamily: "Georgia, serif" }}>{selected.name}</h2>
            </div>
            <span className={`text-xs px-2 py-1 rounded-full border ${STATUS[selected.status].chip}`}>{STATUS[selected.status].label}</span>
          </div>

          <div className="grid grid-cols-2 gap-3 mt-4 text-sm">
            <Field label="Tipo" value={selected.type || "—"} />
            <Field label="Cantidad" value={selected.quantity} />
            <Field label="Ubicación" value={selected.location || "—"} />
            <Field label="Asignado a" value={selected.assignedTo || "Sin asignar"} />
          </div>
          {selected.notes && (
            <div className="mt-3 text-sm">
              <div className="text-xs text-stone-400 mb-0.5">Notas</div>
              <p className="text-stone-700">{selected.notes}</p>
            </div>
          )}

          <div className="flex gap-2 mt-4">
            <button onClick={() => openEdit(selected)} className="flex items-center gap-1 text-sm px-3 py-1.5 rounded-md border border-stone-300 hover:bg-stone-50">
              <Pencil size={13} /> Editar
            </button>
            <button onClick={() => setConfirmDelete(selected.id)} className="flex items-center gap-1 text-sm px-3 py-1.5 rounded-md border border-rose-200 text-rose-600 hover:bg-rose-50">
              <Trash2 size={13} /> Eliminar
            </button>
          </div>

          <div className="mt-6 border-t border-stone-200 pt-4">
            <div className="flex items-center gap-1.5 text-sm font-medium text-stone-700 mb-2">
              <History size={14} /> Historial de reparaciones
            </div>
            <div className="flex gap-2 mb-3">
              <input
                value={repairDraft}
                onChange={(e) => setRepairDraft(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && addRepair()}
                placeholder="Describe la reparación o el mantenimiento"
                className="flex-1 border border-stone-300 rounded-md px-2.5 py-1.5 text-sm"
              />
              <button onClick={addRepair} className="bg-emerald-800 text-white text-sm px-3 rounded-md hover:bg-emerald-900">Agregar</button>
            </div>
            {selected.repairHistory.length === 0 ? (
              <p className="text-xs text-stone-400">Sin registros todavía.</p>
            ) : (
              <ul className="space-y-2">
                {selected.repairHistory.map((r, idx) => (
                  <li key={idx} className="text-sm bg-stone-50 border border-stone-200 rounded-md px-3 py-2">
                    <div className="text-stone-700">{r.note}</div>
                    <div className="text-[11px] text-stone-400 mt-0.5">
                      {new Date(r.date).toLocaleDateString("es-CR", { day: "numeric", month: "short", year: "numeric" })} · {r.by}
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </Modal>
      )}

      {/* Add/edit form */}
      {editing && (
        <Modal onClose={() => setEditing(null)}>
          <h2 className="text-xl mb-4" style={{ fontFamily: "Georgia, serif" }}>
            {items.some((i) => i.id === editing.id) ? "Editar artículo" : "Nuevo artículo"}
          </h2>
          <form onSubmit={saveItem} className="space-y-3">
            <TextInput label="Nombre" value={editing.name} onChange={(v) => setEditing({ ...editing, name: v })} required />
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-xs text-stone-500">Categoría</label>
                <select
                  value={editing.category}
                  onChange={(e) => setEditing({ ...editing, category: e.target.value })}
                  className="w-full border border-stone-300 rounded-md px-2.5 py-1.5 text-sm mt-1"
                >
                  {Object.entries(CATS).map(([k, v]) => (
                    <option key={k} value={k}>{v.label}</option>
                  ))}
                </select>
              </div>
              <div>
                <label className="text-xs text-stone-500">Estado</label>
                <select
                  value={editing.status}
                  onChange={(e) => setEditing({ ...editing, status: e.target.value })}
                  className="w-full border border-stone-300 rounded-md px-2.5 py-1.5 text-sm mt-1"
                >
                  {Object.entries(STATUS).map(([k, v]) => (
                    <option key={k} value={k}>{v.label}</option>
                  ))}
                </select>
              </div>
            </div>
            <TextInput label="Tipo / detalle (ej. Violín 3/4, Papel bond)" value={editing.type} onChange={(v) => setEditing({ ...editing, type: v })} />
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="text-xs text-stone-500">Cantidad</label>
                <input
                  type="number"
                  min="0"
                  value={editing.quantity}
                  onChange={(e) => setEditing({ ...editing, quantity: parseInt(e.target.value) || 0 })}
                  className="w-full border border-stone-300 rounded-md px-2.5 py-1.5 text-sm mt-1"
                />
              </div>
              <TextInput label="Ubicación" value={editing.location} onChange={(v) => setEditing({ ...editing, location: v })} />
            </div>
            <TextInput label="Asignado a (opcional)" value={editing.assignedTo} onChange={(v) => setEditing({ ...editing, assignedTo: v })} />
            <div>
              <label className="text-xs text-stone-500">Notas</label>
              <textarea
                value={editing.notes}
                onChange={(e) => setEditing({ ...editing, notes: e.target.value })}
                rows={2}
                className="w-full border border-stone-300 rounded-md px-2.5 py-1.5 text-sm mt-1"
              />
            </div>
            <div className="flex gap-2 pt-2">
              <button type="submit" className="flex items-center gap-1 bg-emerald-800 text-white text-sm px-4 py-1.5 rounded-md hover:bg-emerald-900">
                <Check size={14} /> Guardar
              </button>
              <button type="button" onClick={() => setEditing(null)} className="text-sm px-4 py-1.5 rounded-md border border-stone-300 hover:bg-stone-50">
                Cancelar
              </button>
            </div>
          </form>
        </Modal>
      )}

      {/* Confirm delete */}
      {confirmDelete && (
        <Modal onClose={() => setConfirmDelete(null)} narrow>
          <div className="flex items-center gap-2 text-rose-700 mb-2">
            <AlertTriangle size={16} />
            <span className="font-medium">Eliminar artículo</span>
          </div>
          <p className="text-sm text-stone-600 mb-4">Esta acción no se puede deshacer. ¿Seguro que quieres eliminarlo?</p>
          <div className="flex gap-2">
            <button onClick={() => deleteItem(confirmDelete)} className="bg-rose-600 text-white text-sm px-3 py-1.5 rounded-md hover:bg-rose-700">
              Sí, eliminar
            </button>
            <button onClick={() => setConfirmDelete(null)} className="text-sm px-3 py-1.5 rounded-md border border-stone-300 hover:bg-stone-50">
              Cancelar
            </button>
          </div>
        </Modal>
      )}
    </div>
  );
}

function StatCard({ label, value, accent }) {
  return (
    <div className={`rounded-lg border px-3 py-2.5 bg-white ${accent ? "border-rose-200" : "border-stone-200"}`}>
      <div className={`text-2xl ${accent ? "text-rose-600" : "text-emerald-900"}`} style={{ fontFamily: "Georgia, serif" }}>{value}</div>
      <div className="text-xs text-stone-500">{label}</div>
    </div>
  );
}

function Field({ label, value }) {
  return (
    <div>
      <div className="text-xs text-stone-400">{label}</div>
      <div className="text-stone-700">{value}</div>
    </div>
  );
}

function TextInput({ label, value, onChange, required }) {
  return (
    <div>
      <label className="text-xs text-stone-500">{label}</label>
      <input
        value={value}
        required={required}
        onChange={(e) => onChange(e.target.value)}
        className="w-full border border-stone-300 rounded-md px-2.5 py-1.5 text-sm mt-1"
      />
    </div>
  );
}

function Modal({ children, onClose, narrow }) {
  return (
    <div className="fixed inset-0 bg-stone-900/40 flex items-center justify-center p-4 z-50" onClick={onClose}>
      <div
        onClick={(e) => e.stopPropagation()}
        className={`bg-white rounded-xl p-6 w-full ${narrow ? "max-w-sm" : "max-w-lg"} max-h-[85vh] overflow-y-auto relative`}
      >
        <button onClick={onClose} className="absolute top-4 right-4 text-stone-400 hover:text-stone-600">
          <X size={18} />
        </button>
        {children}
      </div>
    </div>
  );
}
