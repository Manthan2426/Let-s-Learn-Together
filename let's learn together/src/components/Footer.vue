<template>
  <footer class="footer">
    <div class="footer-container">

      <!-- Brand -->
      <div class="footer-brand">
        <div class="logo">
          <span class="logo-icon">📚</span>
          <span>Let's Learn Together</span>
        </div>

        <p>
          Learn something new, build useful skills and grow together
          with a community of curious learners.
        </p>

        <div class="social-links">
          <a href="#" aria-label="Instagram">📷</a>
          <a href="#" aria-label="LinkedIn">in</a>
          <a href="#" aria-label="YouTube">▶</a>
          <a href="#" aria-label="GitHub">◉</a>
        </div>
      </div>

      <!-- Learning -->
      <div class="footer-column">
        <h3>Learning</h3>

        <a href="#courses">Courses</a>
        <a href="#courses">Popular Courses</a>
        <a href="#categories">Categories</a>
        <a href="#reviews">Reviews</a>
      </div>

      <!-- Company -->
      <div class="footer-column">
        <h3>Company</h3>

        <a href="#">About Us</a>
        <a href="#">How It Works</a>
        <a href="#">Contact</a>
        <a href="#">Careers</a>
      </div>

      <!-- Support -->
      <div class="footer-column">
        <h3>Support</h3>

        <a href="#">Help Center</a>
        <a href="#">FAQs</a>
        <a href="#">Privacy Policy</a>
        <a href="#">Terms & Conditions</a>
      </div>

    </div>

    <!-- Bottom -->
    <div class="footer-bottom">
      <p>
        © {{ currentYear }} Let's Learn Together. All rights reserved.
      </p>

      <p>
        Made with ❤️ for learners.
      </p>
    </div>
  </footer>
</template>

<script setup>
const currentYear = new Date().getFullYear()
</script>

<style scoped>
.footer {
  padding: 70px 0 0;
  background: #202433;
  color: white;
}

.footer-container {
  max-width: 1180px;
  margin: 0 auto;
  padding: 0 24px 60px;

  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr;
  gap: 50px;
}

/* Brand */

.logo {
  display: flex;
  align-items: center;
  gap: 10px;

  color: white;
  font-size: 20px;
  font-weight: 800;
}

.logo-icon {
  width: 38px;
  height: 38px;

  display: flex;
  align-items: center;
  justify-content: center;

  background: #5b55e8;
  border-radius: 11px;

  font-size: 20px;
}

.footer-brand > p {
  max-width: 350px;
  margin: 20px 0;

  color: #aeb3c2;
  font-size: 15px;
  line-height: 1.7;
}

/* Social */

.social-links {
  display: flex;
  gap: 10px;
}

.social-links a {
  width: 40px;
  height: 40px;

  display: flex;
  align-items: center;
  justify-content: center;

  color: white;
  background: #2b3040;
  border-radius: 10px;

  text-decoration: none;
  font-size: 15px;
  font-weight: 700;

  transition: 0.2s ease;
}

.social-links a:hover {
  background: #5b55e8;
  transform: translateY(-2px);
}

/* Columns */

.footer-column {
  display: flex;
  flex-direction: column;
  gap: 13px;
}

.footer-column h3 {
  margin: 0 0 8px;

  color: white;
  font-size: 16px;
}

.footer-column a {
  color: #aeb3c2;
  font-size: 14px;
  text-decoration: none;

  transition: 0.2s ease;
}

.footer-column a:hover {
  color: white;
  transform: translateX(3px);
}

/* Bottom */

.footer-bottom {
  max-width: 1180px;
  margin: 0 auto;
  padding: 22px 24px;

  display: flex;
  justify-content: space-between;
  gap: 20px;

  border-top: 1px solid #343949;

  color: #858b9d;
  font-size: 13px;
}

.footer-bottom p {
  margin: 0;
}

/* Responsive */

@media (max-width: 850px) {
  .footer-container {
    grid-template-columns: 1fr 1fr;
    gap: 40px;
  }
}

@media (max-width: 550px) {
  .footer {
    padding-top: 50px;
  }

  .footer-container {
    grid-template-columns: 1fr;
    gap: 35px;
  }

  .footer-bottom {
    flex-direction: column;
    text-align: center;
  }
}
</style>