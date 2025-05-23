<template>
  <section class="resource-list">
    <h2>Imported Resources</h2>
    <ul v-if="resources.length > 0">
      <li v-for="resource in resources" :key="resource.id" @click="selectResource(resource)">
        <strong>{{ resource.name }}</strong> ({{ resource.file_path }}) - {{ resource.file_counts?.total || 0 }} files
      </li>
    </ul>
    <p v-else>No resources imported yet.</p>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';

// Define a basic type for Resource for now
interface Resource {
  id: string;
  name: string;
  file_path: string;
  file_counts?: { total?: number; image?: number; video?: number; }; // Make it optional for dummy data
  // Add other fields as needed from backend models.py
}

const resources = ref<Resource[]>([]);
const selectedResource = ref<Resource | null>(null);

const fetchResources = () => {
  // Dummy data
  resources.value = [
    { id: '1', name: 'Sample Project A', file_path: '/path/to/project_a', file_counts: { total: 10, image: 5, video: 2 } },
    { id: '2', name: 'Holiday Photos', file_path: '/path/to/holidays', file_counts: { total: 150, image: 150 } },
  ];
  console.log('Fetched dummy resources');
};

const selectResource = (resource: Resource) => {
  selectedResource.value = resource;
  console.log('Selected resource:', resource);
  // In a real app, this might emit an event to show details in ResourceDetail.vue
};

onMounted(() => {
  fetchResources();
});
</script>

<style scoped>
.resource-list ul {
  list-style: none;
  padding: 0;
}
.resource-list li {
  padding: 10px;
  border: 1px solid #eee;
  margin-bottom: 5px;
  cursor: pointer;
}
.resource-list li:hover {
  background-color: #f9f9f9;
}
</style>
