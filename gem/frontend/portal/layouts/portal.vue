<template>
  <div>
    <Navbar/>

    <div class="main-section">
      <nuxt/>
    </div>
  </div>
</template>

<script>
import Navbar from '@/components/Navbar.vue';

export default {
  components: {
    Navbar
  }
};
</script>
