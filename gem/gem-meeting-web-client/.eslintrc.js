module.exports = {
  extends: ['eslint:recommended', 'plugin:vue/recommended', '@vue/airbnb'],
  rules: {
    'no-param-reassign': ['error', { props: false }],
    'no-debugger': 0,
    'comma-dangle': ['error', 'never']
  }
};
