<template>
  <div class="card clearfix" :class="data.selected ? 'selected' : ''">
    <div class="chk f_left">
      <div
        class="checkbox"
        @click="$emit('selectItem', data.id, !data.selected)"
      >
        <i class="iconfont icon-active" v-if="data.selected">&#xe608;</i>
        <i class="iconfont" v-else>&#xe8ed;</i>
      </div>
    </div>
    <div class="info clearfix f_left">
      <div
        class="img-box f_left"
        @mouseenter="showBigImgfunc()"
        @mouseleave="closeBigImgfunc()"
      >
        <a :href="data.book.image">
          <el-image
            style="width: 88px; height: 88px"
            fit="scale-down"
            :src="data.book.image"
          >
            <template #error>
              <div class="image-slot">本书目未收录图片</div>
            </template>
          </el-image></a
        >
        <div class="big-img-box" v-show="showBigImg">
          <el-image
            style="width: 350px; height: 350px"
            fit="scale-down"
            :src="data.book.image"
          >
            <template #error>
              <div class="image-slot">本书目未收录图片</div>
            </template>
          </el-image>
        </div>
      </div>
      <div class="book-info-box f_left">
        <span class="bookname">
          {{ data.book.name }}
        </span>
      </div>
    </div>
    <div class="other f_left">
      <div class="only-price-box f_left">
        <span class="only-price-text">￥{{ data.book.price }}</span>
      </div>
      <div class="count-box f_left">
        <span class="count-text">仅此一件</span>
      </div>
      <div class="item-price-box f_left">
        <span class="item-price-text">￥{{ data.book.price }}</span>
      </div>
      <div class="operate-box f_left">
        <a
          href="javascript:;"
          class="delete-cart-item"
          @click="$emit('deleteOrder', data.id)"
        >
          删除
        </a>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, onMounted, getCurrentInstance } from "vue";

const { proxy } = getCurrentInstance() as any;

const props: any = defineProps<{
  data: {
    id: number;
    book: {
      id: number;
      image: string;
      name: string;
      price: number;
    };
    selected: boolean;
  };
}>();

let showBigImg = ref(false);

onMounted(() => {});

const showBigImgfunc = () => {
  showBigImg.value = true;
};

const closeBigImgfunc = () => {
  showBigImg.value = false;
};

const deleteOrder = (val: number) => {
  //   console.log(proxy.$lodash.findIndex(props.data, ["id", val]));
};
</script>

<style scoped lang="scss">
.card {
  border: 1px solid #f5f5f5;
  background-color: #f5f5f5;
  border-radius: 18px;
  margin: 0 24px;
  height: 130px;
}
.checkbox {
  position: absolute;
  top: 41%;
  display: block;
  padding: 0px 8px;
  cursor: pointer;
}
.chk {
  margin-left: 15px;
  height: 100%;
  width: 40px;
  overflow: hidden;
  display: block;
}
.info {
  width: 400px;
  margin-top: 20px;
}
.img-box {
  position: relative;
  float: left;
  width: 90px;
  height: 90px;
  line-height: 88px;
  border: 1px solid #e5e5e5;
  text-align: center;
  background-color: #ffffff;
  font-size: 0;
}
.big-img-box {
  position: absolute;
  top: 0;
  left: 90px;
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
.bookname {
  font-weight: 700;
  max-height: 60px;
  line-height: 30px;
}
.book-info-box {
  width: 240px;
  margin-left: 10px;
  //   height: 90px;
}
.other {
  margin-top: 20px;
  padding-left: 60px;
}
.only-price-text {
  font-size: 12px;
  color: #3c3c3c;
  font-weight: 700;
  font-family: Verdana, Tahoma, arial;
}
.only-price-box {
  width: 120px;
}
.count-box {
  width: 104px;
}
.count-text {
  color: #db6912;
  font-size: 12px;
}
.item-price-text {
  color: #f40;
  font-weight: 700;
}
.item-price-box,
.operate-box {
  width: 100px;
}
.delete-cart-item {
  font-size: 13px;
}
.selected {
  border: 1px solid #8c222c;
}
.icon-active {
  color: #8c222c;
}
</style>
