import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import CourseDetailView from '../views/CourseDetailView.vue'
import MyLearningView from '../views/MyLearningView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
  },
  {
    path: '/courses/:slug',
    name: 'course-detail',
    component: CourseDetailView,
  },
  {
    path: '/mylearning',
    name: 'my-learning',
    component: MyLearningView,
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior() {
    return { top: 0 }
  },
  routes,
})

export default router
