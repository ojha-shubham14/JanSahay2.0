import { render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import App from './App.tsx'

describe('App', () => {
  beforeEach(() => {
    vi.stubGlobal(
      'fetch',
      vi.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve({ status: 'ok' }),
        } as Response),
      ),
    )
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('shows JanSahay', () => {
    render(<App />)
    expect(screen.getByText('JanSahay')).toBeDefined()
  })
})
