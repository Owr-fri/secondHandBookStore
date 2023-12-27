<template>
  <div class="header-search">
    <Search />
    <div class="detail-box">
      <h3 class="detail-title">
        {{ originBook.name }}
      </h3>
      <div class="">
        <div class="f_left detail-left">
          <div class="detail-img f_left">
            <a :href="proxy.$API.BASE_URL + originBook.image">
              <el-image
                style="width: 160px; height: 160px"
                fit="scale-down"
                :src="proxy.$API.BASE_URL + originBook.image"
              >
                <template #error>
                  <div class="image-slot">本书目未收录图片</div>
                </template>
              </el-image></a
            >
          </div>
          <div class="detail-left-top">
            <div class="info-right f_right">
              <div class="info-right-top">
                <div class="info-right-top-left">
                  <div class="item">
                    <span class="c333">作者: </span>
                    <a
                      :href="'https://www.baidu.com/s?wd=' + originBook.author"
                      target="_blank"
                    >
                      <span style="color: var(--vt-c-href-color)">{{
                        originBook.author
                      }}</span></a
                    >
                  </div>
                  <div class="item c333">
                    <span>出版社: </span>
                    <span>{{ originBook.press }}</span>
                  </div>
                  <div class="item c333">
                    <span>出版时间: </span>
                    <span>{{ originBook.published_date }}</span>
                  </div>
                  <div class="item c333">
                    <span>版次: </span>
                    <span>{{ originBook.revision }}</span>
                  </div>
                  <div class="item c333">
                    <span>isbn: </span>
                    <span>{{ originBook.isbn }}</span>
                  </div>
                  <div class="item c333">
                    <span>定价: </span>
                    <span>{{ originBook.original_price }}</span>
                  </div>
                </div>
                <div class="info-right-top-right">
                  <div class="item c333" v-if="originBook.translator">
                    <span>译者: </span>
                    <span>{{ originBook.translator }}</span>
                  </div>
                  <div class="item c333">
                    <span>页数: </span>
                    <span>{{ originBook.page_numbers }}页</span>
                  </div>
                  <div class="item c333">
                    <span>分类: </span>
                    <a
                      @click="toCategoryfunc(originBook.category)"
                      href="javascript:void(0);"
                      style="color: var(--vt-c-href-color)"
                      ><span>{{ originBook.category_name }}</span></a
                    >
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="detail-right f_right">
          <div class="detial-descibe">
            <h5>内容简介</h5>
            <div :style="{ height: descHieght, overflow: 'hidden' }" id="12">
              <span class="descibe-box" id="desc" ref="desc"
                >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{{
                  originBook.describe
                }}</span
              >
              <h5 v-show="originBook.author_brief">作者简介</h5>
              <span
                v-show="originBook.author_brief"
                class="descibe-box"
                id="author_brief"
                ref="author_brief"
                >&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{{
                  originBook.author_brief
                }}</span
              >
            </div>
            <div class="more-box clearfix" v-show="showMoreBox">
              <div
                class="f_right more-btn"
                @click="showMoreDesc()"
                v-if="showMoreBtn"
              >
                <span class="more-text">查看详情</span>
                <span class="more-icon">&#65086;</span>
              </div>
              <div class="f_right close-btn" @click="closeMoreDesc()" v-else>
                <span class="close-text">收起</span>
                <span class="close-icon">&#65085;</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="book-list-box">
      <div class="sorted-header">
        <div class="book-count inline-box">
          <span>{{ totalCount }}</span>
          <span>条</span>
        </div>
        <div class="inline-box">|</div>
        <div
          class="default-sorted inline-box"
          :class="sortedId == 1 ? 'sorted-btn-activate' : ''"
          @click="sortedfunc(1, 'default')"
        >
          综合排序
        </div>
        <div
          class="new-sorted inline-box"
          :class="sortedId == 2 ? 'sorted-btn-activate' : ''"
          @click="sortedfunc(2, 'new')"
        >
          最新上架
        </div>
        <div
          class="price-sorted inline-box"
          @mouseenter="focusPriceSorted(true)"
          @mouseleave="focusPriceSorted(false)"
        >
          <div
            class="price-text"
            :class="[
              showPriceSorted ? 'price-text-focus' : '',
              sortedId == 3 ? 'sorted-btn-activate' : '',
            ]"
          >
            {{ priceSortedText }}
          </div>
          <div class="price-select-box" v-show="showPriceSorted">
            <div
              class="price-section-item"
              @click="sortedByPrice('price', '总价从低到高', 3)"
            >
              总价从低到高
            </div>
            <div
              class="price-section-item"
              @click="sortedByPrice('-price', '总价从高到低', 3)"
            >
              总价从高到低
            </div>
          </div>
        </div>
      </div>
      <div class="detail-book-list" v-if="bookList.length">
        <ul class="detail-book-list-ul">
          <li
            class="clearfix item-list"
            v-for="item in bookList"
            :key="item.id"
          >
            <div
              class="item-img"
              @mouseenter="showBigImgfunc(item.id)"
              @mouseleave="closeBigImgfunc()"
            >
              <a :href="item.image" target="_blank">
                <el-image
                  style="width: 78px; height: 78px"
                  fit="scale-down"
                  :src="item.image"
                >
                  <template #error>
                    <div class="image-slot">本书目未收录图片</div>
                  </template>
                </el-image>
              </a>
              <div class="big-img-box" v-show="item.id == showBigImgId">
                <el-image
                  style="width: 350px; height: 350px"
                  fit="scale-down"
                  :src="item.image"
                >
                  <template #error>
                    <div class="image-slot">本书目未收录图片</div>
                  </template>
                </el-image>
              </div>
            </div>
            <div class="list-title">
              <a :href="'/sbook/' + item.id"> {{ item.name }}</a>
            </div>
            <div style="width: 240px" class="f_left inline-box">&nbsp;</div>
            <div class="f_left inline-box list-user">
              <a :href="'/all/' + item.user_id" style="color: #666">{{
                item.user_name
              }}</a>
            </div>
            <div class="f_left inline-box list-price">
              <span class="price-span">￥{{ item.price }}</span>
            </div>
            <div class="opera-box inline-box f_right">
              <div class="quick-buy-btn">
                <a
                  href="javascript:;"
                  class="quick-buy-btn-text"
                  @click="easyBuy(item.id, item.user_id)"
                  >立即购买</a
                >
              </div>
              <div class="add-cart-btn" @click="addCart(item.id)">
                加入购物车
              </div>
            </div>
          </li>
        </ul>
      </div>
      <div class="no-book" v-else>
        <h2>暂无条目</h2>
      </div>
      <div class="pagination">
        <el-pagination
          small
          background
          layout="prev, pager, next"
          :page-size="20"
          :pager-count="7"
          :total="totalCount"
          :hide-on-single-page="true"
          class="mt-4"
          :current-page="currentPage"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { storeToRefs } from "pinia";
