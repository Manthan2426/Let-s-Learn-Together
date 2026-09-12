// Tiny API client for the Let's Learn Together Django backend.
// During development Vite proxies `/api` to the Django server (see vite.config.js),
// so we default to the app-relative path.
export const API_BASE = import.meta.env.VITE_API_BASE || '/api'
export const TOKEN_KEY = 'llt_access'
export const REFRESH_KEY = 'llt_refresh'

function readToken() {
  try {
    return localStorage.getItem(TOKEN_KEY) || ''
  } catch {
    return ''
  }
}

// DRF returns a plain array when pagination is off and {count, results}
// when it is on. Accept both so enabling pagination later can't break the UI.
function unwrap(data) {
  if (Array.isArray(data)) return data
  if (data && Array.isArray(data.results)) return data.results
  return []
}

async function request(path, options = {}) {
  const token = readToken()
  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: {
      ...(options.body ? { 'Content-Type': 'application/json' } : {}),
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {}),
    },
  })
  if (!res.ok) {
    if (res.status === 401 || res.status === 403) {
      throw new Error('AUTH_REQUIRED')
    }
    throw new Error(`API error ${res.status} on ${path}`)
  }
  return res.json()
}

// ---- Formatting helpers ------------------------------------------------

function formatPrice(value) {
  const n = Number(value)
  if (Number.isNaN(n)) return value
  return `₹${n.toLocaleString('en-IN')}`
}

function formatStudents(count) {
  const n = Number(count)
  if (Number.isNaN(n)) return count
  if (n >= 1000) return `${(n / 1000).toFixed(1).replace(/\.0$/, '')}k`
  return String(n)
}

function formatLessons(count) {
  const n = Number(count) || 0
  return `${n} ${n === 1 ? 'lesson' : 'lessons'}`
}

// ---- API endpoints -----------------------------------------------------

export async function getCourses() {
  const data = unwrap(await request('/courses/'))
  return data.map((c) => ({
    id: c.id,
    slug: c.slug,
    icon: c.icon,
    category: c.category,
    category_slug: c.category_slug,
    title: c.title,
    lessons: formatLessons(c.lessons_count),
    duration: c.duration,
    level: c.level,
    rating: Number(c.rating).toFixed(1),
    students: formatStudents(c.students_count),
    price: formatPrice(c.price),
    oldPrice: c.old_price ? formatPrice(c.old_price) : '',
    color: c.color,
  }))
}

export async function getCategories() {
  const data = unwrap(await request('/categories/'))
  // Map color schemes to categories; reused palette keeps the UI colorful.
  const palette = ['purple', 'orange', 'blue', 'pink', 'green', 'teal']
  return data.map((c, i) => ({
    id: c.id,
    slug: c.slug,
    icon: c.icon,
    title: c.name,
    courses: `${c.courses_count ?? 0} ${c.courses_count === 1 ? 'course' : 'courses'}`,
    color: palette[i % palette.length],
  }))
}

export async function getCourse(slug) {
  const course = await request(`/courses/${slug}/`)
  // Guarantee the arrays the detail view iterates over always exist.
  return {
    ...course,
    lessons: course.lessons || [],
    reviews: course.reviews || [],
  }
}

// Enrol the current user in a course (requires the JWT token attached).
export async function enrollInCourse(courseId) {
  try {
    return await request('/enrollments/', {
      method: 'POST',
      body: JSON.stringify({ course_id: courseId }),
    })
  } catch (e) {
    if (e.message === 'AUTH_REQUIRED') throw e
    throw new Error('Enrolment failed. Please try again.')
  }
}

export async function unenrollFromCourse(courseId) {
  const enrollments = await getMyEnrollments()

  const enrollment = enrollments.find(
    (e) => e.course?.id === courseId
  )

  if (!enrollment) {
    throw new Error('You are not enrolled in this course.')
  }

  const token = readToken()

  const res = await fetch(`${API_BASE}/enrollments/${enrollment.id}/`, {
    method: 'DELETE',
    headers: token
      ? { Authorization: `Bearer ${token}` }
      : {},
  })

  if (res.status === 401 || res.status === 403) {
    throw new Error('AUTH_REQUIRED')
  }

  if (!res.ok) {
    throw new Error('Could not exit the course.')
  }

  return true
}

// List the current user's enrollments.
export async function getMyEnrollments() {
  return unwrap(await request('/enrollments/'))
}

// ---- Reviews -----------------------------------------------------------

export async function getCourseReviews(courseSlug) {
  return unwrap(await request(`/reviews/?course=${encodeURIComponent(courseSlug)}`))
}

// Create or update the signed-in learner's review for a course.
// Posting twice updates the existing review rather than failing.
export async function submitReview(courseId, { rating, comment }) {
  try {
    return await request('/reviews/', {
      method: 'POST',
      body: JSON.stringify({
        course_id: courseId,
        rating,
        comment: comment || '',
      }),
    })
  } catch (e) {
    if (e.message === 'AUTH_REQUIRED') throw e
    throw new Error('Review save nahi hua. Please try again.')
  }
}

export async function deleteReview(reviewId) {
  const token = readToken()
  const res = await fetch(`${API_BASE}/reviews/${reviewId}/`, {
    method: 'DELETE',
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  })
  if (res.status === 401 || res.status === 403) throw new Error('AUTH_REQUIRED')
  if (!res.ok) throw new Error('Review delete nahi hua.')
  // 204 No Content — nothing to parse.
  return true
}
