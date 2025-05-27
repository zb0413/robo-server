<template>
  <el-container>
    <el-header>
      <el-row>
        <el-col :span="24">
          <h1>Multimedia Resource Manager</h1>
        </el-col>
      </el-row>
    </el-header>
    
    <el-main>
      <el-card class="section-card">
        <ImportSection />
      </el-card>

      <el-divider />
      
      <el-row :gutter="20">
        <el-col :span="16">
          <el-card class="section-card">
            <ResourceList />
          </el-card>
        </el-col>
        
        <el-col :span="8">
          <el-card class="section-card">
            <ResourceDetail />
          </el-card>
        </el-col>
      </el-row>

      <el-divider />
      
      <el-card class="section-card">
        <StatisticsDisplay />
      </el-card>
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { ElContainer, ElHeader, ElMain, ElCard, ElRow, ElCol, ElDivider } from 'element-plus'
import 'element-plus/dist/index.css'
import ImportSection from './components/ImportSection.vue'
import ResourceList from './components/ResourceList.vue'
import ResourceDetail from './components/ResourceDetail.vue'
import StatisticsDisplay from './components/StatisticsDisplay.vue'
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.el-header {
  background-color: #fff;
  border-bottom: 1px solid #dcdfe6;
  padding: 20px;
}

.el-header h1 {
  margin: 0;
  text-align: center;
}

.el-main {
  padding: 20px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 80px);
}

.section-card {
  margin-bottom: 20px;
}

.section-card:last-child {
  margin-bottom: 0;
}
</style>
