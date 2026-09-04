<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { getMyEnrollments } from '../lib/api'
import { useAuth } from '../store/auth'

const router = useRouter()
const { user, isAuthenticated } = useAuth()

const enrollments = ref([])
const loading = ref(true)
const error = ref('')

const totalCourses = computed(() => enrollments.value.length)
const completed = computed(() => enrollments.value.filter((e) => e.progress >= 1).length)

function formatProgress(p) {
  return `${Math.round((p || 0) * 100)}%`
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleDateString('en-IN', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })
}

function formatPrice(value) {
  return `₹${Number(value).toLocaleString('en-IN')}`
}

function openCourse(e) {
  router.push({ name: 'course-detail', params: { slug: e.course.slug } })
}

async function load() {
  if (!isAuthenticated.value) {
    router.replace({ name: 'login', query: { next: '/mylearning' } })
    return
  }
  loading.value = true
  error.value = ''
  try {
    enrollments.value = await getMyEnrollments()
  } catch (e) {
    error.value = 'Enrolled courses load nahi ho paaye. Check /api/enrollments/.'
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<template>
  <section class="my-learning">
    <div class="container">
      <div class="page-head">
        <div>
          <h1>My Learning</h1>
          <p>
            Welcome back{{ user?.username ? `, ${user.username}` : '' }}! 
            Continue where you left off.
          </p>
        </div>
        <div class="stats">
          <div class="stat">
            <strong>{{ totalCourses }}</strong>
            <span>Enrolled</span>
          </div>
          <div class="stat">
            <strong>{{ completed }}</strong>
            <span>Completed</span>
          </div>
        </div>
      </div>

      <div v-if="loading" class="state-msg">
        <span class="spinner"></span> Loading your courses…
      </div>

      <div v-else-if="error" class="state-msg error">
        {{ error }}
        <button @click="load">Retry</button>
      </div>

      <div v-else-if="!enrollments.length" class="empty">
        <div class="empty-icon">🎓</div>
        <h2>You haven't enrolled yet</h2>
        <p>Browse the catalog and start your first course today.</p>
        <router-link to="/" class="browse-btn">Browse courses →</router-link>
      </div>

      <div v-else class="grid">
        <article
          v-for="enroll in enrollments"
          :key="enroll.id"
          class="enroll-card"
          @click="openCourse(enroll)"
        >
          <div :class="['thumb', enroll.course.color]">
            <span class="thumb-icon">{{ enroll.course.icon }}</span>
            <span class="thumb-cat">{{ enroll.course.category }}</span>
          </div>

          <div class="body">
            <h3>{{ enroll.course.title }}</h3>
            <p class="instructor">by {{ enroll.course.instructor }}</p>

            <div class="progress-line">
              <span>{{ formatProgress(enroll.progress) }} complete</span>
              <span>⏱ {{ enroll.course.duration }}</span>
            </div>
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: formatProgress(enroll.progress) }"></div>
            </div>

            <div class="meta">
              <span>Enrolled {{ formatDate(enroll.enrolled_at) }}</span>
              <span class="continue">Continue →</span>
            </div>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>

<style scoped>
.my-learning {
  min-height: calc(100vh - 90px);
  background: #f7f8fc;
  padding: 40px 0 80px;
}
.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 24px;
}
.page-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 24px;
  margin-bottom: 34px;
}
.page-head h1 {
  margin: 0 0 6px;
  color: #202433;
  font-size: 38px;
}
.page-head p {
  margin: 0;
  color: #5c6474;
}
.stats {
  display: flex;
  gap: 16px;
}
.stat {
  background: white;
  border: 1px solid #e6e8f0;
  border-radius: 16px;
  padding: 14px 22px;
  text-align: center;
  min-width: 90px;
}
.stat strong {
  display: block;
  font-size: 26px;
  color: #5b55e8;
}
.stat span {
  color: #8b93a3;
  font-size: 13px;
}

.state-msg {
  padding: 50px;
  text-align: center;
  color: #6c7485;
  font-size: 17px;
  background: white;
  border: 1px solid #e6e8f0;
  border-radius: 18px;
}
.state-msg.error {
  color: #c0392b;
  background: #ffe9e9;
}
.spinner {
  display: inline-block;
  width: 22px;
  height: 22px;
  border: 3px solid #d7d9e2;
  border-top-color: #5b55e8;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  vertical-align: middle;
  margin-right: 10px;
}
@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.empty {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border: 1px solid #e6e8f0;
  border-radius: 20px;
}
.empty-icon {
  font-size: 64px;
  margin-bottom: 10px;
}
.empty h2 {
  color: #202433;
}
.empty p {
  color: #8b93a3;
}
.browse-btn {
  display: inline-block;
  margin-top: 16px;
  padding: 14px 26px;
  background: #5b55e8;
  color: white;
  border-radius: 30px;
  font-weight: 700;
}

.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}
.enroll-card {
  display: flex;
  background: white;
  border: 1px solid #e6e8f0;
  border-radius: 20px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}
.enroll-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 14px 30px rgba(31, 36, 48, 0.1);
}
.thumb {
  width: 130px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}
.thumb.purple { background: #eeecff; }
.thumb.orange { background: #fff4dd; }
.thumb.pink   { background: #fdeaf2; }
.thumb.teal   { background: #e2f7f7; }
.thumb.green  { background: #e3f6f0; }
.thumb.blue   { background: #e8f0ff; }
.thumb-icon {
  font-size: 48px;
}
.thumb-cat {
  position: absolute;
  bottom: 10px;
  font-size: 11px;
  font-weight: 700;
  color: #5c6474;
  letter-spacing: 0.5px;
}
.body {
  padding: 22px;
  flex: 1;
}
.body h3 {
  margin: 0 0 4px;
  color: #202433;
  font-size: 20px;
}
.instructor {
  margin: 0 0 18px;
  color: #8b93a3;
  font-size: 14px;
}
.progress-line {
  display: flex;
  justify-content: space-between;
  color: #5c6474;
  font-size: 14px;
  margin-bottom: 8px;
}
.progress-bar {
  height: 8px;
  background: #eef0f5;
  border-radius: 10px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background: #5b55e8;
  border-radius: 10px;
  transition: width 0.3s ease;
}
.meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 18px;
  color: #8b93a3;
  font-size: 13px;
}
.continue {
  color: #5b55e8;
  font-weight: 700;
}

@media (max-width: 800px) {
  .grid { grid-template-columns: 1fr; }
  .page-head { flex-direction: column; align-items: flex-start; }
}
</style>
