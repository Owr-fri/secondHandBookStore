<script setup lang="ts">
import navHeader from "./components/Header.vue";
import { nextTick, ref, provide } from "vue";

let isRouterAlive = ref(true);
const reload = () => {
  isRouterAlive.value = false;
  nextTick(() => {
    isRouterAlive.value = true;
  });
};

provide("reload", reload);
</script>

<template>
  <navHeader></navHeader>

  <router-view v-if="isRouterAlive" />
</template>

<style scoped></style>
