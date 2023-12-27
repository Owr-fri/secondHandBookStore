<template>
  <div class="search_page">
    <div class="content_header">
      <div class="header_box">
        <Search />
      </div>
    </div>
    <div class="search_tab">
      <a href="javascript:;" class="tab_item"> 图书条目 </a>
    </div>
    <div class="search_con">
      <div class="crumbsBar">
        <div>
          <span>{{ count }}</span>
          <span> 条结果</span>
          <span class="splite">|</span>
          <span class="defualt_b bold">{{ proxy.$route.query.searchKey }}</span>
        </div>
      </div>
      <div class="search_main">
        <div class="sorted_header"></div>
        <div class="book-content" v-if="count">
          <div class="detail-book-list">
            <ul class="detail-book-list-ul">
              <li
                class="clearfix item-list"
                v-for="item in data.bookList"
                :key="item.id"
              >
                <div
                  class="item-img"
                  @mouseenter="showBigImgfunc(item.id)"
                  @mouseleave="closeBigImgfunc()"
                >
                  <a :href="item.image" target="_blank">
                    <el-image
                      style="height: 136px; margin: 0 auto; display: block"
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
                <div class="item-info">
                  <a
                    :href="'/book/' + item.id"
                    target="_blank"
                    class="item-name"
                    >{{ item.name }}</a
                  >
                  <div class="item-info-bottom clearfix">
                    <div class="bottom-left">
                      <li>
                        <span>作者：{{ item.author }}</span>
                      </li>
                      <li v-if="item.translator">
                        <span>译者：{{ item.translator }}</span>
                      </li>
                      <li>
                        <span>isbn：{{ item.isbn }}</span>
                      </li>
                      <li>
                        <span>版本：{{ item.revision }}</span>
                      </li>
                    </div>
                    <div class="bottom-right">
                      <li>
                        <span>出版社：{{ item.press }}</span>
                      </li>
                      <li v-if="item.published_date">
                        <span>出版时间：{{ item.published_date }}</span>
                      </li>
                    </div>
                  </div>
                  <div class="f_left new-message-box" v-if="item.messageInfo">
                    <a
                      class="new-message"
                      :href="'sbook/' + item.messageInfo.id"
                    >
                      <span class="iconfont message-icon">&#xe618;</span>
                      {{ item.messageInfo.user_name }} 于
                      {{ item.messageInfo.ptime }} 发布此书</a
                    >
                  </div>
                </div>
                <div class="item-content-right-box f_right">
                  <div class="old-price-box">
                    <span class="old-price-title">原价</span>
                    <span class="old-price">
                      <span class="old-price-icon">￥</span>
                      <span class="old-price-text">{{
                        item.original_price
                      }}</span>
                    </span>
                  </div>
                  <div class="now-price-box">
                    <span class="now-price-title">现最低价</span>
                    <span class="now-price" v-if="item.min_price">
                      <span class="now-price-icon">￥</span>
                      <span class="now-price-text">{{ item.min_price }}</span>
                    </span>
                    <span class="now-price" v-else>
                      <span class="now-price-text">暂无报价</span>
                    </span>
                    <p>
                      <span class="count">{{ item.count }} 本在售</span>
                    </p>
                  </div>
                  <div class="item-content-right-box-bottom">
                    <a :href="'book/' + item.id" class="quick-buy-btn"
                      >立即查看</a
                    >
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>
        <div class="no-book" v-else>
          <h2>暂无书籍</h2>
        </div>
      </div>
      <div class="pagination">
        <el-pagination
          small
          background
          layout="prev, pager, next"
          :page-size="20"
          :pager-count="7"
          :total="count"
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
import {
  ref,
  getCurrentInstance,
  inject,
  onBeforeMount,
  watch,
  reactive,
} from "vue";
import Search from "../components/SearchBox.vue";

const { proxy } = getCurrentInstance() as any;
const axios: any = inject("axios");

let data: any = reactive({
  bookList: [],
});

let count = ref(0);
let showBigImgId = ref(-1);
let currentPage = ref(1);

const initData = () => {
  let searchKey = proxy.$route.query.searchKey;

  axios
    .get(proxy.$API.API_SEARCH, {
      params: {
        key: searchKey,
      },
    })
    .then((res: any) => {
      data.bookList = res.results.sort((a: any, b: any) => {
        return b.count - a.count;
      });
      count.value = res.count;
      //   let _ = res.results.sort((a: any, b: any) => {
      //     return b.count - a.count;
      //   });
      //   console.log(_);
    });
};

onBeforeMount(() => {
  initData();
});

watch(
  () => proxy.$route.query.searchKey,
  (value, oldValue) => {
    initData();
  }
);

