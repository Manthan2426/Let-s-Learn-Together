<script setup>
const reviews = [
  {
    id: 1,
    name: 'Riya Sharma',
    role: 'JavaScript Learner',
    avatar: '👩🏻',
    rating: 5,
    review:
      'I love how simple and friendly the lessons are. The quizzes make learning JavaScript much more fun!',
  },
  {
    id: 2,
    name: 'Aman Verma',
    role: 'Design Student',
    avatar: '👨🏻',
    rating: 5,
    review:
      'The short lessons help me stay consistent. I can learn whenever I have some free time.',
  },
  {
    id: 3,
    name: 'Priya Singh',
    role: 'Science Learner',
    avatar: '👩🏽',
    rating: 5,
    review:
      'Learning with a community keeps me motivated. It feels much better than studying completely alone.',
  },
]
</script>

<template>
  <section class="reviews-section" id="reviews">
    <div class="container">

      <!-- Heading -->
      <div class="section-heading">
        <span class="section-label">WHAT LEARNERS SAY</span>

        <h2>
          Learning together,
          <span>feels better 💜</span>
        </h2>

        <p>
          Thousands of learners are building new skills every day.
          Here's what some of them have to say.
        </p>
      </div>

      <!-- Reviews -->
      <div class="reviews-grid">

        <article
          v-for="review in reviews"
          :key="review.id"
          class="review-card"
        >

          <div class="stars">
            <span
              v-for="star in review.rating"
              :key="star"
            >
              ★
            </span>
          </div>

          <p class="review-text">
            "{{ review.review }}"
          </p>

          <div class="reviewer">

            <div class="avatar">
              {{ review.avatar }}
            </div>

            <div>
              <h3>{{ review.name }}</h3>
              <p>{{ review.role }}</p>
            </div>

          </div>

        </article>

      </div>

    </div>
  </section>
</template>

<style scoped>
.reviews-section {
  padding: 100px 0;
  background: #ffffff;
}

.container {
  max-width: 1180px;
  margin: 0 auto;
  padding: 0 24px;
}

/* Heading */

.section-heading {
  max-width: 750px;
  margin: 0 auto 55px;
  text-align: center;
}

.section-label {
  color: #5b55e8;
  font-size: 14px;
  font-weight: 800;
  letter-spacing: 1.5px;
}

.section-heading h2 {
  margin: 12px 0;
  color: #202433;
  font-size: 46px;
  line-height: 1.15;
  font-weight: 800;
}

.section-heading h2 span {
  color: #5b55e8;
}

.section-heading p {
  max-width: 650px;
  margin: 0 auto;
  color: #6c7485;
  font-size: 18px;
  line-height: 1.7;
}

/* Reviews */

.reviews-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 25px;
}

.review-card {
  padding: 32px;
  background: #f7f8fc;
  border: 1px solid #e6e8f0;
  border-radius: 24px;
  transition: 0.2s ease;
}

.review-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 15px 35px rgba(31, 36, 48, 0.1);
}

/* Stars */

.stars {
  margin-bottom: 20px;
  color: #ffb020;
  font-size: 19px;
  letter-spacing: 3px;
}

/* Review */

.review-text {
  min-height: 120px;
  margin: 0 0 30px;
  color: #4f586b;
  font-size: 17px;
  line-height: 1.7;
}

/* Reviewer */

.reviewer {
  display: flex;
  align-items: center;
  gap: 14px;
  padding-top: 20px;
  border-top: 1px solid #e2e4ec;
}

.avatar {
  width: 52px;
  height: 52px;

  display: flex;
  align-items: center;
  justify-content: center;

  background: white;
  border-radius: 50%;
  border: 2px solid #e5e6ee;

  font-size: 25px;
}

.reviewer h3 {
  margin: 0 0 4px;
  color: #202433;
  font-size: 16px;
}

.reviewer p {
  margin: 0;
  color: #7a8293;
  font-size: 13px;
}

/* Responsive */

@media (max-width: 900px) {
  .reviews-grid {
    grid-template-columns: 1fr 1fr;
  }
}

@media (max-width: 600px) {
  .reviews-section {
    padding: 70px 0;
  }

  .section-heading h2 {
    font-size: 36px;
  }

  .reviews-grid {
    grid-template-columns: 1fr;
  }
}
</style>