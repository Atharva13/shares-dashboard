<template>
<div>
  <v-data-table
    :page="page+1"
    :pageCount="numberOfPages"
    :headers="headers"
    :items="shares"
    :options.sync="options"
    :server-items-length="totalShares"
    :loading="loading"
    :search="search"
    :footer-props="{
      'items-per-page-options': [10,50,100,200,-1],
      }"
    class="elevation-1"
    disable-sort fixed-header
  >
    <template v-slot:top>
      <v-row
          class="mt-2"
        >
        <h2 class="mt-4 ml-8">EQUITY DASHBOARD</h2>
        <v-row justify="space-around" class="ml-n16">
      <v-col
          cols="12"
          sm="6"
          md="3"
        >
      <v-text-field
        v-model="search"
        solo
        label="Search Shares"
        class="mt-3 ml-n16"
        prepend-inner-icon="mdi-shield-search"
      ></v-text-field>
      </v-col>
        </v-row>
    </v-row>
    </template>
  </v-data-table>
  <download-excel
     :data="downloadShares"
     name="shares.csv"
     type="csv"
     :fetch = "fetchData"
     class="btn btn-default mt-4">
     <v-btn color="green" small="true" class="mr-16 mt-2 float-right">
       <v-icon small="true" class="ml-n2 mr-2">mdi-file-download</v-icon>
       Export CSV</v-btn>
    </download-excel>
</div>
</template>

<script>
import axios from 'axios';

  export default {
    name : 'DataTable',
    data () {
      return {
        page: 0,
        totalShares: 0,
        numberOfPages: 0,
        shares: [],
        downloadShares: [],
        loading: true,
        options: {},
        search: '',
        pageReset: false,
        headers : [
          { text: 'Share Code', value: 'code' },
          { text: 'Share Name', value: 'name' },
          { text: 'High', value: 'highPrice' },
          { text: 'Low', value: 'lowPrice' },
          { text: 'Open', value: 'openPrice' },
          { text: 'Close', value: 'closePrice' },
        ]
      };
    },
    watch: {
      options: {
        handler() {
          this.getShares()
        }
      },
      search: {
        handler() {
          this.getShares()
        }
      },
      deep: true,
    },
    methods: {
      getShares() {
        this.loading = true;
        const { page, itemsPerPage } = this.options;
        axios.get(`http://localhost:8000/equity/?pageNumber=${page-1}&limit=${itemsPerPage}&search=${this.search}`).then(res => {
          this.loading = false;
          this.totalShares = res.data["totalShares"];
          this.numberOfPages = res.data["totalPages"];
          this.shares = res.data["shares"];
          this.pageReset = res.data["pageReset"];
          this.options.page = this.pageReset ? 1 : this.options.page
        })
      },
      async fetchData() {
        await axios.get(`http://localhost:8000/equity/?pageNumber=0&limit=${this.totalShares}&search=${this.search}`).then(res => {
          this.loading = false;
          this.totalShares = res.data["totalShares"]
          this.numberOfPages = res.data["totalPages"]
          this.downloadShares = res.data["shares"];
        })
        return this.downloadShares
      }
    },
    mounted() {
      this.getShares()
    }
  }
</script>

<style lang="scss">
.v-data-table table thead tr th {
  background: #e6e6f8 !important;
  font-size: 16px !important;
  color: #694ed6 !important;
}
.v-data-table__wrapper{max-height:calc(100vh - 220px) !important;}
</style>