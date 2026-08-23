<template>
  <section class="cta-section">
    <div class="cta-container">
      <div class="cta-content">
        <span class="cta-label">START YOUR LEARNING JOURNEY</span>

        <h2>
          Ready to start
          <span>learning?</span>
        </h2>

        <p>
          Pick something you're curious about, learn at your own pace,
          and grow together with thousands of other learners.
        </p>

        <div class="cta-buttons">
          <button class="primary-btn">
            Explore Courses
            <span>→</span>
          </button>

          <button class="secondary-btn">
            Get Started
          </button>
        </div>
      </div>

      <div class="cta-decoration">
        <div class="circle circle-one"></div>
        <div class="circle circle-two"></div>
        <div class="floating-card card-one">
          📚
        </div>
        <div class="floating-card card-two">
          🚀
        </div>
        <div class="floating-card card-three">
          🎓
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.cta-section {
  padding: 100px 24px;
  background: #f7f8fc;
}

.cta-container {
  position: relative;
  max-width: 1180px;
  min-height: 420px;
  margin: 0 auto;
  padding: 70px;
  display: flex;
  align-items: center;
  overflow: hidden;
  border-radius: 35px;
  background: #5b55e8;
  box-shadow: 0 25px 50px rgba(91, 85, 232, 0.22);
}

.cta-content {
  position: relative;
  z-index: 2;
  max-width: 650px;
}

.cta-label {
  color: #dddafe;
  font-size: 13px;
  font-weight: 800;
  letter-spacing: 1.5px;
}

.cta-content h2 {
  margin: 14px 0 20px;
  color: white;
  font-size: 55px;
  line-height: 1.1;
  font-weight: 800;
}

.cta-content h2 span {
  color: #ffd978;
}

.cta-content p {
  max-width: 600px;
  margin: 0;
  color: #e6e4ff;
  font-size: 18px;
  line-height: 1.7;
}

.cta-buttons {
  display: flex;
  gap: 15px;
  margin-top: 32px;
}

.primary-btn,
.secondary-btn {
  padding: 16px 27px;
  border-radius: 35px;
  font-size: 16px;
  font-weight: 700;
  cursor: pointer;
}

.primary-btn {
  border: none;
  background: white;
  color: #5b55e8;
}

.primary-btn span {
  margin-left: 8px;
  font-size: 20px;
}

.secondary-btn {
  border: 2px solid white;
  background: transparent;
  color: white;
}

.primary-btn:hover {
  transform: translateY(-2px);
}

.secondary-btn:hover {
  background: rgba(255, 255, 255, 0.12);
}

/* Decorative shapes */

.cta-decoration {
  position: absolute;
  right: -40px;
  top: 0;
  width: 48%;
  height: 100%;
}

.circle {
  position: absolute;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.15);
}

.circle-one {
  width: 380px;
  height: 380px;
  right: -70px;
  top: 20px;
}

.circle-two {
  width: 260px;
  height: 260px;
  right: 30px;
  top: 80px;
}

.floating-card {
  position: absolute;
  width: 75px;
  height: 75px;

  display: flex;
  align-items: center;
  justify-content: center;

  background: white;
  border-radius: 22px;

  font-size: 32px;

  box-shadow: 0 15px 30px rgba(30, 25, 100, 0.2);
}

.card-one {
  right: 230px;
  top: 70px;
  transform: rotate(-10deg);
}

.card-two {
  right: 80px;
  top: 210px;
  transform: rotate(8deg);
}

.card-three {
  right: 250px;
  bottom: 55px;
  transform: rotate(7deg);
}

/* Responsive */

@media (max-width: 800px) {
  .cta-container {
    padding: 55px 35px;
  }

  .cta-content h2 {
    font-size: 42px;
  }

  .cta-decoration {
    opacity: 0.35;
    width: 70%;
  }
}

@media (max-width: 600px) {
  .cta-section {
    padding: 70px 15px;
  }

  .cta-container {
    padding: 45px 25px;
  }

  .cta-content h2 {
    font-size: 36px;
  }

  .cta-buttons {
    flex-direction: column;
  }

  .cta-buttons button {
    width: 100%;
  }

  .cta-decoration {
    display: none;
  }
}
</style>