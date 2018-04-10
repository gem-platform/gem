<template>
  <section class="hero is-info is-fullheight">
    <div class="hero-body">
      <div class="container has-text-centered">
        <div class="column is-4 is-offset-4">
          <h1 class="title">
            GBC Environment For Meetings
          </h1>
          <div class="box">
            <b-message 
              v-if="isAccessError"
              type="is-danger">
              Wrong login/password
            </b-message>
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
                <a @click="signIn"
                  :class="{'is-loading': isLoading}"
                  class="button is-fullwidth is-primary">
                  Login
                </a>
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
      password: '',
      isAccessError: false,
      isLoading: false
    };
  },
  methods: {
    async signIn() {
      this.isLoading = true;
      try {
        const res = await this.$axios.post('/api/login', {
          name: this.name,
          password: this.password
        });

        if (res.data.success) {
          localStorage.token = res.data.token;
          this.$router.push('/meeting');
        } else {
          this.isAccessError = true;
        }
      } catch (e) {
        alert('Some error!');
      } finally {
        this.isLoading = false;
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
  background: linear-gradient(
      135deg,
      rgba(229, 58, 121, 0.5) 30%,
      rgba(254, 175, 18, 0.5) 70%
    ),
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
