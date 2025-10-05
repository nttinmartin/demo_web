import React from 'react';
import ClientesCRUD from '../components/ClientesCRUD';

export default function ClientesPage() {
  return (
    <div className="container">
      <h2>Clientes</h2>
      <ClientesCRUD />
    </div>
  );
}
