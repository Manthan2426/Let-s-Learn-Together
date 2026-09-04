<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth } from '../store/auth'

const router = useRouter()
const { user, isAuthenticated, logout } = useAuth()
const menuOpen = ref(false)

function onLogout() {
  logout()
  menuOpen.value = false
  router.push('/')
}
</script>

<template>
  <nav class="navbar">
    <div class="logo">
      <div class="logo-icon">🎓</div>
      <span class="logo-text">Let's Learn</span>
      <span class="logo-highlight">Together</span>
    </div>

    <div class="nav-links">
      <a href="/#home">Home</a>
      <a href="/#courses">Courses</a>
      <a href="/#how-it-works">How it works</a>
      <a href="/#why-us">Why us</a>
      <a href="/#reviews">Reviews</a>
    </div>

    <div class="nav-actions">
      <!-- Logged out -->
      <template v-if="!isAuthenticated">
        <router-link to="/login" class="sign-in">Sign in</router-link>
        <router-link to="/register" class="get-started">Get Started</router-link>
      </template>

      <!-- Logged in -->
      <div v-else class="user-area">
        <span class="user-badge">{{ (user?.username || 'U')[0].toUpperCase() }}</span>
        <button class="user-menu-btn" @click="menuOpen = !menuOpen" @blur="menuOpen = false">
          Hey, {{ user?.username || 'learner' }} ▾
        </button>
        <div v-if="menuOpen" class="dropdown">
          <button class="dropdown-item" @click="onLogout">Sign out</button>
        </div>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  width: 100%;
  height: 90px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 30px;
  background: white;
  border-bottom: 1px solid #e8e8ef;
  box-sizing: border-box;
  position: sticky;
  top: 0;
  z-index: 20;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 24px;
  font-weight: 700;
  white-space: nowrap;
}

.logo-icon {
  width: 58px;
  height: 58px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #635bff;
  color: white;
  border-radius: 18px;
  font-size: 27px;
  box-shadow: 0 8px 20px rgba(99, 91, 255, 0.25);
}

.logo-text {
  color: #202433;
}

.logo-highlight {
  color: #5b55e8;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 42px;
}

.nav-links a {
  position: relative;
  text-decoration: none;
  color: #606576;
  font-size: 20px;
  font-weight: 600;
  padding: 10px 0;
}

.nav-links a:hover,
.nav-links a.active {
  color: #5b55e8;
}

.nav-links a.active::after {
  content: "";
  position: absolute;
  left: 0;
  right: 0;
  bottom: -5px;
  height: 4px;
  background: #5b55e8;
  border-radius: 10px;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 25px;
}

.sign-in {
  text-decoration: none;
  color: #202433;
  font-size: 20px;
  font-weight: 600;
}

.sign-in:hover {
  color: #5b55e8;
}

.get-started {
  text-decoration: none;
  background: #5b55e8;
  color: white;
  padding: 22px 38px;
  border-radius: 40px;
  font-size: 18px;
  font-weight: 700;
  box-shadow: 0 10px 25px rgba(91, 85, 232, 0.25);
}

.get-started:hover {
  background: #4d47d5;
}

/* Logged-in UI */
.user-area {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-badge {
  width: 42px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #5b55e8;
  color: white;
  font-weight: 700;
  border-radius: 50%;
  font-size: 18px;
}

.user-menu-btn {
  border: none;
  background: transparent;
  color: #202433;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
}

.dropdown {
  position: absolute;
  top: 58px;
  right: 0;
  min-width: 150px;
  background: white;
  border: 1px solid #e6e8f0;
  border-radius: 14px;
  box-shadow: 0 12px 30px rgba(31, 36, 48, 0.12);
  padding: 8px;
  z-index: 30;
}

.dropdown-item {
  width: 100%;
  text-align: left;
  padding: 12px 14px;
  border: none;
  background: transparent;
  color: #5c6474;
  font-size: 15px;
  font-weight: 600;
  border-radius: 10px;
  cursor: pointer;
}

.dropdown-item:hover {
  background: #f2f3fa;
  color: #5b55e8;
}

@media (max-width: 900px) {
  .nav-links {
    display: none;
  }
}
</style>
