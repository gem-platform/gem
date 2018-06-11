<template>
  <section class="hero is-info is-fullheight">
    <div class="hero-body">
      <div class="column is-4 is-offset-4">
        <!-- GEM Logo -->
        <div
          :class="{'shake':isPasswordWrong}"
          class="box">
          <div class="logo">
            <img src="gem-logo-gray.svg">
          </div>

          <!-- Error message -->
          <b-message
            v-if="error"
            type="is-danger">
            {{ error }}
          </b-message>

          <!-- Control buttons -->
          <form @submit.prevent="submit">
            <!-- Login field -->
            <b-field
              :type="nameFieldType">
              <b-autocomplete
                v-model="name"
                :data="logins"
                placeholder="Name"
                size="is-large">
                <template slot="empty">No user found</template>
              </b-autocomplete>
            </b-field>

            <!-- Password field -->
            <b-field
              :type="passwordFieldType">
              <b-input
                ref="password"
                v-model="password"
                type="password"
                placeholder="Password"
                password-reveal/>
            </b-field>

            <!-- Login button -->
            <div class="field">
              <button
                :class="{'is-loading': isBusy}"
                type="submit"
                class="button is-fullwidth is-primary">
                Login
              </button>
            </div>
          </form>
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
      passwordFieldType: '',
      isPasswordWrong: false
    };
  },
  computed: {
    isBusy() {
      return this.$store.state.auth.busy;
    },
    logins() {
      // get names only form users
      const names = this.$store.getters['dashboard/users/all']
        .map(x => x.name);

      // filter names using value specified in login field
      return names.filter(option => option
        .toString()
        .toLowerCase()
        .indexOf(this.name.toLowerCase()) >= 0);
    }
  },
  mounted() {
    this.name = localStorage.login || '';
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
        localStorage.login = this.name;
      } catch (e) {
        this.error = 'Some error occured';

        const code = e.response.status;
        if (code === 401) {
          this.isPasswordWrong = true;
          this.error = 'Wrong login/password';
        }
      }
    },
    submit() {
      this.isPasswordWrong = false;
      this.nameFieldType = !this.name ? 'is-danger' : '';
      this.passwordFieldType = !this.password ? 'is-danger' : '';

      if (!(this.name && this.password)) {
        this.error = 'Login and password required';
        return;
      }

      this.signIn();
    }
  },
  async fetch({ store }) {
    // fetch all of the users to make autocomplete
    // at login field possible
    await store.dispatch('dashboard/users/fetch');
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
.logo {
  padding: 20px;
  padding-top: 5px;
}

.shake {
  animation: shake 0.82s cubic-bezier(.36,.07,.19,.97) both;
  transform: translate3d(0, 0, 0);
  backface-visibility: hidden;
  perspective: 1000px;
}

@keyframes shake {
  10%, 90% {
    transform: translate3d(-1px, 0, 0);
  }

  20%, 80% {
    transform: translate3d(2px, 0, 0);
  }

  30%, 50%, 70% {
    transform: translate3d(-4px, 0, 0);
  }

  40%, 60% {
    transform: translate3d(4px, 0, 0);
  }
}
</style>