import { ElMessage } from "element-plus";
import { useUserStore } from "@/stores/store";
import { onBeforeMount, ref, getCurrentInstance, inject, onUpdated } from "vue";
import Search from "../components/SearchBox.vue";

const { proxy } = getCurrentInstance() as any;
const axios: any = inject("axios");

let originBook: any = ref([]);
let bookList: any = ref([]);

let descHieght = ref("160px");
let showMoreBtn = ref(true);
let showMoreBox = ref(false);
let showPriceSorted = ref(false);
let sortedId = ref(1);
let priceSortedText = ref("价格");
let showBigImgId = ref(-1);
let totalCount = ref(0);
let currentPage = ref(1);

const store = useUserStore();
const userInfoSotre = storeToRefs(store);

onBeforeMount(() => {
  const bookId = proxy.$route.params.id;
  axios.get(proxy.$API.API_SECONDBOOKSLIST + `${bookId}/`).then((res: any) => {
    totalCount.value = res.count;
    originBook.value = res.results.originBook;
    bookList.value = res.results.bookList;
  });
});

onUpdated(() => {
  if (
    proxy.$refs.desc.clientHeight + proxy.$refs.author_brief.clientHeight >
    160
  ) {
    showMoreBox.value = true;
  }
});

const showMoreDesc = () => {
  descHieght.value = "auto";
  showMoreBtn.value = false;
};

