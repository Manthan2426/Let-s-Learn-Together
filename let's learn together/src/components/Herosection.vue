<template>
  <section class="hero-section" id="home">
    <!-- Left Content -->
    <div class="hero-content">

      <div class="hero-badge">
        🎓 500+ expert-led courses · new lessons every week
      </div>

      <h1>
        Learn anything,
        <span>together</span> — one
        lesson at a time
      </h1>

      <p class="hero-description">
        Friendly classes, bite-sized videos, fun quizzes and a community
        that cheers you on. Start from zero, or level up the skills you
        already have.
      </p>

      <div class="hero-buttons">
        <button class="primary-btn">
          Explore Courses
          <span>→</span>
        </button>

        <button class="secondary-btn">
          ▶
          <span>How it works</span>
        </button>
      </div>

      <div class="learners">
        <div class="avatars">
          <span>👨🏻</span>
          <span>👩🏻</span>
          <span>👨🏽</span>
          <span>👩🏽</span>
        </div>

        <strong>1,00,000+</strong>
        <span>learners already joined the fun</span>
      </div>

    </div>

    <!-- Right Illustration -->
    <div class="hero-visual">

      <div class="streak-card">
        <div class="streak-icon">✧</div>

        <div>
          <strong>Daily streak 🔥</strong>
          <p>12 days in a row!</p>
        </div>
      </div>

      <div class="illustration-box">

        <div class="person-head"></div>

        <div class="person-body">
          <div class="screen">
            <div class="graph"></div>
          </div>
        </div>

        <div class="desk"></div>

        <div class="book"></div>

      </div>

      <div class="quiz-card">
        <div class="quiz-icon">✓</div>

        <div>
          <strong>Quiz passed!</strong>
          <p>Great job, Riya 🎉</p>
        </div>
      </div>

      <div class="joined-card">
        <div class="joined-icon">♙</div>

        <div>
          <strong>+2,300 today</strong>
          <p>joined a live class</p>
        </div>
      </div>

    </div>
  </section>
</template>

<style scoped>
.hero {
  min-height: 720px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 50px;
  align-items: center;
  padding: 80px 5%;
  background: #f7f8ff;
  overflow: hidden;
}

/* LEFT SIDE */

.hero-content {
  max-width: 700px;
}

.hero-badge {
  display: inline-block;
  padding: 14px 22px;
  background: white;
  border-radius: 30px;
  color: #4f46e5;
  font-size: 18px;
  font-weight: 600;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.06);
  margin-bottom: 40px;
}

.hero h1 {
  margin: 0;
  color: #202433;
  font-size: clamp(48px, 5vw, 72px);
  line-height: 1.05;
  font-weight: 800;
  letter-spacing: -2px;
}

.hero h1 span {
  color: #5b55e8;
  position: relative;
}

.hero h1 span::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: -5px;
  width: 100%;
  height: 10px;
  background: #ffd978;
  border-radius: 20px;
  z-index: -1;
}

.hero-description {
  margin-top: 35px;
  max-width: 700px;
  color: #5c667a;
  font-size: 20px;
  line-height: 1.8;
}

.hero-buttons {
  display: flex;
  gap: 18px;
  margin-top: 35px;
}

.primary-btn,
.secondary-btn {
  border-radius: 40px;
  padding: 18px 30px;
  font-size: 18px;
  font-weight: 700;
  cursor: pointer;
}

.primary-btn {
  border: none;
  color: white;
  background: #5b55e8;
  box-shadow: 0 12px 30px rgba(91, 85, 232, 0.25);
}

.primary-btn span {
  margin-left: 10px;
  font-size: 24px;
}

.secondary-btn {
  color: #5b55e8;
  background: white;
  border: 3px solid #5b55e8;
}

.secondary-btn span {
  margin-left: 8px;
}

.learners {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 35px;
  color: #697386;
  font-size: 15px;
}

.learners strong {
  color: #202433;
  font-size: 18px;
}

.avatars {
  display: flex;
  margin-right: 8px;
}

.avatars span {
  width: 38px;
  height: 38px;
  margin-right: -8px;
  border: 3px solid white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #eee;
}

/* RIGHT SIDE */

.hero-visual {
  position: relative;
  min-height: 600px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.illustration-box {
  width: 90%;
  height: 500px;
  background: white;
  border-radius: 35px;
  position: relative;
  box-shadow: 0 20px 50px rgba(50, 55, 100, 0.08);
}

/* Simple illustration */

.person-head {
  position: absolute;
  top: 105px;
  left: 50%;
  transform: translateX(-50%);
  width: 75px;
  height: 75px;
  background: #ffd8ad;
  border-radius: 50%;
}

.person-body {
  position: absolute;
  top: 160px;
  left: 50%;
  transform: translateX(-50%);
  width: 180px;
  height: 145px;
  background: #5b55e8;
  border-radius: 35px 35px 20px 20px;
  padding: 22px;
}

.screen {
  width: 100%;
  height: 100%;
  background: #303047;
  border-radius: 15px;
  position: relative;
}

.graph {
  position: absolute;
  width: 80px;
  height: 35px;
  border-bottom: 6px solid white;
  border-right: 6px solid white;
  transform: rotate(-20deg);
  left: 35px;
  top: 50px;
}

.desk {
  position: absolute;
  bottom: 120px;
  left: 15%;
  width: 70%;
  height: 15px;
  background: #e5e8f5;
  border-radius: 20px;
}

.book {
  position: absolute;
  bottom: 135px;
  left: 20%;
  width: 65px;
  height: 35px;
  background: #ff6972;
  border-radius: 8px;
}

/* CARDS */

.streak-card,
.quiz-card,
.joined-card {
  position: absolute;
  display: flex;
  align-items: center;
  gap: 15px;
  background: white;
  padding: 20px;
  border-radius: 22px;
  box-shadow: 0 15px 40px rgba(40, 45, 80, 0.12);
  z-index: 2;
}

.streak-card {
  top: 20px;
  left: 0;
}

.quiz-card {
  bottom: 10px;
  left: 50px;
}

.joined-card {
  right: -20px;
  bottom: 100px;
}

.streak-icon,
.quiz-icon,
.joined-icon {
  width: 55px;
  height: 55px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 15px;
  font-size: 25px;
}

.streak-icon {
  background: #ff6972;
  color: white;
}

.quiz-icon {
  background: #ffb51b;
  color: #202433;
}

.joined-icon {
  background: #0fa9aa;
  color: white;
}

.streak-card strong,
.quiz-card strong,
.joined-card strong {
  display: block;
  color: #202433;
  font-size: 17px;
}

.streak-card p,
.quiz-card p,
.joined-card p {
  margin: 6px 0 0;
  color: #7a8293;
}

/* RESPONSIVE */

@media (max-width: 900px) {
  .hero {
    grid-template-columns: 1fr;
  }

  .hero-visual {
    min-height: 500px;
  }

  .nav-links {
    display: none;
  }
}

@media (max-width: 600px) {
  .hero {
    padding: 50px 20px;
  }

  .hero h1 {
    font-size: 45px;
  }

  .hero-buttons {
    flex-direction: column;
  }

  .illustration-box {
    width: 100%;
  }

  .joined-card {
    right: 0;
  }
}
</style>