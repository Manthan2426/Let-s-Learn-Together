<script setup>
import Navbar from './components/Navbar.vue'
import Herosection from './components/Herosection.vue'
import Courses from './components/Courses.vue'
import Categories from './components/Categories.vue'
import HowItWorks from './components/HowItWorks.vue'
import WhyUs from './components/WhyUs.vue'
import Reviews from './components/Reviews.vue'
import CTASection from './components/CTASection.vue'
import Footer from './components/Footer.vue'

</script>

<template>
  <Navbar />

  <Herosection />
  
  <Courses />
  
  <Categories />
  
  <HowItWorks />
  
  <WhyUs />
  
  <Reviews />
  
  <CTASection />

  <Footer />
  <main>
    <h1>Let's Learn Together</h1>
    <p>Learn anything, together — one lesson at a time.</p>
  </main>
</template>

<style>
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: Arial, sans-serif;
}

main {
  padding: 60px 30px;
  text-align: center;
}
</style>