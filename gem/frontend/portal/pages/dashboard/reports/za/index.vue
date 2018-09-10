<template>
  <div class="notification">
    <p class="title">Zonal assignments report</p>
    <b-field label="Hierarchy">
      <b-switch
        v-model="hierarchy">
        Display the hierarchy of zones.
      </b-switch>
    </b-field>

    <b-field label="Levels">
      <b-switch
        v-model="leavesOnly">
        Display only last nodes of tree.
      </b-switch>
    </b-field>

    <b-field>
      <PrintReport
        :params="params"
        title="Zonal Assignments Report"
        url="office/zonal/report"
        filename="Zonal Assignments Report.pdf"/>
    </b-field>
  </div>
</template>

<script>
import PrintReport from '@/components/PrintReport.vue';

export default {
  layout: 'dashboard',
  components: { PrintReport },
  data() {
    return {
      hierarchy: false,
      leavesOnly: true
    };
  },
  computed: {
    params() {
      return { hierarchy: this.hierarchy, leavesOnly: this.leavesOnly };
    }
  }
};
</script>

<style>

</style>
