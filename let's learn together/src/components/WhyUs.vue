<script setup>
const benefits = [
  {
    id: 1,
    icon: '🎯',
    title: 'Learn by doing',
    description:
      'Practice what you learn with quizzes, exercises and real-world activities.',
  },
  {
    id: 2,
    icon: '⚡',
    title: 'Bite-sized lessons',
    description:
      'Short and focused lessons help you learn without feeling overwhelmed.',
  },
  {
    id: 3,
    icon: '👥',
    title: 'Learn together',
    description:
      'Join a friendly community, share your progress and learn from others.',
  },
  {
    id: 4,
    icon: '🏆',
    title: 'Track your progress',
    description:
      'Keep an eye on your learning journey and celebrate every milestone.',
  },
]
</script>

<template>
  <section class="why-us" id="why-us">
    <div class="container">

      <!-- Left side -->
      <div class="why-content">
        <span class="section-label">WHY LEARN WITH US?</span>

        <h2>
          Learning should feel
          <span>fun, not stressful.</span>
        </h2>

        <p class="intro">
          We believe learning works best when it is simple, practical and
          social. That's why Let's Learn Together is designed around you.
        </p>

        <div class="benefits">
          <div
            v-for="benefit in benefits"
            :key="benefit.id"
            class="benefit"
          >
            <div class="benefit-icon">
              {{ benefit.icon }}
            </div>

            <div>
              <h3>{{ benefit.title }}</h3>
              <p>{{ benefit.description }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Right side -->
      <div class="why-visual">
        <div class="visual-card">

          <div class="progress-card">
            <div class="progress-top">
              <span>Your progress</span>
              <strong>78%</strong>
            </div>

            <div class="progress-bar">
              <div class="progress-fill"></div>
            </div>

            <p>You're doing great! Keep going 🚀</p>
          </div>

          <div class="achievement">
            <div class="achievement-icon">🏆</div>

            <div>
              <strong>New achievement!</strong>
              <p>7 day learning streak</p>
            </div>
          </div>

          <div class="community-card">
            <div class="community-avatars">
              <span>👨🏻</span>
              <span>👩🏻</span>
              <span>👨🏽</span>
            </div>

            <strong>12,000+</strong>
            <p>learners learning together</p>
          </div>

        </div>
      </div>

    </div>
  </section>
</template>

<style scoped>
.why-us {
  padding: 100px 0;
  background: #f7f8fc;
}

.container {
  max-width: 1180px;
  margin: 0 auto;
  padding: 0 24px;

  display: grid;
  grid-template-columns: 1fr 0.9fr;
  gap: 80px;
  align-items: center;
}

/* Left content */

.section-label {
  color: #5b55e8;
  font-size: 14px;
  font-weight: 800;
  letter-spacing: 1.5px;
}

.why-content h2 {
  margin: 12px 0 20px;
  color: #202433;
  font-size: 48px;
  line-height: 1.15;
  font-weight: 800;
}

.why-content h2 span {
  color: #5b55e8;
}

.intro {
  max-width: 620px;
  margin: 0 0 35px;
  color: #6c7485;
  font-size: 18px;
  line-height: 1.7;
}

/* Benefits */

.benefits {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 25px;
}

.benefit {
  display: flex;
  gap: 15px;
  align-items: flex-start;
}

.benefit-icon {
  width: 52px;
  height: 52px;
  flex-shrink: 0;

  display: flex;
  align-items: center;
  justify-content: center;

  background: white;
  border-radius: 16px;

  font-size: 25px;
  box-shadow: 0 7px 20px rgba(31, 36, 48, 0.07);
}

.benefit h3 {
  margin: 0 0 6px;
  color: #202433;
  font-size: 18px;
}

.benefit p {
  margin: 0;
  color: #747d8f;
  font-size: 14px;
  line-height: 1.6;
}

/* Right visual */

.why-visual {
  display: flex;
  justify-content: center;
}

.visual-card {
  position: relative;
  width: 100%;
  min-height: 500px;

  padding: 40px;

  background: #5b55e8;
  border-radius: 35px;

  overflow: hidden;
  box-shadow: 0 25px 50px rgba(91, 85, 232, 0.25);
}

.visual-card::before {
  content: "";
  position: absolute;

  width: 280px;
  height: 280px;

  top: -100px;
  right: -80px;

  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
}

.visual-card::after {
  content: "";
  position: absolute;

  width: 200px;
  height: 200px;

  bottom: -80px;
  left: -70px;

  border-radius: 50%;
  background: rgba(255, 255, 255, 0.08);
}

/* Progress */

.progress-card {
  position: absolute;
  top: 70px;
  left: 40px;
  right: 40px;

  padding: 25px;

  background: white;
  border-radius: 22px;

  z-index: 1;
}

.progress-top {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;

  color: #202433;
  font-weight: 700;
}

.progress-top strong {
  color: #5b55e8;
}

.progress-bar {
  width: 100%;
  height: 12px;

  background: #e7e8f2;
  border-radius: 20px;
  overflow: hidden;
}

.progress-fill {
  width: 78%;
  height: 100%;
  background: #5b55e8;
  border-radius: 20px;
}

.progress-card p {
  margin: 14px 0 0;
  color: #747d8f;
  font-size: 14px;
}

/* Achievement */

.achievement {
  position: absolute;
  left: 55px;
  bottom: 120px;

  display: flex;
  align-items: center;
  gap: 15px;

  padding: 18px;

  background: white;
  border-radius: 20px;

  z-index: 1;
}

.achievement-icon {
  width: 55px;
  height: 55px;

  display: flex;
  align-items: center;
  justify-content: center;

  background: #fff1c7;
  border-radius: 15px;

  font-size: 28px;
}

.achievement strong {
  display: block;
  color: #202433;
}

.achievement p {
  margin: 5px 0 0;
  color: #747d8f;
  font-size: 13px;
}

/* Community */

.community-card {
  position: absolute;
  right: 40px;
  bottom: 45px;

  padding: 18px 22px;

  background: white;
  border-radius: 20px;

  z-index: 1;
}

.community-avatars {
  display: flex;
  margin-bottom: 10px;
}

.community-avatars span {
  width: 35px;
  height: 35px;

  display: flex;
  align-items: center;
  justify-content: center;

  margin-right: -7px;

  background: #eeeeee;
  border: 2px solid white;
  border-radius: 50%;
}

.community-card strong {
  color: #202433;
  font-size: 20px;
}

.community-card p {
  margin: 4px 0 0;
  color: #747d8f;
  font-size: 13px;
}

/* Responsive */

@media (max-width: 900px) {
  .container {
    grid-template-columns: 1fr;
    gap: 50px;
  }

  .why-content h2 {
    font-size: 40px;
  }
}

@media (max-width: 650px) {
  .why-us {
    padding: 70px 0;
  }

  .benefits {
    grid-template-columns: 1fr;
  }

  .visual-card {
    min-height: 450px;
    padding: 25px;
  }

  .progress-card {
    left: 25px;
    right: 25px;
  }

  .achievement {
    left: 25px;
    bottom: 110px;
  }

  .community-card {
    right: 25px;
  }
}
</style>