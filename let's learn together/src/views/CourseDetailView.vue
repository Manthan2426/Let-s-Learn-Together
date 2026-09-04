<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { enrollInCourse, getCourse, getMyEnrollments } from '../lib/api'
import { useAuth } from '../store/auth'

const route = useRoute()
const router = useRouter()
const { isAuthenticated } = useAuth()

const course = ref(null)
const loading = ref(true)
const error = ref('')
const isEnrolled = ref(false)
const enrolling = ref(false)
const enrollMsg = ref('')

// How many lessons are "free to preview" for guests.
const freePreviewCount = computed(
  () => course.value?.lessons?.filter((l) => l.is_free_preview).length || 0
)

function formatPrice(value) {
  return `₹${Number(value).toLocaleString('en-IN')}`
}
const priceDisplay = computed(() =>
  course.value ? formatPrice(course.value.price) : ''
)
const oldPriceDisplay = computed(() =>
  course.value?.old_price ? formatPrice(course.value.old_price) : ''
)
const studentsDisplay = computed(() => {
  const n = Number(course.value?.students_count || 0)
  if (n >= 1000) return `${(n / 1000).toFixed(1).replace(/\.0$/, '')}k`
  return String(n)
})

function canAccess(lesson) {
  // Guests can watch free previews only; enrolled users get everything.
  return isEnrolled.value || lesson.is_free_preview
}

async function loadCourse() {
  loading.value = true
  error.value = ''
  try {
    course.value = await getCourse(route.params.slug)
    if (isAuthenticated.value) {
      const enrollees = await getMyEnrollments()
      isEnrolled.value = enrollees.some((e) => e.course?.id === course.value.id)
    }
  } catch (e) {
    error.value = 'Course load nahi ho paya. Check URL ya backend.'
  } finally {
    loading.value = false
  }
}

async function onEnroll() {
  if (!isAuthenticated.value) {
    router.push({ name: 'login', query: { next: route.fullPath } })
    return
  }
  if (isEnrolled.value) return
  enrolling.value = true
  enrollMsg.value = ''
  try {
    await enrollInCourse(course.value.id)
    isEnrolled.value = true
    enrollMsg.value = 'You are now enrolled! All lessons are unlocked. 🎉'
  } catch (e) {
    if (e.message === 'AUTH_REQUIRED') {
      router.push({ name: 'login', query: { next: route.fullPath } })
    } else {
      enrollMsg.value = e.message
    }
  } finally {
    enrolling.value = false
  }
}

function goBack() {
  router.push('/')
}

onMounted(loadCourse)
</script>