const showBigImgfunc = (value: any) => {
  showBigImgId.value = value;
};

const closeBigImgfunc = () => {
  showBigImgId.value = -1;
};

const handleCurrentChange = (val: number) => {
  let searchKey = proxy.$route.query.searchKey;

  axios
    .get(proxy.$API.API_SEARCH, {
      params: {
        key: searchKey,
        page: val,
      },
    })
    .then((res: any) => {
      data.bookList = res.results;
      count.value = res.count;
      currentPage.value = val;
    });
};
</script>

<style scoped lang="scss">
.content_header {
  background: #f2f1ea;
}
.header_box {
  padding-top: 20px;
  width: 1000px;
  margin: 0 auto;
  height: 90px;
}
.search_tab {
  width: 1000px;
  height: 40px;
  margin: 20px auto 0 auto;
  font-size: 16px;
  line-height: 40px;
  border-bottom: 1px solid #b5aa9a;
  .tab_item {
    float: left;
    display: block;
    height: 39px;
    margin-right: 30px;
    color: #666;
    font-weight: 500;
    width: 120px;
    padding-left: 0;
    text-align: center;
    background-color: #b5aa9a;
    color: #fff;
  }
}
.search_con {
  width: 1000px;
  margin: 20px auto 0 auto;
  .crumbsBar {
    font-size: 14px;
    height: 24px;
    line-height: 24px;
    margin-left: 10px;
    overflow: hidden;
    .splite {
      color: #ccc;
      margin: 0 3px;
    }
  }
  .sorted_header {
    height: 40px;
    font-size: 14px;
    line-height: 40px;
    background-color: #f8f7f3;
    margin: 15px 0 10px 0;
  }
}

// 书籍列表css开始
.item-list {
  padding: 20px 5px 20px 20px;
  border-bottom: 1px solid #e5e5e5;
  position: relative;
  min-height: 150px;
  list-style: none;
}
.big-img-box {
  position: absolute;
  top: 0;
  left: 130px;
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
.no-book {
  text-align: center;
  padding: 150px 0 250px 0;
}
.item-img {
  width: 130px;
  height: 140px;
  float: left;
  padding: 2px;
  border: 1px solid #e5e5e5;
}
.item-info {
  width: 500px;
  float: left;
  height: 140px;
  margin-left: 20px;

  .item-name {
    max-height: 44px;
    line-height: 22px;
    font-size: 14px;
    word-break: break-word;
    word-wrap: break-word;
    overflow: hidden;
    color: var(--vt-c-href-color);
  }
}

.bottom-left,
.bottom-right {
  width: 220px;
  float: left;
  margin-right: 20px;
  overflow: hidden;
}
.item-info-bottom {
  margin-top: 10px;
  color: #333;
  font-size: 12px;
  line-height: 20px;
}
.item-content-right-box {
  width: 200px;
  height: 140px;
  text-align: right;
}
.old-price::after {
  content: "";
  display: inline-block;
  position: absolute;
  left: 0;
  top: 11px;
  bottom: 0;
  width: 100%;
  height: 0.5px;
  background: #333;
}
.old-price-title,
.now-price-title {
  text-align: left;
  margin: 0 19px 0 10px;
  color: #8c222c;
  font-size: 18px;
  font-weight: bolder;
}
.old-price-icon {
  font-size: 16px;
  color: #333;
  font-weight: 500;
}
.old-price-text {
  margin-right: 5px;
  font-size: 16px;
  font-weight: 500;
  color: #333;
}
.now-price-box {
  margin-top: 7px;
  .count {
    font-size: 12px;
    color: #999;
  }
}
.now-price-icon {
  font-size: 14px;
  color: #8c222c;
  font-weight: bolder;
}
.now-price-text {
  margin-right: 5px;
  font-size: 18px;
  color: #8c222c;
  font-weight: bolder;
}
.item-content-right-box-bottom {
  position: absolute;
  bottom: 0px;
  right: 0px;
}
.quick-buy-btn {
  cursor: pointer;
  display: block;
  width: 120px;
  height: 28px;
  line-height: 26px;
  border-radius: 2px;
  margin: 0 auto;
  background: #fff;
  font-size: 12px;
  text-align: center;
  color: #bf7f5f;
  border: 1px solid #dfbfaf;
  a {
    color: #bf7f5f;
  }
}
.quick-buy-btn:hover {
  background: #f8f2ef;
  border: 1px solid #bf7f5f;
  a {
    color: #a66442;
  }
  color: #a66442;
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
// 书籍列表css结束
@media screen and (min-width: 1600px) {
  .header_box,
  .search_tab,
  .search_con {
    width: 1200px;
  }
}
</style>
