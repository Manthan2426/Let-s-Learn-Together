// Axios instance kept for anything that prefers axios over fetch.
//
// It deliberately uses the same relative base as src/lib/api.js so requests go
// through the Vite dev proxy (see vite.config.js) instead of a hardcoded
// http://127.0.0.1:8000, which breaks the moment the app is served from
// anywhere other than the developer's own machine.
import axios from 'axios'

import { API_BASE, TOKEN_KEY } from '../lib/api'

const api = axios.create({
  baseURL: API_BASE,
})

// Attach the JWT access token, if the learner is signed in.
api.interceptors.request.use((config) => {
  let token = ''
  try {
    token = localStorage.getItem(TOKEN_KEY) || ''
  } catch {
    token = ''
  }
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default api
