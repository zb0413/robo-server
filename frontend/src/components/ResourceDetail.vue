<template>
  <section class="resource-detail" v-if="resource">
    <h2>Resource Details: {{ resource.name }}</h2>
    <p><strong>Path:</strong> {{ resource.file_path }}</p>
    <p><strong>Total Files:</strong> {{ resource.file_counts?.total || 0 }}</p>
    <p><strong>Images:</strong> {{ resource.file_counts?.image || 0 }}</p>
    <p><strong>Videos:</strong> {{ resource.file_counts?.video || 0 }}</p>
    <!-- Add more details and list of ResourceDetail items here -->
    <h3>Files:</h3>
    <ul>
      <li v-for="file in resource.details" :key="file.id">
        {{ file.name }} ({{ file.type }}) - {{ file.file_path }}
      </li>
    </ul>
     <p v-if="!resource.details || resource.details.length === 0">No file details available for this resource.</p>
  </section>
  <section v-else>
    <p>Select a resource from the list to see its details.</p>
  </section>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'; // Assuming a prop or event will update this

// Define types for Resource and ResourceDetail for dummy data
interface ResourceFile {
  id: string;
  name: string;
  type: string;
  file_path: string;
}
interface Resource {
  id: string;
  name: string;
  file_path: string;
  file_counts?: { total?: number; image?: number; video?: number; };
  details?: ResourceFile[];
}

// This component would typically receive the selected resource via props or a global state
// For now, let's imagine it's manually set for demonstration or receives it via an event bus/store
const resource = ref<Resource | null>(null);

// Dummy data for demonstration if a resource were "selected"
// In a real app, this would be driven by user interaction in ResourceList
const setDummyResource = () => {
  resource.value = {
    id: '1',
    name: 'Sample Project A (Details)',
    file_path: '/path/to/project_a',
    file_counts: { total: 10, image: 5, video: 2 },
    details: [
      { id: 'file1', name: 'image1.jpg', type: 'image', file_path: '/path/to/project_a/image1.jpg' },
      { id: 'file2', name: 'video1.mp4', type: 'video', file_path: '/path/to/project_a/video1.mp4' },
    ]
  };
};
// Call it for initial display for testing, or remove if it should start empty
// setDummyResource(); 

// Expose a method to update the resource (e.g., if an event bus was used)
// defineExpose({
//   updateResourceDetail: (selectedResource: Resource) => {
//     resource.value = selectedResource;
//   }
// });

// Or watch a prop if passed down (more common for direct child)
// const props = defineProps<{ selectedResource: Resource | null }>();
// watch(() => props.selectedResource, (newVal) => {
//  resource.value = newVal;
// });

</script>

<style scoped>
.resource-detail {
  padding: 15px;
  border: 1px solid #ddd;
  background-color: #f9f9f9;
}
.resource-detail h3 {
  margin-top: 15px;
}
.resource-detail ul {
  list-style-position: inside;
}
</style>
