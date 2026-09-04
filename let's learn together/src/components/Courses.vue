<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { enrollInCourse, getCourses } from '../lib/api'
import { useAuth } from '../store/auth'

const router = useRouter()
const { isAuthenticated } = useAuth()

const courses = ref([])
const loading = ref(true)
const error = ref('')
const enrollingId = ref(null)
const enrollMsg = ref('')
const enrolledMap = ref({})

async function loadCourses() {
  loading.value = true
  error.value = ''
  try {
    courses.value = await getCourses()
  } catch (e) {
    error.value = 'Courses load nahi ho paaye. Backend start hai? Check /api/courses/.'
  } finally {
    loading.value = false
  }
}

function openCourse(course) {
  router.push({ name: 'course-detail', params: { slug: course.slug } })
}

async function onEnroll(e, course) {
  e.stopPropagation()
  if (!isAuthenticated.value) {
    router.push({ name: 'login', query: { next: `/courses/${course.slug}` } })
    return
  }
  enrollingId.value = course.id
  enrollMsg.value = ''
  try {
    await enrollInCourse(course.id)
    enrolledMap.value[course.id] = true
    enrollMsg.value = `You're enrolled in "${course.title}"! 🎉`
  } catch (e) {
    if (e.message === 'AUTH_REQUIRED') {
      router.push({ name: 'login', query: { next: `/courses/${course.slug}` } })
    } else {
      enrollMsg.value = e.message
    }
  } finally {
    enrollingId.value = null
  }
}

onMounted(loadCourses)
</script>

<template>
  <section class="courses-section" id="courses">
    <div class="container">

      <!-- Section Heading -->
      <div class="section-heading">
        <div>
          <span class="section-label">LEARN SOMETHING NEW</span>

          <h2>
            Courses learners
            <span>love 💜</span>
          </h2>

          <p>
            Short, practical and fun. Pick something you're curious about
            and start learning today.
          </p>
        </div>

        <button class="view-all">
          View all courses →
        </button>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="state-msg">
        <span class="spinner"></span> Courses load ho rahe hain…
      </div>

      <!-- Error -->
      <div v-else-if="error" class="state-msg error">
        {{ error }}
        <button class="retry-btn" @click="loadCourses">Retry</button>
      </div>

      <!-- Course Cards -->
      <div v-else class="courses-grid">

        <article
          v-for="course in courses"
          :key="course.id"
          class="course-card"
          @click="openCourse(course)"
        >

          <!-- Course Image / Icon -->
          <div :class="['course-image', course.color]">
            <div class="course-icon">
              {{ course.icon }}
            </div>

            <span class="level-badge">
              {{ course.level }}
            </span>
          </div>

          <!-- Course Content -->
          <div class="course-content">

            <span class="category">
              {{ course.category }}
            </span>

            <h3>
              {{ course.title }}
            </h3>

            <div class="course-info">
              <span>📚 {{ course.lessons }}</span>
              <span>⏱️ {{ course.duration }}</span>
            </div>

            <div class="rating">
              <span class="stars">★★★★★</span>
              <strong>{{ course.rating }}</strong>
              <span>({{ course.students }})</span>
            </div>

            <div class="course-bottom">

              <div class="price">
                <strong>{{ course.price }}</strong>
                <del>{{ course.oldPrice }}</del>
              </div>

              <button class="enroll-btn" @click="onEnroll($event, course)" :disabled="enrollingId === course.id">
                <span v-if="enrollingId === course.id">Enrolling…</span>
                <span v-else-if="enrolledMap[course.id]">Enrolled ✓</span>
                <span v-else>Enroll</span>
              </button>

            </div>

          </div>

        </article>

      </div>

      <div v-if="enrollMsg" class="enroll-toast">{{ enrollMsg }}</div>
    </div>
  </section>
</template>

<style scoped>
.courses-section {
  padding: 90px 0;
  background: #ffffff;
}

.container {
  max-width: 1180px;
  margin: 0 auto;
  padding: 0 24px;
}

/* SECTION HEADING */

.section-heading {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 30px;
  margin-bottom: 45px;
}

.section-label {
  color: #5b55e8;
  font-size: 14px;
  font-weight: 800;
  letter-spacing: 1.5px;
}

