<template>
  <section class="hero is-info is-fullheight">
    <div class="hero-body">
      <div class="container has-text-centered">
        <div class="column is-4 is-offset-4">
          <h1 class="title">
            GBC Environment For Meetings
          </h1>
          <div class="box">
            <div class="field">
              <p class="control is-expanded">
                <input v-model="name" class="input" type="text" placeholder="Name">
              </p>
            </div>
            <div class="field">
              <p class="control is-expanded">
                <input v-model="password" class="input" type="text" placeholder="Password">
              </p>
            </div>
            <div class="field">
              <p class="control is-expanded">
                <a @click="signIn" class="button is-fullwidth is-primary">Login</a>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
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
      try {
        const res = await this.$axios.post('http://localhost:5000/login', {
          name: this.name,
          password: this.password
        });
        if (res.data.success) {
          localStorage.token = res.data.token;
          this.$router.push('/meeting');
        } else {
          alert("It isn't you bro!");
        }
      } catch (e) {
        alert('Some error!');
      }
    }
  }
};
</script>

<style scoped>
html,
body {
  font-family: 'Open Sans', serif;
}
.hero.is-info {
  background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
    url('/login-bg/bg1.jpg') no-repeat center center fixed;
  -webkit-background-size: cover;
  -moz-background-size: cover;
  -o-background-size: cover;
  background-size: cover;
}
.hero .nav,
.hero.is-success .nav {
  -webkit-box-shadow: none;
  box-shadow: none;
}
.hero .subtitle {
  padding: 3rem 0;
  line-height: 1.5;
}
</style>
