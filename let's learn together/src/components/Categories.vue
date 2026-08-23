<script setup>
const categories = [
  {
    id: 1,
    icon: '💻',
    title: 'Coding & Tech',
    courses: '120+ courses',
    color: 'purple',
  },
  {
    id: 2,
    icon: '📐',
    title: 'Math & Science',
    courses: '80+ courses',
    color: 'orange',
  },
  {
    id: 3,
    icon: '🌐',
    title: 'Languages',
    courses: '60+ courses',
    color: 'blue',
  },
  {
    id: 4,
    icon: '🎨',
    title: 'Art & Design',
    courses: '70+ courses',
    color: 'pink',
  },
  {
    id: 5,
    icon: '🎵',
    title: 'Music & Voice',
    courses: '45+ courses',
    color: 'green',
  },
  {
    id: 6,
    icon: '🚀',
    title: 'Life & Career',
    courses: '90+ courses',
    color: 'teal',
  },
]
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

      <div class="categories-grid">

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