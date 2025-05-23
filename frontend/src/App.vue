<template>
  <div id="app">
    <h1>Multimedia Resource Manager</h1>
    
    <ImportSection />
    <hr />
    <ResourceList />
    <hr />
    <ResourceDetail /> <!-- This might be conditionally shown or part of ResourceList items -->
    <hr />
    <StatisticsDisplay />
  </div>
</template>

<script setup lang="ts">
import ImportSection from './components/ImportSection.vue';
import ResourceList from './components/ResourceList.vue';
import ResourceDetail from './components/ResourceDetail.vue';
import StatisticsDisplay from './components/StatisticsDisplay.vue';
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin-top: 20px;
  padding: 20px;
}
hr {
  margin: 20px 0;
}
</style>
