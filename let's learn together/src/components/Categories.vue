<script setup>
import { onMounted, ref } from 'vue'
import { getCategories } from '../lib/api'

const categories = ref([])
const loading = ref(true)
const error = ref('')

async function loadCategories() {
  loading.value = true
  error.value = ''
  try {
    categories.value = await getCategories()
  } catch (e) {
    error.value = 'Categories load nahi ho paaye. Backend start hai? Check /api/categories/.'
  } finally {
    loading.value = false
  }
}

onMounted(loadCategories)
</script>

<template>
  <section class="categories-section">
    <div class="container">

      <div class="section-heading">
        <div>
          <span class="section-label">EXPLORE BY CATEGORY</span>

          <h2>
            Find what
            <span>excites you ✨</span>
          </h2>

          <p>
            Explore our learning categories and discover something new
            to learn every day.
          </p>
        </div>
      </div>

      <div v-if="loading" class="state-msg">
        <span class="spinner"></span> Categories load ho rahe hain…
      </div>

      <div v-else-if="error" class="state-msg error">
        {{ error }}
        <button class="retry-btn" @click="loadCategories">Retry</button>
      </div>

      <div v-else class="categories-grid">

        <div
          v-for="category in categories"
          :key="category.id"
          :class="['category-card', category.color]"
        >
          <div class="category-icon">
            {{ category.icon }}
          </div>

          <div class="category-content">
            <h3>{{ category.title }}</h3>
            <p>{{ category.courses }}</p>
          </div>

          <span class="arrow">→</span>
        </div>

      </div>

    </div>
  </section>
</template>

<style scoped>
.categories-section {
  padding: 90px 0;
  background: #f7f8fc;
}

.container {
  max-width: 1180px;
  margin: 0 auto;
  padding: 0 24px;
}

.section-heading {
  margin-bottom: 40px;
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
  max-width: 650px;
  margin: 0;
  color: #6c7485;
  font-size: 18px;
  line-height: 1.7;
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 22px;
}

.category-card {
  position: relative;
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 24px;
  background: white;
  border: 1px solid #e6e8f0;
  border-radius: 20px;
  cursor: pointer;
  transition: 0.2s ease;
}

.category-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(31, 36, 48, 0.1);
}

.category-icon {
  width: 65px;
  height: 65px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 18px;
  background: white;
  font-size: 32px;
}

.category-content {
  flex: 1;
}

.category-content h3 {
  margin: 0 0 5px;
  color: #202433;
  font-size: 19px;
}

.category-content p {
  margin: 0;
  color: #7a8293;
  font-size: 14px;
}

.arrow {
  color: #5b55e8;
  font-size: 25px;
  font-weight: 700;
}

/* Category colors */

.category-card.purple {
  background: #eeecff;
}

.category-card.orange {
  background: #fff4dd;
}

.category-card.blue {
  background: #e8f0ff;
}

.category-card.pink {
  background: #fdeaf2;
}

.category-card.green {
  background: #e3f6f0;
}

.category-card.teal {
  background: #e2f7f7;
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
  background: #ffffff;
  border: 1px solid #e6e8f0;
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

/* Responsive */

@media (max-width: 900px) {
  .categories-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 600px) {
  .categories-section {
    padding: 60px 0;
  }

  .section-heading h2 {
    font-size: 36px;
  }

  .categories-grid {
    grid-template-columns: 1fr;
  }
}
</style>         