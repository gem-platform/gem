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
              v-if="error"
              type="is-danger">
              {{ error }}
            </b-message>

            <form @submit.prevent="submit">
              <b-field
                :type="nameFieldType">
                <b-input
                  v-model="name"
                  placeholder="Name"/>
              </b-field>

              <b-field
                :type="passwordFieldType">
                <b-input
                  v-model="password"
                  type="password"
                  placeholder="Password"
                  password-reveal/>
              </b-field>

              <div class="field">
                <p class="control is-expanded">
                  <button
                    :class="{'is-loading': isBusy}"
                    type="submit"
                    class="button is-fullwidth is-primary">
                    Login
                  </button>
                </p>
              </div>
            </form>
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
      error: undefined,
      nameFieldType: '',
      passwordFieldType: ''
    };
  },
  computed: {
    isBusy() {
      return this.$store.state.auth.busy;
    }
  },
  methods: {
    async signIn() {
      try {
        const credentials = { name: this.name, password: this.password };
        await this.$auth.loginWith('local', {
          data: credentials
        });

        this.error = undefined;
        this.$router.push('/');
      } catch (e) {
        this.error = 'Some error occured';

        const code = e.response.status;
        if (code === 401) this.error = 'Wrong login/password';
      }
    },
    submit() {
      this.nameFieldType = !this.name ? 'is-danger' : '';
      this.passwordFieldType = !this.password ? 'is-danger' : '';

      if (!(this.name && this.password)) {
        this.error = 'Login and password required';
        return;
      }

      this.signIn();
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
