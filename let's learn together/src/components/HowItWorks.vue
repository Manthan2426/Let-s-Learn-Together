<script setup>
const steps = [
  {
    id: 1,
    number: '01',
    icon: '🔎',
    title: 'Pick a course',
    description:
      'Choose something you are curious about from our growing collection of courses.',
  },
  {
    id: 2,
    number: '02',
    icon: '📚',
    title: 'Learn at your pace',
    description:
      'Watch bite-sized lessons, practice with quizzes and learn whenever you want.',
  },
  {
    id: 3,
    number: '03',
    icon: '🚀',
    title: 'Grow together',
    description:
      'Connect with other learners, share your progress and keep improving together.',
  },
]
</script>

<template>
  <section class="how-it-works" id="how-it-works">
    <div class="container">

      <!-- Heading -->
      <div class="section-heading">
        <span class="section-label">HOW IT WORKS</span>

        <h2>
          Learning is better
          <span>together 🤝</span>
        </h2>

        <p>
          Getting started is simple. Pick what you want to learn,
          follow the lessons and grow with a community that supports you.
        </p>
      </div>

      <!-- Steps -->
      <div class="steps">

        <div
          v-for="(step, index) in steps"
          :key="step.id"
          class="step"
        >
          <!-- Number -->
          <div class="step-number">
            {{ step.number }}
          </div>

          <!-- Icon -->
          <div class="step-icon">
            {{ step.icon }}
          </div>

          <!-- Content -->
          <div class="step-content">
            <h3>{{ step.title }}</h3>

            <p>
              {{ step.description }}
            </p>
          </div>

          <!-- Arrow -->
          <div
            v-if="index < steps.length - 1"
            class="step-arrow"
          >
            →
          </div>
        </div>

      </div>

    </div>
  </section>
</template>

<style scoped>
.how-it-works {
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
  max-width: 760px;
  margin: 0 auto 60px;
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
  margin: 0 auto;
  max-width: 650px;
  color: #6c7485;
  font-size: 18px;
  line-height: 1.7;
}

/* Steps */

.steps {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
}

.step {
  position: relative;
  padding: 35px 30px;
  background: #f7f8fc;
  border: 1px solid #e6e8f0;
  border-radius: 25px;
  text-align: center;
  transition: 0.2s ease;
}

.step:hover {
  transform: translateY(-6px);
  box-shadow: 0 15px 35px rgba(31, 36, 48, 0.1);
}

/* Number */

.step-number {
  position: absolute;
  top: 20px;
  right: 22px;
  color: #c8c9d8;
  font-size: 15px;
  font-weight: 800;
}

/* Icon */

.step-icon {
  width: 85px;
  height: 85px;
  margin: 0 auto 25px;

  display: flex;
  align-items: center;
  justify-content: center;

  background: #eeecff;
  border-radius: 25px;

  font-size: 38px;
}

/* Content */

.step-content h3 {
  margin: 0 0 12px;
  color: #202433;
  font-size: 22px;
}

.step-content p {
  margin: 0;
  color: #6c7485;
  font-size: 16px;
  line-height: 1.7;
}

/* Arrow */

.step-arrow {
  position: absolute;
  top: 50%;
  right: -27px;
  transform: translateY(-50%);

  width: 50px;
  height: 50px;

  display: flex;
  align-items: center;
  justify-content: center;

  background: white;
  border: 1px solid #e6e8f0;
  border-radius: 50%;

  color: #5b55e8;
  font-size: 25px;
  font-weight: 700;

  z-index: 2;
}

/* Responsive */

@media (max-width: 900px) {
  .steps {
    grid-template-columns: 1fr;
  }

  .step-arrow {
    display: none;
  }
}

@media (max-width: 600px) {
  .how-it-works {
    padding: 70px 0;
  }

  .section-heading h2 {
    font-size: 36px;
  }
}
</style>