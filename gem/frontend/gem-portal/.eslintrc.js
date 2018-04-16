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
    'plugin:vue/essential'
    // 'eslint:recommended',
    // 'plugin:vue/recommended',
    // '@vue/airbnb'
  ],
  // required to lint *.vue files
  plugins: ['vue'],
  // add your custom rules here
  rules: {
    'no-param-reassign': 0, // ['error', { props: false }],
    'no-debugger': 0,
    'comma-dangle': ['error', 'never']
  }
};
