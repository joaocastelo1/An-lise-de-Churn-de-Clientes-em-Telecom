'use client'

import { useState } from 'react'
import { PieChart, Pie, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts'

const churnData = [
  { name: 'Mantido', value: 3214 },
  { name: 'Churn', value: 1786 },
]

const contractData = [
  { name: 'Mensal', churn: 65.7 },
  { name: 'Anual', churn: 0 },
  { name: 'Bienal', churn: 0 },
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

const COLORS = ['#10b981', '#ef4444']

export default function Dashboard() {
  const [tab, setTab] = useState('geral')

  return (
    <main style={{ padding: '20px', fontFamily: 'system-ui', background: '#f9fafb', minHeight: '100vh' }}>
      <header style={{ background: '#111827', color: 'white', padding: '24px', borderRadius: '12px', marginBottom: '24px' }}>
        <h1 style={{ margin: 0, fontSize: '28px' }}>Telecom Churn Analysis</h1>
        <p style={{ margin: '8px 0 0', opacity: 0.8 }}>Dashboard Interativo de Análise de Churn de Clientes</p>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px', marginBottom: '24px' }}>
        <div style={{ background: '#ef4444', padding: '20px', borderRadius: '12px', color: 'white' }}>
          <div style={{ fontSize: '14px', opacity: 0.9 }}>Taxa de Churn</div>
          <div style={{ fontSize: '36px', fontWeight: 'bold' }}>35.7%</div>
        </div>
        <div style={{ background: '#3b82f6', padding: '20px', borderRadius: '12px', color: 'white' }}>
          <div style={{ fontSize: '14px', opacity: 0.9 }}>Total Clientes</div>
          <div style={{ fontSize: '36px', fontWeight: 'bold' }}>5,000</div>
        </div>
        <div style={{ background: '#f59e0b', padding: '20px', borderRadius: '12px', color: 'white' }}>
          <div style={{ fontSize: '14px', opacity: 0.9 }}>Churnados</div>
          <div style={{ fontSize: '36px', fontWeight: 'bold' }}>1,786</div>
        </div>
        <div style={{ background: '#10b981', padding: '20px', borderRadius: '12px', color: 'white' }}>
          <div style={{ fontSize: '14px', opacity: 0.9 }}>Ticket Médio</div>
          <div style={{ fontSize: '36px', fontWeight: 'bold' }}>$64</div>
        </div>
      </div>

      <nav style={{ display: 'flex', gap: '8px', marginBottom: '24px' }}>
        {['geral', 'contratos', 'internet', 'pagamento'].map(t => (
          <button key={t} onClick={() => setTab(t)} style={{ padding: '12px 24px', border: 'none', borderRadius: '8px', background: tab === t ? '#111827' : '#fff', color: tab === t ? '#fff' : '#374151', cursor: 'pointer', fontWeight: '500', boxShadow: '0 1px 2px rgba(0,0,0,0.05)' }}>
            {t.charAt(0).toUpperCase() + t.slice(1)}
          </button>
        ))}
      </nav>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
        <div style={{ background: '#fff', padding: '24px', borderRadius: '12px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <h3 style={{ marginTop: 0, marginBottom: '16px' }}>Distribuição de Churn</h3>
          <ResponsiveContainer width="100%" height={280}>
            <PieChart>
              <Pie data={churnData} cx="50%" cy="50%" innerRadius={60} outerRadius={90} paddingAngle={5} dataKey="value" label={({ name, percent }) => `${name} ${(percent * 100).toFixed(1)}%`}>
                {churnData.map((entry, index) => <Cell key={`cell-${index}`} fill={COLORS[index]} />)}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>

        {tab === 'geral' && (
          <div style={{ background: '#fff', padding: '24px', borderRadius: '12px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
            <h3 style={{ marginTop: 0 }}>Resumo Executivo</h3>
            <ul style={{ lineHeight: '2', paddingLeft: '20px' }}>
              <li>Taxa de Churn: <strong>35.7%</strong></li>
              <li>Total de Clientes: <strong>5,000</strong></li>
              <li>Clientes Perdidos: <strong>1,786</strong></li>
              <li>Receita em Risco: <strong>$96,775/ano</strong></li>
            </ul>
            <h4 style={{ marginTop: '20px' }}> Principais Fatores de Risco</h4>
            <ul style={{ lineHeight: '1.8', paddingLeft: '20px', color: '#dc2626' }}>
              <li>Contrato Mensal: 65.7% churn</li>
              <li>Electronic Check: 73.7% churn</li>
              <li>Sem Internet: 75% churn</li>
            </ul>
          </div>
        )}

        {tab === 'contratos' && (
          <div style={{ background: '#fff', padding: '24px', borderRadius: '12px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
            <h3 style={{ marginTop: 0 }}>Churn por Tipo de Contrato</h3>
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={contractData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="churn" fill="#ef4444" name="Churn %" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {tab === 'internet' && (
          <div style={{ background: '#fff', padding: '24px', borderRadius: '12px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
            <h3 style={{ marginTop: 0 }}>Churn por Internet</h3>
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={internetData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="churn" fill="#ef4444" name="Churn %" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {tab === 'pagamento' && (
          <div style={{ background: '#fff', padding: '24px', borderRadius: '12px', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
            <h3 style={{ marginTop: 0 }}>Churn por Forma de Pagamento</h3>
            <ResponsiveContainer width="100%" height={280}>
              <BarChart data={paymentData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="churn" fill="#ef4444" name="Churn %" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      <footer style={{ marginTop: '40px', textAlign: 'center', color: '#6b7280', padding: '20px' }}>
        <p>Projeto desenvolvido para demonstração de competências em Data Analytics</p>
      </footer>
    </main>
  )
}