import React from 'react';
import { Link } from 'react-router-dom';

export default function NavBar() {
  return (
    <nav>
      <ul style={{ display: 'flex', gap: 16, listStyle: 'none', margin: 0, padding: 0 }}>
        <li><Link to="/dashboard" style={{ color: '#fff' }}>Dashboard</Link></li>
        <li><Link to="/productos" style={{ color: '#fff' }}>Productos</Link></li>
        <li><Link to="/clientes" style={{ color: '#fff' }}>Clientes</Link></li>
        <li><Link to="/pedidos" style={{ color: '#fff' }}>Pedidos</Link></li>
      </ul>
    </nav>
  );
}
