<template>
  <div class="content center">
    <div v-if="entity">
      <h1>Delete</h1>
      <p>Are you sure you want to delete?</p>
      <a 
        class="button is-danger"
        @click="remove"
        :class="{'is-loading': busy}">
        Confirm
      </a>
    </div>
    <div v-else>
      Entity doesn't exist any more.
    </div>
  </div>
</template>

<script>
import CrudComponentMixin from '@/components/CrudComponentMixin';
import BusyMixin from '@/components/BusyMixin';

export default {
  layout: 'portal',
  mixins: [CrudComponentMixin(), BusyMixin]
};
</script>

<style>
.center {
  display: flex;
  justify-content: center;
  height: 100%;
  align-items: center;
  text-align: center;
}
</style>
