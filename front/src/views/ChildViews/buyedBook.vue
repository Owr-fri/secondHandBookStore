<template>
  <div class="buyed_book_con">
    <div class="title"><h3>已买书籍</h3></div>
    <div class="bookshelf"></div>
    <div class="books_con" v-if="data.bookList.length">
      <div class="book_item" v-for="item in data.bookList">
        <div class="book_img">
          <el-image
            style="width: 120px; height: 140px"
            fit="scale-down"
            :src="item.image"
          >
            <template #error>
              <div class="image-slot">本书目未收录图片</div>
            </template>
          </el-image>
        </div>
        <div class="book_name">
          <span class="book_name_text">{{ item.name }}</span>
          <p>
            <span class="book_seller_text">卖家：{{ item.user }}</span>
          </p>
        </div>
      </div>
    </div>
    <div class="no_book" v-else>
      <h2>无已购书籍</h2>
    </div>
  </div>
</template>
<script setup lang="ts">
import {
  ref,
  getCurrentInstance,
  inject,
  onBeforeMount,
  watch,
  reactive,
} from "vue";

const { proxy } = getCurrentInstance() as any;
const axios: any = inject("axios");

let data: any = reactive({
  bookList: [],
});

onBeforeMount(() => {
  axios.get(proxy.$API.API_PURCHASEDBOOKS).then((res: any) => {
    data.bookList = res;
  });
});
</script>
<style scoped lang="scss">
h3 {
  font-size: 18px;
  font-weight: 700;
}
.title {
  margin-left: 10px;
}
.bookshelf {
  margin: 10px 0 25px 10px;
  position: relative;
  left: -5px;
  width: 700px;
  height: 16px;
  background-color: #8c222c;
  border-top-right-radius: 8px;
  border-bottom-right-radius: 8px;

  &::before {
    content: ""; /*不换行空格*/
    display: inline-block;
    position: relative;
    top: -1px;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    border-bottom-left-radius: 0px;
    border-top-left-radius: 0px;
    background: #fff;
    z-index: 100;
  }
}
.no_book,
.books_con {
  min-height: 400px;
}
.no_book {
  text-align: center;
  padding: 150px 0 200px 0;
}
.books_con {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  grid-gap: 20px;
}
.book_name,
.book_img {
  width: 122px;
}
.book_img {
  border: 1px solid #e5e5e5;
  height: 142px;
}
.book_name {
  text-align: center;
  margin-top: 4px;
  .book_name_text {
    font-size: 16px;
    color: #333;
  }
  .book_seller_text {
    font-size: 12px;
    color: #999;
  }
}
</style>
