<template>
  <div class="signal"/>
</template>

<style scoped>
.signal {
  border: 5px solid white;
  border-radius: 60px;
  height: 60px;
  left: 50%;
  margin: -30px 0 0 -30px;
  opacity: 0;
  position: absolute;
  top: 50%;
  width: 60px;

  animation: pulsate .5s ease-out;
  animation-iteration-count: infinite;
}

@keyframes pulsate {
  0% {
    transform: scale(.1);
    opacity: 0.0;
  }
  50% {
    opacity: 1;
  }
  100% {
    transform: scale(1.2);
    opacity: 0;
  }
}
</style>
