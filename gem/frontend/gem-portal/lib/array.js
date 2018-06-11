export default {
  move(array, from, to) {
    array.splice(to, 0, array.splice(from, 1)[0]);
  },
  removeIndex(array, index) {
    array.splice(index, 1);
  }
};