const closeMoreDesc = () => {
  descHieght.value = "160px";
  showMoreBtn.value = true;
};

const focusPriceSorted = (flag: any) => {
  showPriceSorted.value = flag;
};

const sortedfunc = (id: number, val: any) => {
  const bookId = proxy.$route.params.id;
  sortedId.value = id;
  priceSortedText.value = "价格";
  if (id === 1) {
    axios
      .get(proxy.$API.API_SECONDBOOKSLIST + `${bookId}/`)
      .then((res: any) => {
        bookList.value = res.results.bookList;
        currentPage.value = 1;
      });
    return;
  }
  if (id === 2) {
    axios
      .get(proxy.$API.API_SECONDBOOKSLIST + `${bookId}/`, {
        params: {
          byOrder: val,
        },
      })
      .then((res: any) => {
        bookList.value = res.results.bookList;
        currentPage.value = 1;
      });
    return;
  }
};

const sortedByPrice = (val: any, text: string, id: any) => {
  sortedId.value = id;
  priceSortedText.value = text;
  const bookId = proxy.$route.params.id;
  axios
    .get(proxy.$API.API_SECONDBOOKSLIST + `${bookId}/`, {
      params: {
        byOrder: val,
      },
    })
    .then((res: any) => {
      bookList.value = res.results.bookList;
      currentPage.value = 1;
    });
};

const showBigImgfunc = (value: any) => {
  showBigImgId.value = value;
};

const closeBigImgfunc = () => {
  showBigImgId.value = -1;
};

const handleCurrentChange = (val: number) => {
  const bookId = proxy.$route.params.id;
  axios
    .get(proxy.$API.API_SECONDBOOKSLIST + `${bookId}/`, {
      params: {
        page: val,
      },
    })
    .then((res: any) => {
      bookList.value = res.results.bookList;
      currentPage.value = val;
    });
};

const toCategoryfunc = (val: number) => {
  proxy.$router.push({
    path: "/category",
    query: {
      id: val,
    },
  });
};

const addCart = (val: number) => {
  axios.post(proxy.$API.API_CART + `${val}/`).then((res: any) => {
    if (res.code === 201) {
      ElMessage({
        message: res.msg,
        type: "success",
      });
    } else {
      ElMessage({
        message: res.error,
        type: "error",
      });
    }
  });
};

