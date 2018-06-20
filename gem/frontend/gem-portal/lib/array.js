export default {
  move(array, from, to) {
    array.splice(to, 0, array.splice(from, 1)[0]);
  },
  removeIndex(array, index) {
    array.splice(index, 1);
  },
  unkey(array, idx) {
    return Object
      .entries(array)
      .map(r => Object.assign({ [idx]: r[0] }, r[1]));
  }
};

