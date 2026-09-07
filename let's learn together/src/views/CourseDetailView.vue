<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  deleteReview,
  enrollInCourse,
  getCourse,
  getMyEnrollments,
  submitReview,
} from '../lib/api'
import { useAuth } from '../store/auth'

const route = useRoute()
const router = useRouter()
const { user, isAuthenticated } = useAuth()

const course = ref(null)
const loading = ref(true)
const error = ref('')
const isEnrolled = ref(false)
const enrolling = ref(false)
const enrollMsg = ref('')

// --- Review form ---------------------------------------------------------

const reviewRating = ref(5)
const reviewComment = ref('')
const reviewSaving = ref(false)
const reviewError = ref('')
const reviewMsg = ref('')

// The signed-in learner's own review, if they already left one.
const myReview = computed(() => {
  const id = user.value?.id
  if (!id) return null
  return course.value?.reviews?.find((r) => r.user_id === id) || null
})

const otherReviews = computed(() =>
  (course.value?.reviews || []).filter((r) => r.id !== myReview.value?.id)
)

// Prefill the form when an existing review loads (or after saving one).
watch(
  myReview,
  (review) => {
    if (review) {
      reviewRating.value = review.rating
      reviewComment.value = review.comment || ''
    }
  },
  { immediate: true }
)

async function onSubmitReview() {
  reviewError.value = ''
  reviewMsg.value = ''
  reviewSaving.value = true
  try {
    await submitReview(course.value.id, {
      rating: reviewRating.value,
      comment: reviewComment.value,
    })
    await loadCourse()
    reviewMsg.value = 'Thanks! Your review is live. 🙌'
  } catch (e) {
    if (e.message === 'AUTH_REQUIRED') {
      router.push({ name: 'login', query: { next: route.fullPath } })
    } else {
      reviewError.value = e.message
    }
  } finally {
    reviewSaving.value = false
  }
}

async function onDeleteReview() {
  if (!myReview.value) return
  reviewError.value = ''
  reviewMsg.value = ''
  reviewSaving.value = true
  try {
    await deleteReview(myReview.value.id)
    reviewRating.value = 5
    reviewComment.value = ''
    await loadCourse()
    reviewMsg.value = 'Your review was removed.'
  } catch (e) {
    if (e.message === 'AUTH_REQUIRED') {
      router.push({ name: 'login', query: { next: route.fullPath } })
    } else {
      reviewError.value = e.message
    }
  } finally {
    reviewSaving.value = false
  }
}

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

function initial(name) {
  return String(name || '?').charAt(0).toUpperCase()
}

