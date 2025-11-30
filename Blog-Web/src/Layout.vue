<script setup lang="ts">
import { ref } from 'vue';

const currentNav = ref('首页');
</script>

<template>
  <div>
    <NavBar 
      :currentNav="currentNav"
      @update:currentNav="(val) => currentNav = val"
    />
    <router-view />
  </div>
</template>
