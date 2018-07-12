export default {
  escape(value) {
    // eslint-disable-next-line
    return value.replace(/[\-\[\]\/\{\}\(\)\*\+\?\.\\\^\$\|]/g, '\\$&');
  }
};
