import React, { useState } from 'react';
import { useProductos, useCrearProducto, useActualizarProducto, useEliminarProducto } from '../hooks/useProductos';

export default function ProductosCRUD() {
  const { data: productos, isLoading } = useProductos();
  const crear = useCrearProducto();
  const actualizar = useActualizarProducto();
  const eliminar = useEliminarProducto();
  const [form, setForm] = useState({ nombre: '', sku: '', precio: 0, stockActual: 0, activo: true });
  const [editId, setEditId] = useState<number | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (editId) {
      actualizar.mutate({ id: editId, ...form });
      setEditId(null);
    } else {
      crear.mutate(form);
    }
    setForm({ nombre: '', sku: '', precio: 0, stockActual: 0, activo: true });
  };

  if (isLoading) return <p>Cargando...</p>;

  return (
    <div>
      <h3>Nuevo producto</h3>
      <form onSubmit={handleSubmit} style={{ display: 'flex', gap: 8 }}>
        <input placeholder="Nombre" value={form.nombre} onChange={e => setForm(f => ({ ...f, nombre: e.target.value }))} required />
        <input placeholder="SKU" value={form.sku} onChange={e => setForm(f => ({ ...f, sku: e.target.value }))} required />
        <input type="number" placeholder="Precio" value={form.precio} onChange={e => setForm(f => ({ ...f, precio: +e.target.value }))} required />
        <input type="number" placeholder="Stock" value={form.stockActual} onChange={e => setForm(f => ({ ...f, stockActual: +e.target.value }))} required />
        <label><input type="checkbox" checked={form.activo} onChange={e => setForm(f => ({ ...f, activo: e.target.checked }))} />Activo</label>
        <button type="submit">{editId ? 'Actualizar' : 'Crear'}</button>
      </form>
      <h3>Listado</h3>
      <table style={{ width: '100%', marginTop: 16 }}>
        <thead>
          <tr>
            <th>ID</th><th>Nombre</th><th>SKU</th><th>Precio</th><th>Stock</th><th>Activo</th><th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {productos?.map((p: any) => (
            <tr key={p.id}>
              <td>{p.id}</td><td>{p.nombre}</td><td>{p.sku}</td><td>{p.precio}</td><td>{p.stockActual}</td><td>{p.activo ? 'Sí' : 'No'}</td>
              <td>
                <button onClick={() => { setEditId(p.id); setForm(p); }}>Editar</button>
                <button onClick={() => eliminar.mutate(p.id)}>Eliminar</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
