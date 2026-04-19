'use client'

import { useState } from 'react'
import { PieChart, Pie, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts'

const data = [
  { name: 'Mantido', value: 3214 },
  { name: 'Churn', value: 1786 },
]

const contractData = [
  { name: 'Mensal', churn: 65.7, retained: 34.3 },
  { name: 'Anual', churn: 0, retained: 100 },
  { name: 'Bienal', churn: 0, retained: 100 },
]

const internetData = [
  { name: 'Sem Internet', churn: 75 },
  { name: 'Fiber', churn: 40 },
  { name: 'DSL', churn: 26.7 },
]

const paymentData = [
  { name: 'Electronic Check', churn: 73.7 },
  { name: 'Mailed Check', churn: 45.5 },
  { name: 'Credit Card', churn: 20 },
  { name: 'Bank Transfer', churn: 0 },
]

const COLORS = ['#2ecc71', '#e74c3c']

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState('geral')

  const tabs = [
    { id: 'geral', label: 'Geral' },
    { id: 'contratos', label: 'Contratos' },
    { id: 'internet', label: 'Internet' },
    { id: 'pagamento', label: 'Pagamento' },
  ]

  return (
    <div style={{ padding: '20px', fontFamily: 'system-ui, sans-serif', background: '#f5f5f5', minHeight: '100vh' }}>
      <header style={{ background: '#1a1a2e', color: 'white', padding: '20px', borderRadius: '10px', marginBottom: '20px' }}>
        <h1 style={{ margin: 0, fontSize: '24px' }}>Telecom Customer Churn Analysis</h1>
        <p style={{ margin: '5px 0 0 0', opacity: 0.8 }}>Dashboard Interativo de Análise de Churn</p>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '15px', marginBottom: '20px' }}>
        <div style={{ background: '#e74c3c', padding: '20px', borderRadius: '10px', color: 'white' }}>
          <div style={{ fontSize: '14px', opacity: 0.9 }}>Taxa de Churn</div>
          <div style={{ fontSize: '32px', fontWeight: 'bold' }}>35.7%</div>
        </div>
        <div style={{ background: '#3498db', padding: '20px', borderRadius: '10px', color: 'white' }}>
          <div style={{ fontSize: '14px', opacity: 0.9 }}>Total Clientes</div>
          <div style={{ fontSize: '32px', fontWeight: 'bold' }}>5,000</div>
        </div>
        <div style={{ background: '#e67e22', padding: '20px', borderRadius: '10px', color: 'white' }}>
          <div style={{ fontSize: '14px', opacity: 0.9 }}>Churnados</div>
          <div style={{ fontSize: '32px', fontWeight: 'bold' }}>1,786</div>
        </div>
        <div style={{ background: '#2ecc71', padding: '20px', borderRadius: '10px', color: 'white' }}>
          <div style={{ fontSize: '14px', opacity: 0.9 }}>Ticket Médio</div>
          <div style={{ fontSize: '32px', fontWeight: 'bold' }}>$64</div>
        </div>
      </div>

      <nav style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
        {tabs.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            style={{
              padding: '12px 24px',
              border: 'none',
              borderRadius: '8px',
              background: activeTab === tab.id ? '#1a1a2e' : 'white',
              color: activeTab === tab.id ? 'white' : '#333',
              cursor: 'pointer',
              fontWeight: '500',
            }}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        <div style={{ background: 'white', padding: '20px', borderRadius: '10px' }}>
          <h3 style={{ marginTop: 0 }}>Distribuição de Churn</h3>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie data={data} cx="50%" cy="50%" innerRadius={60} outerRadius={80} paddingAngle={5} dataKey="value">
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {activeTab === 'geral' && (
          <div style={{ background: 'white', padding: '20px', borderRadius: '10px' }}>
            <h3 style={{ marginTop: 0 }}>Visão Geral</h3>
            <p style={{ color: '#666' }}>
              Este dashboard apresenta a análise de churn de clientes para empresa de telecomunicações.
              Os principais fatores de risco foram identificados e recomendações foram geradas.
            </p>
            <ul style={{ lineHeight: '1.8' }}>
              <li>Taxa de Churn: <strong>35.7%</strong></li>
              <li>Clientes no período: <strong>5,000</strong></li>
              <li>Receita mensal em risco: <strong>$8,064.65</strong></li>
            </ul>
          </div>
        )}

        {activeTab === 'contratos' && (
          <div style={{ background: 'white', padding: '20px', borderRadius: '10px' }}>
            <h3 style={{ marginTop: 0 }}>Churn por Tipo de Contrato</h3>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={contractData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="churn" fill="#e74c3c" name="Churn %" />
                <Bar dataKey="retained" fill="#2ecc71" name="Retido %" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {activeTab === 'internet' && (
          <div style={{ background: 'white', padding: '20px', borderRadius: '10px' }}>
            <h3 style={{ marginTop: 0 }}>Churn por Internet</h3>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={internetData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="churn" fill="#e74c3c" name="Churn %" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {activeTab === 'pagamento' && (
          <div style={{ background: 'white', padding: '20px', borderRadius: '10px' }}>
            <h3 style={{ marginTop: 0 }}>Churn por Forma de Pagamento</h3>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={paymentData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="churn" fill="#e74c3c" name="Churn %" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      <footer style={{ marginTop: '30px', textAlign: 'center', color: '#666', padding: '20px' }}>
        <p>Projeto desenvolvido para demonstração de competências em Data Analytics</p>
      </footer>
    </div>
  )
}