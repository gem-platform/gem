export default {
  methods: {
    validationHasError(value) {
      return value.$error ? 'is-danger' : '';
    },
    validationMessages(value) {
      // there is no errors, so return nothing
      if (!value.$error) {
        return [];
      }

      const errors = [];

      if (value.required === false) { errors.push('Value is required'); }
      if (value.minLength === false) { errors.push('Value is to short'); }
      if (value.maxLength === false) { errors.push('Value is to long'); }
      if (value.belongToStage === false) { errors.push('Does not belong to workflow'); }

      return errors;
    },
    validationTouch(value) {
      value.$touch();
      this.$emit('invalid', this.$v.$invalid);
    }
  }
};