const easyBuy = (val: number, userId: number) => {
  axios
    .get(proxy.$API.API_CHECK, {
      params: {
        id: userId,
      },
    })
    .then((res: any) => {
      if (res.code == 200) {
        proxy.$router.push({
          name: "easyBuy",
          query: { bookId: val },
        });
      } else if (res.code == 401) {
        userInfoSotre.notLogin.value = true;
        ElMessage({
          message: "请登录！",
          type: "error",
        });
      } else {
        ElMessage({
          message: res.error,
          type: "error",
        });
      }
    });
};
</script>
<style scoped lang="scss">
.header-search {
  position: relative;
  width: 1000px;
  height: 86px;
  margin: 0 auto;
  padding-top: 31px;
}
.detail-box {
  position: relative;
  width: 1000px;
  min-height: 100%;
  margin: 0 auto;
  overflow: hidden;
  padding-bottom: 50px;
}
.detail-title {
  margin: 26px 0;
  line-height: 26px;
  color: #333;
  padding-left: 20px;
  font-size: 20px;
  font-weight: 600;
}
.detail-img {
  width: 160px;
  height: 160px;
  line-height: 158px;
  text-align: center;
}
.info-right {
  float: right;
  width: 506px;
  padding-top: 3px;
  overflow: hidden;
  padding-bottom: 12px;
}
.detail-left {
  width: 706px;
}
.info-right-top {
  padding-top: 3px;
  overflow: hidden;
  padding-bottom: 12px;
}
.info-right-top-left {
  float: left;
  width: 60%;
  overflow: hidden;
}
.info-right-top-right {
  float: left;
  width: 40%;
  overflow: hidden;
}
.item {
  height: auto;
  line-height: 22px;
  font-size: 14px;
}
.detail-right {
  width: 280px;
  padding-right: 20px;

  h5 {
    font-weight: 600;
    font-size: 15px;
  }
}
.descibe-box {
  overflow: hidden;
  display: block;
  line-height: 20px;
  font-size: 13px;
  word-wrap: break-word;
  height: auto;
}
.more-btn,
.close-btn {
  cursor: pointer;

  color: var(--vt-c-href-color);
}
.close-text,
.more-text {
  font-size: 12px;
}
.more-box {
  width: 100%;
}
.more-icon {
  font-size: 12px;
  position: relative;
  top: 2px;
  margin: 3px;
}
.close-icon {
  font-size: 14px;
  position: relative;
  top: -2px;
  margin: 3px;
}
.book-list-box {
  height: 40px;
  font-size: 14px;
  line-height: 40px;
  background-color: #f8f7f3;
}
.book-count {
  padding: 0 20px;
  span {
    font-weight: 600;
  }
}
.default-sorted,
.new-sorted {
  margin: 0 20px;
  font-size: 12px;
  cursor: pointer;
}
.sorted-btn-activate {
  color: #bf7f5f;
}
.price-text {
  padding: 0 20px;
  border: 1px solid transparent;
  z-index: 1000;
  font-size: 12px;
  cursor: pointer;
  border-bottom: none;
}
.price-text-focus {
  border-bottom: none;
  background-color: #fff;
  border: 1px solid #ccc;
  border-bottom: none;
}
.price-select-box {
  position: absolute;
  top: 40px;
  left: 0;
  z-index: 999;
  padding-bottom: 5px;
  padding-top: 8px;
  border: 1px solid #ccc;
  background-color: #fff;
  overflow: hidden;
}
.price-section-item {
  line-height: 24px;
  font-size: 12px;
  margin: 5px 0;
  cursor: pointer;
  padding: 0 20px;
  width: 130px;
}
.price-section-item:hover {
  color: #8c222c;
  background-color: #f3f0e9;
}
.item-list {
  line-height: 20px;
  padding: 20px;
  border-bottom: 1px solid #e5e5e5;
  position: relative;
  min-height: 122px;
  list-style: none;
}
.detail-book-list-ul {
  margin: 0;
  padding: 0;
  list-style: none;
}
.sorted-header {
  padding-bottom: 5px;
}
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
.list-title {
  float: left;
  width: 180px;
  margin-right: 20px;
  font-size: 14px;
  line-height: 22px;
  a {
    color: var(--vt-c-href-color) !important;
  }
}
.list-user {
  width: 240px;
}
.price-span {
  font-size: 16px;
  color: #8c222c;
  font-weight: bold;
}
.quick-buy-btn {
  cursor: pointer;
  display: block;
  width: 80px;
  height: 26px;
  line-height: 24px;
  border-radius: 2px;
  margin: 0 auto;
  background: #fff;
  font-size: 12px;
  text-align: center;
  color: #bf7f5f;
  border: 1px solid #dfbfaf;
}
.quick-buy-btn:hover {
  background: #f8f2ef;
  border: 1px solid #bf7f5f;
  color: #a66442;
}
.add-cart-btn {
  cursor: pointer;
  display: block;
  width: 80px;
  height: 26px;
  line-height: 24px;
  border-radius: 2px;
  margin: 8px auto 0;
  background: #fff;
  font-size: 12px;
  text-align: center;
  color: #a9987f;
  border: 1px solid #dad4cc;
}
.add-cart-btn:hover {
  background: #f8f7f3;
  color: #967f5f;
  border: 1px solid #bbb1a2;
}
.pagination {
  margin-top: 20px;
}
.mt-4 {
  width: 400px;
  margin: 0 auto;
  justify-content: center;
  :deep(.el-pager li.is-active) {
    background-color: #8c222c !important;
  }
  :deep(.el-pager li:hover) {
    color: #c59b9e !important;
  }
}
:deep(.el-pagination button:hover) {
  color: #c59b9e !important;
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
.quick-buy-btn-text {
  color: #bf7f5f;
}
.no-book {
  text-align: center;
  padding: 150px 0 250px 0;
}
@media screen and (min-width: 1600px) {
  .header-search,
  .detail-box {
    width: 1200px;
  }
  .detail-right {
    width: 440px;
  }
  .list-user {
    width: 340px;
  }
}
</style>
