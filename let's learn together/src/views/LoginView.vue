<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../store/auth'

const router = useRouter()
const { login } = useAuth()

const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function onSubmit() {
  error.value = ''
  loading.value = true
  try {
    await login(username.value, password.value)
    router.push('/')
  } catch (e) {
    error.value = e.message || 'Something went wrong.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <section class="auth-page">
    <div class="auth-card">
      <div class="auth-logo">🎓</div>
      <h1>Welcome back</h1>
      <p class="subtitle">Sign in to continue learning.</p>

      <form @submit.prevent="onSubmit">
        <label>
          Username
          <input v-model.trim="username" type="text" required placeholder="you@example.com" autocomplete="username" />
        </label>

        <label>
          Password
          <input v-model="password" type="password" required placeholder="••••••••" autocomplete="current-password" />
        </label>

        <div v-if="error" class="form-error">{{ error }}</div>

        <button class="submit-btn" type="submit" :disabled="loading">
          {{ loading ? 'Signing in…' : 'Sign in' }}
        </button>
      </form>

      <p class="switch-link">
        New here?
        <router-link to="/register">Create an account</router-link>
      </p>
    </div>
  </section>
</template>

<style scoped>
.auth-page {
  min-height: calc(100vh - 90px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  background: #f7f8fc;
}
.auth-card {
  width: 100%;
  max-width: 420px;
  background: white;
  border: 1px solid #e6e8f0;
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 18px 45px rgba(31, 36, 48, 0.08);
}
.auth-logo {
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #5b55e8;
  color: white;
  font-size: 32px;
  border-radius: 18px;
  margin-bottom: 18px;
}
.auth-card h1 {
  margin: 0 0 6px;
  color: #202433;
  font-size: 30px;
}
.subtitle {
  margin: 0 0 24px;
  color: #6c7485;
}
form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
label {
  display: flex;
  flex-direction: column;
  gap: 6px;
  font-size: 14px;
  font-weight: 600;
  color: #202433;
}
input {
  padding: 13px 15px;
  border: 1px solid #d7d9e2;
  border-radius: 12px;
  font-size: 16px;
}
input:focus {
  outline: 2px solid #5b55e8;
  border-color: transparent;
}
.form-error {
  padding: 10px 14px;
  background: #ffe9e9;
  color: #c0392b;
  border-radius: 10px;
  font-size: 14px;
}
.submit-btn {
  padding: 14px;
  border: none;
  border-radius: 12px;
  background: #5b55e8;
  color: white;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
}
.submit-btn:hover:not(:disabled) {
  background: #4d47d5;
}
.submit-btn:disabled {
  opacity: 0.7;
}
.switch-link {
  margin: 20px 0 0;
  text-align: center;
  color: #6c7485;
  font-size: 14px;
}
.switch-link a {
  color: #5b55e8;
  font-weight: 700;
}
</style>
