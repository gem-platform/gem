<template>
  <div class="login">
    <h1>This is an login page</h1>
    <input v-model="name">
    <input v-model="password">
    <input
      type="submit"
      @click="signIn">
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      name: '',
      password: ''
    };
  },
  methods: {
    async signIn() {
      const res = await this.$axios.post('http://localhost:5000/login', {
        name: this.name,
        password: this.password
      });
      if (res.data.success) {
        localStorage.token = res.data.token;
      } else {
        alert("It isn't you bro!");
      }
    }
  }
};
</script>

