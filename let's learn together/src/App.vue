<script setup>
import { onMounted } from 'vue'
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'
import { initAuth } from './store/auth'

onMounted(() => {
  initAuth()
})
</script>

<template>
  <Navbar />

  <router-view />

  <Footer />
</template>

<style>
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: Arial, sans-serif;
}
</style>
