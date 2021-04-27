<template>
  <v-app>
      <v-main>
      <DataTable/>
    </v-main>
  </v-app>
</template>

<script>
import DataTable from './components/DataTable';

export default {
  name: 'App',

  components: {
    DataTable,
  },

  data: () => ({
    //
  }),
};
</script>
