<template>
  <div>
    <PrintReport
      title="Zonal Assignments Report"
      url="office/zonal/report"
      filename="Zonal Assignments Report.pdf" />
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
