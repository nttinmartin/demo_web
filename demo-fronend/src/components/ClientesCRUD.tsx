import React, { useState } from 'react';
import { useClientes, useCrearCliente, useActualizarCliente, useEliminarCliente } from '../hooks/useClientes';

export default function ClientesCRUD() {
  const { data: clientes, isLoading } = useClientes();
  const crear = useCrearCliente();
  const actualizar = useActualizarCliente();
  const eliminar = useEliminarCliente();
  const [form, setForm] = useState({ nombre: '', email: '', segmento: '' });
  const [editId, setEditId] = useState<number | null>(null);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (editId) {
      actualizar.mutate({ id: editId, ...form });
      setEditId(null);
    } else {
      crear.mutate(form);
    }
    setForm({ nombre: '', email: '', segmento: '' });
  };

  if (isLoading) return <p>Cargando...</p>;

  return (
    <div>
      <h3>Nuevo cliente</h3>
      <form onSubmit={handleSubmit} style={{ display: 'flex', gap: 8 }}>
        <input placeholder="Nombre" value={form.nombre} onChange={e => setForm(f => ({ ...f, nombre: e.target.value }))} required />
        <input placeholder="Email" value={form.email} onChange={e => setForm(f => ({ ...f, email: e.target.value }))} required />
        <input placeholder="Segmento" value={form.segmento} onChange={e => setForm(f => ({ ...f, segmento: e.target.value }))} required />
        <button type="submit">{editId ? 'Actualizar' : 'Crear'}</button>
      </form>
      <h3>Listado</h3>
      <table style={{ width: '100%', marginTop: 16 }}>
        <thead>
          <tr>
            <th>ID</th><th>Nombre</th><th>Email</th><th>Segmento</th><th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {clientes?.map((c: any) => (
            <tr key={c.id}>
              <td>{c.id}</td><td>{c.nombre}</td><td>{c.email}</td><td>{c.segmento}</td>
              <td>
                <button onClick={() => { setEditId(c.id); setForm(c); }}>Editar</button>
                <button onClick={() => eliminar.mutate(c.id)}>Eliminar</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
