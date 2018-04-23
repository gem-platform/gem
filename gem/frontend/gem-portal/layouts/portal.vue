<template>
  <div>
    <Navbar/>
    <br>

    <div class="container">
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
