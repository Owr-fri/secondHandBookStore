<template>
  <div class="search-box clearfix">
    <input
      class="search-input"
      type="text"
      v-model="searchKey"
      placeholder="书名,作者,ISBN"
      @keyup.enter="searchBook(searchKey)"
    />
    <input
      class="search-btn"
      type="button"
      value="搜 索"
      @click="searchBook(searchKey)"
    />
  </div>
</template>
<script setup lang="ts">
import { ref, getCurrentInstance } from "vue";

const { proxy } = getCurrentInstance() as any;

let searchKey = ref("");

const searchBook = (val: string) => {
  if (val == "") {
    return;
  }
  proxy.$router.push({
    path: "/search",
    query: {
      searchKey: val,
    },
  });
};
</script>
<style scoped lang="scss">
.search-box {
  float: right;
  margin-top: 5px;
}
.search-input {
  width: 396px;
  height: 34px;
  line-height: 34px;
  padding: 0 48px 0 10px;
  line-height: 18px;
  font-size: 12px;
  color: #333;
  border: none;
  outline: none;
  border-radius: 0;
  border: 2px solid #8c222c;
}
.search-btn {
  width: 88px;
  height: 34px;
  position: relative;
  top: 1px;
  padding: 0px 6px;
  border: 0;
  padding-left: 2px;
  line-height: 28px;
  font-size: 16px;
  color: #fff;
  border-radius: 0;
  background-color: #8c222c;
  text-align: center;
  cursor: pointer;
}
</style>
