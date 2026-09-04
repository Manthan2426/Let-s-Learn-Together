import { ref, computed } from 'vue'

// Lightweight reactive auth store (no Pinia needed).
const TOKEN_KEY = 'llt_access'
const REFRESH_KEY = 'llt_refresh'

const accessToken = ref(localStorage.getItem(TOKEN_KEY) || '')
const refreshToken = ref(localStorage.getItem(REFRESH_KEY) || '')
const user = ref(null)
const ready = ref(false)

function persist() {
  if (accessToken.value) localStorage.setItem(TOKEN_KEY, accessToken.value)
  else localStorage.removeItem(TOKEN_KEY)
  if (refreshToken.value) localStorage.setItem(REFRESH_KEY, refreshToken.value)
  else localStorage.removeItem(REFRESH_KEY)
}

async function request(path, options = {}) {
  const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) }
  if (accessToken.value) headers['Authorization'] = `Bearer ${accessToken.value}`
  const res = await fetch(`/api${path}`, { ...options, headers })
  return res
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
    throw new Error(Array.isArray(first) ? first[0] : (first || 'Registration failed.'))
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
  } else if (res.status === 401) {
    const refreshed = await refresh()
    if (!refreshed) return
    const res2 = await request('/auth/me/')
    if (res2.ok) user.value = await res2.json()
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
  if (accessToken.value) await fetchMe()
  ready.value = true
}

export function useAuth() {
  return {
    accessToken,
    refreshToken,
    user,
    isAuthenticated,
    login,
    register,
    logout,
    fetchMe,
    initAuth,
  }
}
