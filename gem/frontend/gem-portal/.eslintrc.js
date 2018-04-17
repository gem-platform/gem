const resolve = require('path').resolve;

module.exports = {
  root: true,
  env: {
    browser: true,
    node: true
  },
  parserOptions: {
    parser: 'babel-eslint'
  },
  extends: [
    // https://github.com/vuejs/eslint-plugin-vue#priority-a-essential-error-prevention
    // consider switching to `plugin:vue/strongly-recommended` or `plugin:vue/recommended` for stricter rules.
    'eslint:recommended',
    'plugin:vue/recommended',
    '@vue/airbnb'
  ],
  // required to lint *.vue files
  plugins: ['vue'],
  // add your custom rules here
  rules: {
    'no-param-reassign': 0, // ['error', { props: false }],
    'no-debugger': 0,
    'comma-dangle': ['error', 'never'],
    'no-shadow': 0,
    'import/extensions': 0,
    'prefer-destructuring': 0,
    'no-underscore-dangle': 0,
    'consistent-return': 0,
    'vue/order-in-components': 0,
    'vue/order-in-components': 0,
    'import/prefer-default-export': 0,
    'vue/require-prop-types': 0,
    eqeqeq: 0
  },
  settings: {
    'import/resolver': {
      webpack: {
        config: {
          resolve: {
            alias: {
              '@': __dirname,
              '~': __dirname,
              static: resolve(__dirname, 'static'), // use in template with <img src="~static/nuxt.png" />
              '~static': resolve(__dirname, 'static'),
              assets: resolve(__dirname, 'assets'), // use in template with <img src="~static/nuxt.png" />
              '~assets': resolve(__dirname, 'assets'),
              '~plugins': resolve(__dirname, 'plugins'),
              '~store': resolve(__dirname, '.nuxt/store'),
              '~router': resolve(__dirname, '.nuxt/router'),
              '~pages': resolve(__dirname, 'pages'),
              '~components': resolve(__dirname, 'components')
            }
          }
        }
      }
    }
  }
};
