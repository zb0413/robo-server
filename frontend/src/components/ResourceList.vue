<template>
  <section class="resource-list">
    <el-card>
      <template #header>
        <h2>已导入资源</h2>
      </template>
      
      <el-table
        v-if="resources.length > 0"
        :data="resources"
        style="width: 100%"
        @row-click="selectResource"
      >
        <el-table-column prop="name" label="名称" />
        <el-table-column prop="file_path" label="路径" />
        <el-table-column label="文件数量">
          <template #default="{ row }">
            {{ row.file_counts?.total || 0 }} 个文件
          </template>
        </el-table-column>
      </el-table>
      
      <el-empty v-else description="暂无导入的资源" />
    </el-card>

    <el-dialog
      v-model="dialogVisible"
      title="资源详情"
      width="70%"
    >
      <ResourceDetail
        v-if="selectedResource"
        :resource="selectedResource"
        @close="dialogVisible = false"
      />
    </el-dialog>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import ResourceDetail from './ResourceDetail.vue';

interface Resource {
  id: string;
  name: string;
  file_path: string;
  file_counts?: { total?: number; image?: number; video?: number; };
}

const resources = ref<Resource[]>([]);
const selectedResource = ref<Resource | null>(null);
const dialogVisible = ref(false);

const fetchResources = () => {
  // Dummy data
  resources.value = [
    { id: '1', name: 'Sample Project A', file_path: '/path/to/project_a', file_counts: { total: 10, image: 5, video: 2 } },
    { id: '2', name: 'Holiday Photos', file_path: '/path/to/holidays', file_counts: { total: 150, image: 150 } },
  ];
};

const selectResource = (resource: Resource) => {
  selectedResource.value = resource;
  dialogVisible.value = true;
};

onMounted(() => {
  fetchResources();
});
</script>

<style scoped>
.resource-list {
  margin: 20px 0;
}

:deep(.el-card__header) {
  padding: 10px 20px;
}

:deep(.el-card__header h2) {
  margin: 0;
  font-size: 18px;
}

:deep(.el-table .el-table__row) {
  cursor: pointer;
}

:deep(.el-table .el-table__row:hover) {
  background-color: #f5f7fa;
}
</style>