async function loadCourse() {
  loading.value = true
  error.value = ''
  try {
    course.value = await getCourse(route.params.slug)
    if (isAuthenticated.value) {
      try {
        const enrollments = await getMyEnrollments()
        isEnrolled.value = enrollments.some((e) => e.course?.id === course.value.id)
      } catch (e) {
        // Not being able to check enrollment shouldn't blank the whole page.
        console.warn('Could not load enrollments:', e)
      }
    }
  } catch (e) {
    console.error('Course API error:', e)
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
                {{ canAccess(lesson) ? '▶' : '🔒' }}
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

            <!-- Write / edit your own review -->
            <div v-if="isEnrolled" class="review-form">
              <h3>{{ myReview ? 'Your review' : 'Leave a review' }}</h3>

              <div class="star-picker" role="radiogroup" aria-label="Your rating">
                <button
                  v-for="star in 5"
                  :key="star"
                  type="button"
                  role="radio"
                  :aria-checked="reviewRating === star"
                  :aria-label="`${star} star${star === 1 ? '' : 's'}`"
                  :class="['star-btn', star <= reviewRating ? 'on' : '']"
                  @click="reviewRating = star"
                >
                  ★
                </button>
                <span class="star-count">{{ reviewRating }}/5</span>
              </div>

              <textarea
                v-model.trim="reviewComment"
                rows="3"
                maxlength="1000"
                placeholder="What did you think of this course?"
              ></textarea>

              <div v-if="reviewError" class="review-error">{{ reviewError }}</div>
              <div v-else-if="reviewMsg" class="review-ok">{{ reviewMsg }}</div>

              <div class="review-actions">
                <button
                  class="review-submit"
                  type="button"
                  :disabled="reviewSaving"
                  @click="onSubmitReview"
                >
                  <span v-if="reviewSaving">Saving…</span>
                  <span v-else>{{ myReview ? 'Update review' : 'Post review' }}</span>
                </button>

                <button
                  v-if="myReview"
                  class="review-delete"
                  type="button"
                  :disabled="reviewSaving"
                  @click="onDeleteReview"
                >
                  Delete
                </button>
              </div>
            </div>

            <p v-else-if="isAuthenticated" class="muted review-gate">
              Enroll in this course to leave a review.
            </p>

            <p v-else class="muted review-gate">
              <router-link :to="{ name: 'login', query: { next: route.fullPath } }">
                Sign in
              </router-link>
              and enroll to leave a review.
            </p>

            <!-- Your review, pinned to the top -->
            <div v-if="myReview" class="review mine" :key="myReview.id">
              <div class="review-avatar">{{ initial(myReview.user) }}</div>
              <div class="review-body">
                <div class="review-head">
                  <strong>{{ myReview.user }}</strong>
                  <span class="you-tag">You</span>
                  <span class="stars">★{{ myReview.rating }}</span>
                </div>
                <p>{{ myReview.comment }}</p>
              </div>
            </div>

            <div class="review" v-for="review in otherReviews" :key="review.id">
              <div class="review-avatar">{{ initial(review.user) }}</div>
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
.review-gate { margin: 16px 0 0; }
.review-gate a { color: #5b55e8; font-weight: 700; }

/* REVIEW FORM */
.review-form {
  margin: 18px 0 6px;
  padding: 20px;
  background: #f7f8fc;
  border: 1px solid #e6e8f0;
  border-radius: 16px;
}
.review-form h3 {
  margin: 0 0 12px;
  color: #202433;
  font-size: 17px;
}
.star-picker {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-bottom: 12px;
}
.star-btn {
  border: none;
  background: transparent;
  padding: 0 2px;
  font-size: 26px;
  line-height: 1;
  color: #d7d9e2;
  cursor: pointer;
}
.star-btn.on { color: #ffb020; }
.star-btn:hover { transform: scale(1.1); }
.star-count {
  margin-left: 8px;
  color: #8b93a3;
  font-size: 14px;
  font-weight: 600;
}
.review-form textarea {
  width: 100%;
  padding: 12px 14px;
  border: 1px solid #d7d9e2;
  border-radius: 12px;
  font-family: inherit;
  font-size: 15px;
  color: #202433;
  resize: vertical;
  box-sizing: border-box;
}
.review-form textarea:focus {
  outline: 2px solid #5b55e8;
  border-color: transparent;
}
.review-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 12px;
}
.review-submit {
  padding: 11px 22px;
  border: none;
  border-radius: 25px;
  background: #5b55e8;
  color: white;
  font-weight: 700;
  cursor: pointer;
}
.review-submit:hover:not(:disabled) { background: #4d47d5; }
.review-submit:disabled { opacity: 0.7; cursor: not-allowed; }
.review-delete {
  padding: 11px 18px;
  border: 1px solid #e6c3c3;
  border-radius: 25px;
  background: white;
  color: #c0392b;
  font-weight: 700;
  cursor: pointer;
}
.review-delete:hover:not(:disabled) { background: #ffe9e9; }
.review-delete:disabled { opacity: 0.6; cursor: not-allowed; }
.review-error {
  margin-top: 12px;
  padding: 10px 14px;
  background: #ffe9e9;
  color: #c0392b;
  border-radius: 10px;
  font-size: 14px;
}
.review-ok {
  margin-top: 12px;
  color: #1c9c7a;
  font-weight: 600;
  font-size: 14px;
}
.review.mine { background: #fbfbff; border-radius: 12px; }
.you-tag {
  padding: 2px 9px;
  background: #eeecff;
  color: #5b55e8;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 800;
  letter-spacing: 0.5px;
}

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
