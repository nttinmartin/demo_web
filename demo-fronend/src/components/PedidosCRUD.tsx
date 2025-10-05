import React, { useState } from 'react';
import { usePedidos, useCrearPedido, useAgregarLineaPedido, useConfirmarPedido, useCancelarPedido } from '../hooks/usePedidos';

export default function PedidosCRUD() {
  const { data: pedidos, isLoading } = usePedidos();
  const crear = useCrearPedido();
  const agregarLinea = useAgregarLineaPedido();
  const confirmar = useConfirmarPedido();
  const cancelar = useCancelarPedido();
  const [form, setForm] = useState({ clienteId: '', descuento: 0 });
  const [linea, setLinea] = useState({ productoId: '', cantidad: 1, precioUnitario: 0 });
  const [pedidoId, setPedidoId] = useState<number | null>(null);

  const handleCrear = (e: React.FormEvent) => {
    e.preventDefault();
    crear.mutate({ ...form, estado: 'BORRADOR' });
    setForm({ clienteId: '', descuento: 0 });
  };

  const handleAgregarLinea = (e: React.FormEvent) => {
    e.preventDefault();
    if (pedidoId) {
      agregarLinea.mutate({ id: pedidoId, linea });
      setLinea({ productoId: '', cantidad: 1, precioUnitario: 0 });
    }
  };

  if (isLoading) return <p>Cargando...</p>;

  return (
    <div>
      <h3>Nuevo pedido</h3>
      <form onSubmit={handleCrear} style={{ display: 'flex', gap: 8 }}>
        <input placeholder="Cliente ID" value={form.clienteId} onChange={e => setForm(f => ({ ...f, clienteId: e.target.value }))} required />
        <input type="number" placeholder="Descuento" value={form.descuento} onChange={e => setForm(f => ({ ...f, descuento: +e.target.value }))} />
        <button type="submit">Crear</button>
      </form>
      <h3>Agregar línea a pedido</h3>
      <form onSubmit={handleAgregarLinea} style={{ display: 'flex', gap: 8 }}>
        <input placeholder="Pedido ID" value={pedidoId ?? ''} onChange={e => setPedidoId(+e.target.value)} required />
        <input placeholder="Producto ID" value={linea.productoId} onChange={e => setLinea(l => ({ ...l, productoId: e.target.value }))} required />
        <input type="number" placeholder="Cantidad" value={linea.cantidad} onChange={e => setLinea(l => ({ ...l, cantidad: +e.target.value }))} required />
        <input type="number" placeholder="Precio Unitario" value={linea.precioUnitario} onChange={e => setLinea(l => ({ ...l, precioUnitario: +e.target.value }))} required />
        <button type="submit">Agregar línea</button>
      </form>
      <h3>Listado</h3>
      <table style={{ width: '100%', marginTop: 16 }}>
        <thead>
          <tr>
            <th>ID</th><th>Cliente</th><th>Estado</th><th>Total Neto</th><th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          {pedidos?.map((p: any) => (
            <tr key={p.id}>
              <td>{p.id}</td><td>{p.clienteId}</td><td>{p.estado}</td><td>{p.totalNeto}</td>
              <td>
                <button onClick={() => confirmar.mutate(p.id)}>Confirmar</button>
                <button onClick={() => cancelar.mutate(p.id)}>Cancelar</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
