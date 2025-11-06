import React, { useEffect, useState } from 'react'

const apiBase = import.meta.env.VITE_API_BASE || '/api'

export default function App() {
  const [items, setItems] = useState([])
  const [title, setTitle] = useState('')

  const load = async () => {
    const r = await fetch(`${apiBase}/items`)
    const data = await r.json()
    setItems(data)
  }

  const add = async () => {
    if (!title.trim()) return
    await fetch(`${apiBase}/items`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, done: false })
    })
    setTitle('')
    await load()
  }

  const toggle = async (id, done) => {
    await fetch(`${apiBase}/items/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ done: !done })
    })
    await load()
  }

  const remove = async (id) => {
    await fetch(`${apiBase}/items/${id}`, { method: 'DELETE' })
    await load()
  }

  useEffect(() => { load() }, [])

  return (
    <div style={{ maxWidth: 600, margin: '2rem auto', fontFamily: 'system-ui, sans-serif' }}>
      <h1>Interview Starter: Items</h1>
      <div style={{ display:'flex', gap: 8, marginBottom: 16 }}>
        <input value={title} onChange={e=>setTitle(e.target.value)} placeholder="New item title" style={{ flex: 1, padding: 8 }} />
        <button onClick={add}>Add</button>
      </div>
      <ul style={{ listStyle:'none', padding: 0 }}>
        {items.map(it => (
          <li key={it.id} style={{ display:'flex', alignItems:'center', gap:12, padding:'8px 0', borderBottom:'1px solid #eee' }}>
            <input type="checkbox" checked={it.done} onChange={() => toggle(it.id, it.done)} />
            <span style={{ textDecoration: it.done ? 'line-through' : 'none' }}>{it.title}</span>
            <button onClick={()=>remove(it.id)} style={{ marginLeft:'auto' }}>Delete</button>
          </li>
        ))}
      </ul>
      <p style={{ marginTop: 32, color:'#666' }}>
        API base: <code>{apiBase}</code> — try the API docs at <a href="http://localhost:8000/docs" target="_blank" rel="noreferrer">/docs</a>.
      </p>
    </div>
  )
}
