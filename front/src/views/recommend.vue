<template>
  <div class="recommend_view">
    <div class="content-header">
      <div class="header-box">
        <Search />
      </div>
    </div>

    <div class="recommend_con">
      <div class="recommend_con_head">
        <span class="recommend_title">好书推荐</span>
        <span class="num_tip">全部 {{ data.count }} 条</span>
      </div>
      <div>
        <ul class="detail-book-list-ul">
          <li
            class="clearfix item-list"
            v-for="item in data.books"
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
              <a :href="'/book/' + item.id" target="_blank" class="item-name">{{
                item.name
              }}</a>
              <div class="info_con">
                <span v-show="item.author">{{ item.author }}</span>
                <span v-show="item.translator"> / {{ item.translator }}</span>
              </div>
            </div>
            <div class="item-content-right-box f_right">
              <div class="now-price-box">
                <span class="now-price-title">现最低价</span>
                <span class="now-price" v-if="item.start_price">
                  <span class="now-price-icon">￥</span>
                  <span class="now-price-text">{{ item.start_price }}</span>
                </span>
                <span class="now-price" v-else>
                  <span class="now-price-text">暂无报价</span>
                </span>
              </div>
              <div class="item-content-right-box-bottom">
                <a :href="'book/' + item.id" class="quick-buy-btn">立即查看</a>
              </div>
            </div>
          </li>
        </ul>
      </div>
      <div class="pagination">
        <el-pagination
          small
          background
          layout="prev, pager, next"
          :page-size="20"
          :pager-count="7"
          :total="data.count"
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
import { ref, onBeforeMount, inject, getCurrentInstance, reactive } from "vue";
import Search from "../components/SearchBox.vue";
import BookImage from "@/components/BookImage.vue";

const axios: any = inject("axios");
const { proxy } = getCurrentInstance() as any;

let data: any = reactive({
  count: 0,
  books: {},
});
let count = ref(0);
let showBigImgId = ref(-1);
let currentPage = ref(1);

onBeforeMount(() => {
  axios
    .get(proxy.$API.API_RECOMMENDBOOKS, {
      params: {
        all: 1,
      },
    })
    .then((res: any) => {
      data.books = res.results;
      data.count = res.count;
    });
});

const showBigImgfunc = (value: any) => {
  showBigImgId.value = value;
};

const closeBigImgfunc = () => {
  showBigImgId.value = -1;
};

const handleCurrentChange = (val: number) => {
  axios
    .get(proxy.$API.API_RECOMMENDBOOKS, {
      params: {
        all: 1,
        page: val,
      },
    })
    .then((res: any) => {
      data.books = res.results;
      currentPage.value = val;
    });
};
</script>

<style scoped lang="scss">
.content-header {
  background: #f2f1ea;
}
.header-box {
  padding-top: 20px;
  width: 1000px;
  margin: 0 auto;
  height: 90px;
}
.recommend_con {
  position: relative;
  width: 1000px;
  padding-right: 220px;
  min-height: 100%;
  margin: 0 auto;
  overflow: hidden;
  padding-bottom: 50px;
}
.recommend_con_head {
  padding: 8px 0;
  //   height: 36px;
  border-bottom: 1px solid #e5e5e5;
}
.recommend_title {
  margin-right: 15px;
  font-size: 22px;
  color: #333;
}
.num_tip {
  font-size: 14px;
  color: #666;
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
.info_con {
  margin: 12px 0;
  font-size: 12px;
  line-height: 20px;
  color: #333;
}
.item-img {
  width: 130px;
  height: 140px;
  float: left;
  padding: 2px;
  border: 1px solid #e5e5e5;
}
.item-info {
  width: 400px;
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
  //   margin-top: 7px;
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
</style>
