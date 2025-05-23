<template>
  <section class="import-section">
    <h2>Import Resources</h2>
    <input type="text" v-model="directoryPath" placeholder="Enter directory path" />
    <button @click="handleImport">Import</button>
    <p v-if="message">{{ message }}</p>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const directoryPath = ref('');
const message = ref('');

const handleImport = () => {
  if (!directoryPath.value.trim()) {
    message.value = 'Please enter a directory path.';
    return;
  }
  message.value = `Attempting to import from: ${directoryPath.value}`;
  // Actual API call will be added later
  console.log('Importing from:', directoryPath.value);
};
</script>

<style scoped>
.import-section input {
  margin-right: 10px;
  padding: 8px;
  min-width: 300px;
}
.import-section button {
  padding: 8px 15px;
}
</style>
