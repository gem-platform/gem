<template>
  <div class="content notification column is-6 is-offset-3">
    <h1>You have been successfully logged out!</h1>
    <p>
      Looking forward to seeing you again!
    </p>
  </div>
</template>


<script>
export default {
  layout: 'portal',
  mounted() {
    this.$auth.logout();
  }
};
</script>
