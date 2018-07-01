<template>
  <div>
    <PrintReport
      title="Zonal Assignment Report"
      url="office/zonal/report" />
  </div>
</template>

<script>
import PrintReport from '@/components/PrintReport.vue';

export default {
  layout: 'dashboard',
  components: { PrintReport }
};
</script>

<style>

</style>