.section-heading h2 {
  margin: 10px 0;
  color: #202433;
  font-size: 46px;
  line-height: 1.1;
  font-weight: 800;
}

.section-heading h2 span {
  color: #5b55e8;
}

.section-heading p {
  max-width: 620px;
  margin: 0;
  color: #6c7485;
  font-size: 18px;
  line-height: 1.7;
}

.view-all {
  padding: 14px 24px;
  background: white;
  color: #5b55e8;
  border: 2px solid #5b55e8;
  border-radius: 30px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
  white-space: nowrap;
}

.view-all:hover {
  background: #eeecff;
}

/* COURSE GRID */

.courses-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 28px;
}

/* CARD */

.course-card {
  overflow: hidden;
  background: white;
  border: 1px solid #e6e8f0;
  border-radius: 22px;
  box-shadow: 0 8px 25px rgba(31, 36, 48, 0.07);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: pointer;
}

.course-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 18px 40px rgba(31, 36, 48, 0.12);
}

/* COURSE IMAGE */

.course-image {
  height: 190px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.course-image.purple {
  background: #eeecff;
}

.course-image.orange {
  background: #fff4dd;
}

.course-image.pink {
  background: #fdeaf2;
}

.course-image.teal {
  background: #e2f7f7;
}

.course-image.green {
  background: #e3f6f0;
}

.course-image.blue {
  background: #e8f0ff;
}

/* Loading / error states */

.state-msg {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 40px;
  justify-content: center;
  color: #6c7485;
  font-size: 17px;
  background: #f7f8fc;
  border-radius: 18px;
}

.state-msg.error {
  color: #c0392b;
  background: #ffe9e9;
  flex-direction: column;
}

.spinner {
  width: 22px;
  height: 22px;
  border: 3px solid #d7d9e2;
  border-top-color: #5b55e8;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.retry-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 22px;
  background: #5b55e8;
  color: white;
  font-weight: 700;
  cursor: pointer;
}

.enroll-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.enroll-toast {
  position: fixed;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  background: #1c9c7a;
  color: white;
  padding: 14px 22px;
  border-radius: 40px;
  font-weight: 600;
  box-shadow: 0 12px 30px rgba(28, 156, 122, 0.35);
  z-index: 50;
}

.course-icon {
  width: 100px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 25px;
  font-size: 50px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
}

.level-badge {
  position: absolute;
  top: 18px;
  right: 18px;
  padding: 7px 13px;
  background: white;
  border-radius: 20px;
  color: #555e70;
  font-size: 13px;
  font-weight: 700;
}

/* CONTENT */

.course-content {
  padding: 25px;
}

.category {
  color: #5b55e8;
  font-size: 12px;
  font-weight: 800;
  letter-spacing: 1px;
}

.course-content h3 {
  min-height: 58px;
  margin: 10px 0 18px;
  color: #202433;
  font-size: 22px;
  line-height: 1.3;
}

.course-info {
  display: flex;
  gap: 18px;
  color: #747d8f;
  font-size: 14px;
}

.rating {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 15px;
  color: #747d8f;
  font-size: 14px;
}

.stars {
  color: #ffb020;
  letter-spacing: 2px;
}

.rating strong {
  color: #202433;
}

/* PRICE */

.course-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 15px;
  margin-top: 22px;
  padding-top: 20px;
  border-top: 1px solid #e6e8f0;
}

.price {
  display: flex;
  align-items: center;
  gap: 8px;
}

.price strong {
  color: #202433;
  font-size: 23px;
}

.price del {
  color: #9aa1af;
  font-size: 14px;
}

.enroll-btn {
  padding: 11px 20px;
  border: none;
  border-radius: 25px;
  background: #5b55e8;
  color: white;
  font-weight: 700;
  cursor: pointer;
}

.enroll-btn:hover {
  background: #4646cf;
}

/* RESPONSIVE */

@media (max-width: 900px) {
  .courses-grid {
    grid-template-columns: 1fr 1fr;
  }

  .section-heading {
    align-items: flex-start;
    flex-direction: column;
  }
}

@media (max-width: 600px) {
  .courses-section {
    padding: 60px 0;
  }

  .section-heading h2 {
    font-size: 36px;
  }

  .courses-grid {
    grid-template-columns: 1fr;
  }
}
</style>