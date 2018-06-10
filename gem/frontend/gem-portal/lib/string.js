export default {
  contains(string, match) {
    return string.toString()
      .toLowerCase()
      .indexOf(match.toLowerCase()) >= 0;
  }
};
