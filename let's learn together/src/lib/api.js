// Tiny API client for the Let's Learn Together Django backend.
// During development Vite proxies `/api` to the Django server (see vite.config.js),
// so we always call the app-relative path.
const BASE = import.meta.env.VITE_API_BASE || '/api'

async function request(path) {
  const res = await fetch(`${BASE}${path}`)
  if (!res.ok) {
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
  return `${count} lessons`
}

// ---- API endpoints -----------------------------------------------------

export async function getCourses() {
  const data = await request('/courses/')
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
  const data = await request('/categories/')
  // Map color schemes to categories; reused palette keeps the UI colorful.
  const palette = ['purple', 'orange', 'blue', 'pink', 'green', 'teal']
  return data.map((c, i) => ({
    id: c.id,
    slug: c.slug,
    icon: c.icon,
    title: c.name,
    courses: `${c.courses_count}+ courses`,
    color: palette[i % palette.length],
  }))
}

export async function getCourse(slug) {
  return request(`/courses/${slug}/`)
}