<template>
  <div class="detail-page">
    <div v-if="loading" class="state-msg">
      <span class="spinner"></span> Course load ho raha hai…
    </div>

    <div v-else-if="error" class="state-msg error">
      {{ error }}
      <button @click="goBack">← Back</button>
    </div>

    <template v-else-if="course">
      <!-- HERO -->
      <section :class="['hero', course.color]">
        <div class="hero-inner">
          <button class="back-btn" @click="goBack">← All courses</button>

          <div class="hero-body">
            <div class="hero-icon">{{ course.icon }}</div>
            <div class="hero-text">
              <span class="hero-category">{{ course.category.name }}</span>
              <h1>{{ course.title }}</h1>
              <p class="hero-desc">{{ course.description }}</p>

              <div class="hero-meta">
                <span>⭐ {{ course.rating }}</span>
                <span>👥 {{ studentsDisplay }} learners</span>
                <span>📚 {{ course.lessons_count }} lessons</span>
                <span>⏱ {{ course.duration }}</span>
                <span class="level-pill">{{ course.level }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <div class="content">
        <div class="main-col">
          <!-- WHAT YOU'LL LEARN -->
          <div class="card">
            <h2>What you'll learn</h2>
            <p class="card-desc">{{ course.description }}</p>
            <ul class="learn-list">
              <li v-for="lesson in course.lessons" :key="lesson.id">
                ✅ {{ lesson.title }}
              </li>
            </ul>
          </div>

          <!-- CURRICULUM -->
          <div class="card">
            <div class="curriculum-head">
              <h2>Course curriculum</h2>
              <span>{{ course.lessons.length }} lessons · {{ course.duration }}</span>
            </div>

            <div class="lesson-item" v-for="lesson in course.lessons" :key="lesson.id">
              <span :class="['play-icon', canAccess(lesson) ? 'open' : 'locked']">
                {{ lesson.is_free_preview ? '▶' : '🔒' }}
              </span>
              <div class="lesson-info">
                <strong>{{ lesson.title }}</strong>
                <small>
                  {{ lesson.is_free_preview ? 'Free preview' : 'Lesson' }} · {{ lesson.duration }}
                </small>
              </div>
              <span v-if="canAccess(lesson)" class="lesson-actions">
                ▶ Watch
              </span>
              <span v-else class="lesson-actions locked">
                🔒 Enrolled ke liye
              </span>
            </div>
          </div>

          <!-- REVIEWS -->
          <div class="card">
            <h2>Student reviews</h2>
            <p v-if="!course.reviews.length" class="muted">No reviews yet. Be the first!</p>

            <div class="review" v-for="review in course.reviews" :key="review.id">
              <div class="review-avatar">{{ review.user[0].toUpperCase() }}</div>
              <div class="review-body">
                <div class="review-head">
                  <strong>{{ review.user }}</strong>
                  <span class="stars">★{{ review.rating }}</span>
                </div>
                <p>{{ review.comment }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- SIDEBAR / ENROLL -->
        <aside class="sidebar">
          <div class="enroll-card">
            <div class="price-row">
              <strong class="price">{{ priceDisplay }}</strong>
              <del v-if="course.old_price">{{ oldPriceDisplay }}</del>
            </div>
            <p class="price-note">One-time payment · lifetime access</p>

            <button
              class="enroll-btn"
              @click="onEnroll"
              :disabled="enrolling || isEnrolled"
            >
              <span v-if="isEnrolled">✅ Enrolled</span>
              <span v-else-if="enrolling">Enrolling…</span>
              <span v-else>Enroll now</span>
            </button>

            <p v-if="enrollMsg" class="enroll-msg">{{ enrollMsg }}</p>

            <ul class="features">
              <li>📘 {{ course.lessons_count }} lessons</li>
              <li>⏱ {{ course.duration }} total</li>
              <li>📱 Learn on any device</li>
              <li>🏅 Certificate of completion</li>
            </ul>
          </div>
        </aside>
      </div>
    </template>
  </div>
</template>

<style scoped>
.detail-page {
  background: #f7f8fc;
  min-height: calc(100vh - 90px);
}

.state-msg {
  padding: 60px;
  text-align: center;
  color: #6c7485;
  font-size: 18px;
}
.state-msg.error {
  color: #c0392b;
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

/* HERO */
.hero {
  padding: 40px 0 60px;
}
.hero.purple { background: #eeecff; }
.hero.orange { background: #fff4dd; }
.hero.pink   { background: #fdeaf2; }
.hero.teal   { background: #e2f7f7; }
.hero.green  { background: #e3f6f0; }
.hero.blue   { background: #e8f0ff; }

.hero-inner {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 24px;
}
.back-btn {
  border: none;
  background: rgba(255, 255, 255, 0.8);
  color: #202433;
  padding: 10px 18px;
  border-radius: 30px;
  font-weight: 700;
  cursor: pointer;
}
.hero-body {
  display: flex;
  gap: 30px;
  align-items: flex-start;
  margin-top: 24px;
}
.hero-icon {
  width: 120px;
  height: 120px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 30px;
  font-size: 64px;
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
}
.hero-text { flex: 1; }
.hero-category {
  color: #5b55e8;
  font-size: 14px;
  font-weight: 800;
  letter-spacing: 1px;
}
.hero-text h1 {
  margin: 8px 0 12px;
  font-size: 40px;
  color: #202433;
  line-height: 1.15;
}
.hero-desc {
  color: #444c5c;
  font-size: 17px;
  max-width: 640px;
}
.hero-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 18px;
  margin-top: 16px;
  color: #5c6474;
  font-weight: 600;
}
.level-pill {
  background: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 13px;
}

/* CONTENT LAYOUT */
.content {
  max-width: 1100px;
  margin: -30px auto 0;
  padding: 0 24px 60px;
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 30px;
  align-items: start;
}
.card {
  background: white;
  border: 1px solid #e6e8f0;
  border-radius: 20px;
  padding: 28px;
  margin-bottom: 24px;
}
.card h2 {
  margin: 0 0 14px;
  color: #202433;
  font-size: 22px;
}
.card-desc { color: #5c6474; }

.learn-list {
  list-style: none;
  padding: 0;
  margin: 16px 0 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}
.learn-list li { color: #5c6474; font-size: 15px; }

/* CURRICULUM */
.curriculum-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
}
.curriculum-head span { color: #8b93a3; font-size: 14px; }
.lesson-item {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 0;
  border-bottom: 1px solid #eef0f5;
}
.lesson-item:last-child { border-bottom: none; }
.play-icon {
  width: 38px;
  height: 38px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  font-size: 16px;
}
.play-icon.open { background: #eeecff; color: #5b55e8; }
.play-icon.locked { background: #f1f2f6; color: #a0a6b3; }
.lesson-info { flex: 1; }
.lesson-info strong { display: block; color: #202433; }
.lesson-info small { color: #8b93a3; }
.lesson-actions { font-size: 13px; font-weight: 700; color: #5b55e8; }
.lesson-actions.locked { color: #a0a6b3; }

/* REVIEWS */
.review {
  display: flex;
  gap: 14px;
  padding: 16px 0;
  border-bottom: 1px solid #eef0f5;
}
.review:last-child { border-bottom: none; }
.review-avatar {
  width: 44px;
  height: 44px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #5b55e8;
  color: white;
  font-weight: 700;
  border-radius: 50%;
}
.review-head { display: flex; align-items: center; gap: 10px; }
.stars { color: #ffb020; font-weight: 700; }
.review-body p { margin: 4px 0 0; color: #5c6474; }
.muted { color: #8b93a3; }

/* SIDEBAR */
.sidebar {
  position: sticky;
  top: 110px;
}
.enroll-card {
  background: white;
  border: 1px solid #e6e8f0;
  border-radius: 20px;
  padding: 26px;
  box-shadow: 0 12px 30px rgba(31, 36, 48, 0.08);
}
.price-row { display: flex; align-items: baseline; gap: 10px; }
.price { font-size: 30px; color: #202433; }
.price-row del { color: #9aa1af; }
.price-note { color: #8b93a3; font-size: 13px; margin: 6px 0 18px; }
.enroll-btn {
  width: 100%;
  padding: 15px;
  border: none;
  border-radius: 14px;
  background: #5b55e8;
  color: white;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
}
.enroll-btn:hover:not(:disabled) { background: #4d47d5; }
.enroll-btn:disabled { opacity: 0.8; cursor: default; }
.enroll-msg { color: #1c9c7a; font-weight: 600; margin-top: 12px; text-align: center; }
.features {
  list-style: none;
  padding: 0;
  margin: 20px 0 0;
  border-top: 1px solid #eef0f5;
  padding-top: 18px;
}
.features li { color: #5c6474; padding: 7px 0; font-size: 15px; }

@media (max-width: 900px) {
  .content { grid-template-columns: 1fr; }
  .hero-body { flex-direction: column; }
  .learn-list { grid-template-columns: 1fr; }
}
</style>
