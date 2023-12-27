<template>
  <div
    class="item-img"
    @mouseenter="showBigImgfunc(props.id)"
    @mouseleave="closeBigImgfunc()"
  >
    <a :href="props.image" target="_blank">
      <el-image
        style="height: 136px; margin: 0 auto; display: block"
        fit="scale-down"
        :src="props.image"
      >
        <template #error>
          <div class="image-slot">本书目未收录图片</div>
        </template>
      </el-image>
    </a>
    <div class="big-img-box" v-show="props.id == showBigImgId">
      <el-image
        style="width: 350px; height: 350px"
        fit="scale-down"
        :src="props.image"
      >
        <template #error>
          <div class="image-slot">本书目未收录图片</div>
        </template>
      </el-image>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onBeforeMount, ref, getCurrentInstance, inject, onUpdated } from "vue";

const { proxy } = getCurrentInstance() as any;
const axios: any = inject("axios");

let showBigImgId = ref(-1);

const props = defineProps<{
  id?: number;
  image?: string;
}>();

const showBigImgfunc = (value: any) => {
  showBigImgId.value = value;
};

const closeBigImgfunc = () => {
  showBigImgId.value = -1;
};
</script>

<style scoped lang="scss">
.item-img {
  position: relative;
  float: left;
  width: 80px;
  height: 80px;
  line-height: 78px;
  border: 1px solid #e5e5e5;
  text-align: center;
  margin-right: 18px;
  font-size: 0;
}
.big-img-box {
  position: absolute;
  top: 0;
  left: 88px;
  z-index: 10;
  width: 350px;
  height: 350px;
  line-height: 298px;
  text-align: center;
  overflow: hidden;
  background-color: #fff;
  border: 1px solid #e5e5e5;
  box-shadow: 0 0 2px #e5e5e5;
  font-size: 0;
}
.image-slot {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  // background: var(--el-fill-color-light);
  color: var(--el-text-color-secondary);
  font-size: 12px;
}
</style>
