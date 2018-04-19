// const webpack = require('webpack');

module.exports = {
  /*
  ** Headers of the page
  */
  head: {
    title: 'gem',
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: 'GEM Platform' }
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }]
  },
  /*
  ** Customize the progress bar color
  */
  loading: { color: 'whitesmoke', height: '4px' },
  /*
  ** Build configuration
  */
  build: {
    vendor: ['vue-bus', 'vue-socket.io', 'lodash', 'vue-multiselect'],
    /*
    ** Run ESLint on save
    */
    extend(config, { isDev, isClient }) {
      if (isDev && isClient) {
        config.module.rules.push({
          enforce: 'pre',
          test: /\.(js|vue)$/,
          loader: 'eslint-loader',
          exclude: /(node_modules)/
        });
      }
    }
  },
  plugins: ['plugins/vue-bus', 'plugins/vue-socketio', 'plugins/vue-multiselect'],
  modules: ['nuxt-buefy', '@nuxtjs/axios', '@nuxtjs/auth'],
  router: {
    middleware: ['auth']
  },
  auth: {
    redirect: {
      home: false
    }
  },
  css: ['~/assets/main.css'],
  axios: {
    browserBaseURL: '/'
  }
};
