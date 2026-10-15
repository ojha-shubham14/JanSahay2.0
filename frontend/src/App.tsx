import { useEffect, useState } from 'react'

function App() {
  const [backendStatus, setBackendStatus] = useState<'ok' | 'not reachable' | null>(null)

  useEffect(() => {
    let isMounted = true
    const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

    fetch(`${baseUrl}/health`)
      .then((res) => {
        if (!res.ok) {
          throw new Error('Health check failed')
        }
        return res.json()
      })
      .then((data: { status?: string }) => {
        if (isMounted) {
          setBackendStatus(data.status === 'ok' ? 'ok' : 'not reachable')
        }
      })
      .catch(() => {
        if (isMounted) {
          setBackendStatus('not reachable')
        }
      })

    return () => {
      isMounted = false
    }
  }, [])

  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-gray-50 text-gray-900">
      <h1 className="text-4xl font-bold mb-4">JanSahay</h1>
      {backendStatus === 'ok' && (
        <p className="text-green-600 font-semibold">Backend: ok</p>
      )}
      {backendStatus === 'not reachable' && (
        <p className="text-red-600 font-semibold">Backend: not reachable</p>
      )}
    </main>
  )
}

export default App
