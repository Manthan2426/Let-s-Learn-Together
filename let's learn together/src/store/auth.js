import { ref, computed } from 'vue'

import { API_BASE, TOKEN_KEY, REFRESH_KEY } from '../lib/api'

// Lightweight reactive auth store (no Pinia needed).

function readStored(key) {
  try {
    return localStorage.getItem(key) || ''
  } catch {
    return ''
  }
}

const accessToken = ref(readStored(TOKEN_KEY))
const refreshToken = ref(readStored(REFRESH_KEY))
const user = ref(null)
const ready = ref(false)

function persist() {
  try {
    if (accessToken.value) localStorage.setItem(TOKEN_KEY, accessToken.value)
    else localStorage.removeItem(TOKEN_KEY)
    if (refreshToken.value) localStorage.setItem(REFRESH_KEY, refreshToken.value)
    else localStorage.removeItem(REFRESH_KEY)
  } catch {
    // Private browsing / storage disabled: the session still works in-memory.
  }
}

async function request(path, options = {}) {
  const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) }
  if (accessToken.value) headers['Authorization'] = `Bearer ${accessToken.value}`
  return fetch(`${API_BASE}${path}`, { ...options, headers })
}

const isAuthenticated = computed(() => Boolean(accessToken.value))

async function login(username, password) {
  const res = await request('/auth/login/', {
    method: 'POST',
    body: JSON.stringify({ username, password }),
  })
  if (!res.ok) {
    const d = await res.json().catch(() => ({}))
    throw new Error(d.detail || d.non_field_errors?.[0] || 'Invalid credentials.')
  }
  const data = await res.json()
  accessToken.value = data.access
  refreshToken.value = data.refresh
  persist()
  await fetchMe()
}

async function register(payload) {
  const res = await request('/auth/register/', {
    method: 'POST',
    body: JSON.stringify(payload),
  })
  if (!res.ok) {
    const d = await res.json().catch(() => ({}))
    const first = Object.values(d)[0]
    throw new Error(Array.isArray(first) ? first[0] : first || 'Registration failed.')
  }
  const data = await res.json()
  accessToken.value = data.access
  refreshToken.value = data.refresh
  persist()
  user.value = data.user
}

async function fetchMe() {
  if (!accessToken.value) return
  const res = await request('/auth/me/')
  if (res.ok) {
    user.value = await res.json()
    return
  }
  if (res.status !== 401) return

  const refreshed = await refresh()
  if (!refreshed) {
    // The stored tokens are dead — drop them so the UI stops pretending
    // the learner is signed in.
    logout()
    return
  }
  const retry = await request('/auth/me/')
  if (retry.ok) {
    user.value = await retry.json()
  } else {
    logout()
  }
}

async function refresh() {
  if (!refreshToken.value) return false
  const res = await request('/auth/refresh/', {
    method: 'POST',
    body: JSON.stringify({ refresh: refreshToken.value }),
  })
  if (!res.ok) return false
  const data = await res.json()
  accessToken.value = data.access
  if (data.refresh) refreshToken.value = data.refresh
  persist()
  return true
}

function logout() {
  accessToken.value = ''
  refreshToken.value = ''
  user.value = null
  persist()
}

// Restore the session once on app start.
export async function initAuth() {
  if (ready.value) return
  ready.value = true
  if (accessToken.value) await fetchMe()
}

export function useAuth() {
  return {
    accessToken,
    refreshToken,
    user,
    isAuthenticated,
    ready,
    login,
    register,
    logout,
    fetchMe,
    initAuth,
  }
}
