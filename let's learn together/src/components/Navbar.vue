<template>
  <nav class="navbar">
    <div class="logo">
      <div class="logo-icon">🎓</div>
      <span class="logo-text">Let's Learn</span>
      <span class="logo-highlight">Together</span>
    </div>

    <div class="nav-links">
     <a href="#home">Home</a>

     <a href="#courses">Courses</a>

     <a href="#how-it-works">How it works</a>

     <a href="#why-us">Why us</a>

     <a href="#reviews">Reviews</a>
    </div>

    <div class="nav-actions">
      <a href="#" class="sign-in">Sign in</a>
      <a href="#" class="get-started">Get Started</a>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  width: 100%;
  height: 90px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 30px;
  background: white;
  border-bottom: 1px solid #e8e8ef;
  box-sizing: border-box;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 24px;
  font-weight: 700;
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

.logo-text {
  color: #202433;
}

.logo-highlight {
  color: #5b55e8;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 42px;
}

.nav-links a {
  position: relative;
  text-decoration: none;
  color: #606576;
  font-size: 20px;
  font-weight: 600;
  padding: 10px 0;
}

.nav-links a:hover,
.nav-links a.active {
  color: #5b55e8;
}

.nav-links a.active::after {
  content: "";
  position: absolute;
  left: 0;
  right: 0;
  bottom: -5px;
  height: 4px;
  background: #5b55e8;
  border-radius: 10px;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 25px;
}

.sign-in {
  text-decoration: none;
  color: #202433;
  font-size: 20px;
  font-weight: 600;
}

.get-started {
  text-decoration: none;
  background: #5b55e8;
  color: white;
  padding: 22px 38px;
  border-radius: 40px;
  font-size: 20px;
  font-weight: 700;
  box-shadow: 0 10px 25px rgba(91, 85, 232, 0.25);
}

.get-started:hover {
  background: #4d47d5;
}
</style>