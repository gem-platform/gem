export default {
  methods: {
    validationHasError(value) {
      return value.$error ? 'is-danger' : '';
    },
    validationMessages(value) {
      const errors = [];

      if (value.required === false) { errors.push('Value is required'); }
      if (value.alphaNum === false) { errors.push('Value should be alphanum'); }

      return errors;
    },
    validationTouch(value) {
      value.$touch();
      this.$emit('invalid', this.$v.$invalid);
    }
  }
};
