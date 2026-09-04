<template>
  <nav class="navbar">
    <div class="navbar-container">

      <!-- Logo -->
      <div class="logo">
        <div class="logo-icon">🎓</div>

        <div class="logo-name">
          <span class="logo-text">Let's Learn</span>
          <span class="logo-highlight">Together</span>
        </div>
      </div>

      <!-- Navigation Links -->
      <div class="nav-links">
        <a href="#home">Home</a>
        <a href="#courses">Courses</a>
        <a href="#how-it-works">How it works</a>
        <a href="#why-us">Why us</a>
        <a href="#reviews">Reviews</a>
      </div>

      <!-- Right Actions -->
      <div class="nav-actions">
        <router-link to="/login" class="sign-in">
         Sign in
        </router-link>
        <a href="#" class="get-started">Get Started</a>
      </div>

    </div>
  </nav>
</template>

<style scoped>
/* =========================
   NAVBAR
========================= */

.navbar {
  width: 100%;
  height: 90px;
  background: #ffffff;
  border-bottom: 1px solid #e8e8ef;
  box-sizing: border-box;
}

/* Main navbar container */

.navbar-container {
  width: calc(100% - 80px);
  max-width: 1400px;
  height: 100%;
  margin: 0 auto;

  display: flex;
  align-items: center;
  justify-content: space-between;

  gap: 30px;
}

/* =========================
   LOGO
========================= */

.logo {
  display: flex;
  align-items: center;
  gap: 14px;

  flex-shrink: 0;
  white-space: nowrap;
}

.logo-icon {
  width: 58px;
  height: 58px;

  display: flex;
  align-items: center;
  justify-content: center;

  background: #635bff;
  color: white;

  border-radius: 18px;

  font-size: 27px;

  box-shadow: 0 8px 20px rgba(99, 91, 255, 0.25);
}

.logo-name {
  display: flex;
  align-items: center;
  gap: 4px;

  font-size: 25px;
  font-weight: 750;
}

.logo-text {
  color: #202433;
}

.logo-highlight {
  color: #5b55e8;
}

/* =========================
   NAV LINKS
========================= */

.nav-links {
  display: flex;
  align-items: center;
  justify-content: center;

  gap: 28px;

  flex: 1;
  min-width: 0;
}

.nav-links a {
  position: relative;

  text-decoration: none;

  color: #606576;

  font-size: 17px;
  font-weight: 600;

  white-space: nowrap;

  padding: 10px 0;

  transition: color 0.2s ease;
}

.nav-links a:hover {
  color: #5b55e8;
}

/* =========================
   RIGHT ACTIONS
========================= */

.nav-actions {
  display: flex;
  align-items: center;

  gap: 18px;

  flex-shrink: 0;
}

.sign-in {
  text-decoration: none;

  color: #202433;

  font-size: 17px;
  font-weight: 600;

  white-space: nowrap;
}

.get-started {
  display: inline-flex;
  align-items: center;
  justify-content: center;

  text-decoration: none;

  background: #5b55e8;
  color: white;

  padding: 16px 28px;

  border-radius: 40px;

  font-size: 17px;
  font-weight: 700;

  white-space: nowrap;

  box-shadow: 0 10px 25px rgba(91, 85, 232, 0.25);

  transition: background 0.2s ease;
}

.get-started:hover {
  background: #4d47d5;
}

/* =========================
   TABLET
========================= */

@media (max-width: 1100px) {

  .navbar-container {
    width: calc(100% - 40px);
    gap: 18px;
  }

  .logo-name {
    font-size: 21px;
  }

  .nav-links {
    gap: 18px;
  }

  .nav-links a {
    font-size: 15px;
  }

  .nav-actions {
    gap: 12px;
  }

  .sign-in {
    font-size: 15px;
  }

  .get-started {
    padding: 14px 20px;
    font-size: 15px;
  }
}

/* =========================
   MOBILE
========================= */

@media (max-width: 850px) {

  .nav-links {
    display: none;
  }

  .navbar-container {
    width: calc(100% - 30px);
  }

  .logo-name {
    font-size: 20px;
  }

  .logo-icon {
    width: 50px;
    height: 50px;
    font-size: 23px;
  }
}

@media (max-width: 500px) {

  .logo-name {
    font-size: 17px;
  }

  .sign-in {
    display: none;
  }

  .get-started {
    padding: 12px 17px;
    font-size: 14px;
  }
}
</style>