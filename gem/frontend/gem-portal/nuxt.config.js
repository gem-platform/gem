// const webpack = require('webpack');

module.exports = {
  /*
  ** Headers of the page
  */
  head: {
    title: 'GEM',
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
  loading: { color: '#276cda', height: '4px' },
  /*
  ** Build configuration
  */
  build: {
    vendor: ['vue-bus', 'vue-socket.io', 'lodash', 'vuelidate', 'vue-timers', 'moment', 'vue-quill-editor'],
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

      config.resolve.alias['@fortawesome/fontawesome-free-solid$'] = '@fortawesome/fontawesome-free-solid/shakable.es.js';
    }
  },
  plugins: [
    'plugins/vue-bus', 'plugins/vue-socketio', 'plugins/vue-validate',
    { src: 'plugins/vue-timers.js', ssr: false },
    { src: '~plugins/vue-quill.js', ssr: false }
  ],
  modules: [
    'nuxt-buefy', '@nuxtjs/axios', '@nuxtjs/auth', 'nuxt-fontawesome'
  ],
  router: {
    middleware: ['auth']
  },
  auth: {
    redirect: {
      home: false
    }
  },
  css: [
    '~/assets/main.css',
    'quill/dist/quill.snow.css',
    'quill/dist/quill.core.css'
  ],
  axios: {
    browserBaseURL: '/'
  },
  buefy: {
    defaultIconPack: 'fa'
  },
  fontawesome: {
    component: 'fa',
    imports: [
      { set: '@fortawesome/fontawesome-free-solid' }
    ]
  }
};
