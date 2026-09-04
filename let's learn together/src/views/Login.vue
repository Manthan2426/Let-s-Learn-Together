<template>
  <div class="login-page">
    <div class="login-box">

      <h1>Welcome Back 👋</h1>
      <p>Sign in to continue learning with us.</p>

      <form>
        <label>Email</label>
        <input
          type="email"
          placeholder="Enter your email"
        />

        <label>Password</label>
        <input
          type="password"
          placeholder="Enter your password"
        />

        <button type="submit">
          Sign In
        </button>
      </form>

      <p class="signup-text">
        Don't have an account?
        <a href="#">Create Account</a>
      </p>

    </div>
  </div>
</template>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: #f5f6ff;
}

.login-box {
  width: 400px;
  padding: 40px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

h1 {
  margin-bottom: 10px;
  color: #202433;
}

p {
  color: #666;
  margin-bottom: 25px;
}

form {
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 7px;
  font-weight: 600;
  color: #333;
}

input {
  padding: 13px;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
}

button {
  padding: 14px;
  border: none;
  border-radius: 8px;
  background: #5b55e8;
  color: white;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
}

button:hover {
  background: #4d47d5;
}

.signup-text {
  text-align: center;
  margin-top: 25px;
  margin-bottom: 0;
}

.signup-text a {
  color: #5b55e8;
  text-decoration: none;
  font-weight: 600;
}
</style>