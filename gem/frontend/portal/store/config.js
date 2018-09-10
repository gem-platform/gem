function getRandomInt(min, max) {
  return Math.floor(Math.random() * ((max - min) + 1)) + min;
}

export const state = () => ({
  backgroundId: getRandomInt(1, 4)
});

export const mutations = {
};
