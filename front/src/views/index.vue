<template>
  <div class="content-box">
    <div class="content-header">
      <div class="header-box">
        <Search />
      </div>
    </div>
    <div class="bg-gray">
      <div class="carousel-box">
        <div class="index-carousel">
          <el-carousel>
            <el-carousel-item v-for="item in carouselList" :key="item.id">
              <a href="" target="_blank">
                <el-image
                  class="carousel-image"
                  :style="{ height: '300px', width: carouselImgWidth }"
                  :src="item.image"
                  fit="fill"
                />
              </a>
            </el-carousel-item>
          </el-carousel>
        </div>
      </div>
    </div>
    <div class="book-header">
      <div class="index">
        <a href="/"><h3 class="index-h3">首页</h3></a>
        <a href="/category">
          <h3 class="category-h3">分类</h3>
        </a>
      </div>
    </div>
    <div class="bg-gray">
      <div class="book-content clearfix">
        <div class="category-box">
          <div class="category-title">
            <span class="category-span"> 图书分类 </span>
          </div>
          <div v-for="item in category" class="cateogry-item-box">
            <div class="box-border">
              <a
                href="javascript:void(0);"
                class="to-category"
                @click="toCategoryfunc(item.id)"
                >{{ item.name }}</a
              >
            </div>
          </div>
        </div>
        <div class="recommend-box f_right">
          <div class="recommend-title">
            <h3 class="inline-box">好书推荐</h3>
            <span class="inline-box middle-font">/</span>
            <a href="recommend" class="inline-box middle-font more-recommend">
              更多
            </a>
          </div>
          <div class="recommend-book">
            <div class="book-item" v-for="item in recommendBooks" key="item.id">
              <a
                :href="'/book/' + item.id"
                target="_blank"
                :title="item.describe"
                ><el-image
                  style="width: 140px; height: 140px"
                  fit="scale-down"
                  :src="item.image"
                >
                  <template #error>
                    <div class="image-slot">本书目未收录图片</div>
                  </template>
                </el-image></a
              >
              <a :href="'/book/' + item.id" target="_blank"
                ><span class="book-name" :title="item.name">{{
                  item.name
                }}</span></a
              >
              <div class="book-author" :title="item.author">
                {{ item.author }}
              </div>
              <div class="book-start-price">
                <div class="price-item-center">
                  <i class="iconfont price-icon">&#xe600;</i>
                  <span class="price-text">{{ item.start_price }}</span>
                  <span class="qi">起</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeMount, inject, getCurrentInstance } from "vue";
import Search from "../components/SearchBox.vue";

let carouselList: any = ref([]);
let category: any = ref([]);
let recommendBooks: any = ref([]);
const carouselImgWidth = ref(window.screen.width > 1600 ? "1200px" : "1000px");

const axios: any = inject("axios");
const { proxy } = getCurrentInstance() as any;

onBeforeMount(() => {
  axios.get(proxy.$API.API_CAROUSEL).then((res: any) => {
    carouselList.value = res.results;
  });
  axios.get(proxy.$API.API_CATEGORY).then((res: any) => {
    category.value = res.results;
  });
  axios.get(proxy.$API.API_RECOMMENDBOOKS).then((res: any) => {
    recommendBooks.value = res;
  });
});

const toCategoryfunc = (val: number) => {
  proxy.$router.push({
    path: "/category",
    query: {
      id: val,
    },
  });
};
</script>

<style lang="scss" scoped>
.carousel-box {
  width: 1000px;
  margin: 0 auto;
}
.header-box {
  padding-top: 20px;
  width: 1000px;
  margin: 0 auto;
  height: 90px;
}
.content-header {
  background: #f2f1ea;
}
// .bg-gray {
//   background: #f7f7f6;
// }

.book-header,
.book-content {
  width: 1000px;
  margin: 10px auto 0px auto;
}
.index {
  padding: 0 5px;
}
.index a {
  display: inline-block;
  margin-right: 80px;
}
.index h3::after {
  content: "";
  display: inline-block;
  left: 0;
  bottom: -4px;
  width: 100%;
  height: 4px;
  background: #b5aa9a;
  position: absolute;
  transform: scaleX(0);
}
.index h3:hover:after {
  width: 100%;
  transform: scaleX(1);
  transform: scaleY(0.5);
  transform-origin: center;
  transition: transform 0.4s ease;
}
.index-h3::after {
  width: 100%;
  transform: scaleX(1) !important;
  transform: scaleY(0.5) !important;
}
.category-box {
  // padding-top: 10px;
  width: 160px;
  height: auto;
  background-color: #f7f7f6;
  float: left;
}
.category-title {
  height: 36px;
  line-height: 36px;
  border: 1px solid #8c222c;
  font-size: 16px;
  color: #fff;
  background-color: #8c222c;
}

.category-span {
  padding-left: 15px;
  font-weight: 600;
  position: relative;
  top: -1px;
}
.cateogry-item-box {
  position: relative;
  display: block;
  margin-bottom: -1px;
  height: 32px;
  line-height: 31px;
  font-size: 13px;
  background-color: #fff;
  border: 1px solid #ddd;
  cursor: pointer;
  box-sizing: border-box;
}
.box-border:hover {
  border-color: #8c222c;
}
.to-category:hover {
  display: inline-block;
  height: 16px;
  line-height: 14px;
  color: #8c222c;
  border-bottom: 1px solid #8c222c;
}
.box-border {
  position: absolute;
  top: -1px;
  left: -1px;
  z-index: 5;
  width: 160px;
  height: 32px;
  line-height: 28px;
  padding-left: 15px;
  border: 2px solid #b9767600;
}
.recommend-box {
  width: 820px;
}
.recommend-title {
  padding-bottom: 10px;
  margin: 10px 0 20px 0px;
  border-bottom: 1px solid #333;
}
.recommend-title h3 {
  line-height: 36px;
  color: #333;
  font-weight: 700;
  margin-right: 5px;
}
.recommend-title span {
  margin-right: 5px;
}
.recommend-book {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  grid-gap: 25px;
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
.book-item {
  height: 234px;
  overflow: visible;
}
.book-name:hover {
  color: #8c222c;
  transition: all 0.5s ease;
}
.book-name {
  display: block;
  width: 98px;
  font-size: 12px;
  color: #333;
  word-break: break-all;
  max-height: 40px;
  line-height: 20px;
  overflow: hidden;
  margin: 0 auto;
}
.book-author {
  width: 98px;
  height: 22px;
  text-align: left;
  overflow: hidden;
  margin: 0 auto;
  color: #999;
  font-size: 12px;
}
.book-start-price {
  position: absolute;
  width: 100%;
  left: 0;
  bottom: 0;
}
.price-item-center {
  width: 98px;
  margin: 0 auto;
  font-size: 16px;
  color: #bf7f5f;
}
.price-icon {
  margin-right: 5px;
}
.price-text {
  margin-right: 10px;
}
.qi {
  color: #bbb;
  font-size: 12px;
}

@media screen and (min-width: 1600px) {
  .header-box,
  .book-header,
  .book-content,
  .carousel-box {
    width: 1200px;
  }
  .recommend-box {
    width: 1020px;
  }
  .recommend-book {
    grid-template-columns: repeat(6, 1fr);
  }
}
</style>
