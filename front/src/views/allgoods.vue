<template>
  <div>
    <div class="shop-top-text">{{ data.user.user_name }}</div>
    <div class="goods_list_box clearfix">
      <div class="store_con">
        <div class="store-info clearfix" v-if="data.user">
          <div class="store-top clearfix">
            <div class="user-avatar f_left">
              <a :href="'/all/' + data.user.id"
                ><el-avatar :src="proxy.$API.BASE_URL + data.user.avatar"
              /></a>
            </div>
            <div class="user-name f_left">
              <a :href="'/all/' + data.user.id"
                ><h4 class="user-name-text">{{ data.user.user_name }}</h4></a
              >
            </div>
          </div>
          <div class="store-center clearfix">
            <ul>
              <li class="item">
                <span class="item-title">称呼</span
                ><span>{{ data.user.chenghu }}</span>
              </li>
              <li class="item">
                <span class="item-title">手机号</span
                ><span>{{ data.user.phone }}</span>
              </li>
              <li class="item">
                <span class="item-title">资质认证</span>
                <span title="实名认证">
                  <i class="iconfont qualification-icon">&#xe673;</i>
                </span>
              </li>
            </ul>
          </div>
          <div class="store-bottom clearfix">
            <ul>
              <li class="item">
                <span class="item-title"> 邮箱 </span>
                <span class="email-text">{{ data.user.email }}</span>
              </li>
              <li class="item">
                <span class="item-title"> 地址 </span>
                <span class="address-text">{{ data.user.sendAddress }}</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
      <div class="books_list_con">
        <div class="detail-book-list" v-if="data.books.length">
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
                    style="width: 78px; height: 78px"
                    fit="scale-down"
                    :src="proxy.$API.BASE_URL + item.image"
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
                    :src="proxy.$API.BASE_URL + item.image"
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
              <div class="f_left inline-box list-user">
                <a :href="'/user/' + item.user_id" style="color: #666">{{
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
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { storeToRefs } from "pinia";
import { ElMessage } from "element-plus";
import { useUserStore } from "@/stores/store";
import { ref, getCurrentInstance, inject, onBeforeMount, reactive } from "vue";

const { proxy } = getCurrentInstance() as any;
const axios: any = inject("axios");

const store = useUserStore();
const userInfoSotre = storeToRefs(store);

let data: any = reactive({
  books: [],
  user: {},
});

let showBigImgId = ref(-1);

onBeforeMount(() => {
  let uid = proxy.$route.params.id;
  axios
    .get(proxy.$API.API_ALL_GOODS_BY_USER, {
      params: {
        u: uid,
      },
    })
    .then((res: any) => {
      data.books = res.books;
      data.user = res.user;
    });
});

const showBigImgfunc = (value: any) => {
  showBigImgId.value = value;
};

const closeBigImgfunc = () => {
  showBigImgId.value = -1;
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
.shop-top-text {
  height: 80px;
  line-height: 80px;
  font-size: 46px;
  text-align: center;
  vertical-align: middle;
  color: #333;
  background: #f2f1ea;
}
.goods_list_box {
  width: 1000px;
  margin: 0 auto;
}
.store_con {
  width: 200px;
  margin-top: 30px;
  float: left;
}
.store-info {
  position: relative;
  border: 1px solid #e5e5e5;
  padding-bottom: 10px;
  border-top: 2px solid #8c222c;
}
.store-top {
  margin: 12px 10px 0px 10px;
  padding-bottom: 6px;
  // border-bottom: 1px solid #e5e5e5;
}
.store-center {
  // margin: 4px 10px 0px 10px;
  background-color: #fafafa;
  padding: 4px 10px 6px 10px;
}
.user-name {
  position: relative;
  top: -5px;
  margin-left: 10px;

  .user-name-text {
    font-size: 16px;
    font-weight: bold;
    color: #333;
  }
}
.store-center {
  .item {
    font-size: 13px;
    line-height: 22px;
    height: 22px;
    .item-title {
      margin-right: 10px;
      font-size: 12px;
      line-height: 22px;
      display: inline-block;
      color: #666;
    }
  }
}
.qualification-icon {
  cursor: default;
  position: relative;
  top: 1px;
}
.store-bottom {
  margin: 4px 10px 0px 10px;
  .item {
    font-size: 13px;
    line-height: 22px;
    height: 22px;
  }
  .item-title {
    margin-right: 10px;
    font-size: 12px;
    line-height: 22px;
    color: #666;
    display: inline-block;
  }
}
.address-text,
.email-text {
  float: right;
  width: 140px;
}
.store-to-personstore-btn {
  display: block;
  width: 180px;
  height: 32px;
  line-height: 32px;
  text-align: center;
  font-size: 12px;
  border-radius: 2px;
  background-color: #f6f7f6;
  border: 1px solid #e5e5e5;
  cursor: pointer;
  margin: 10px auto 5px auto;
  a {
    color: #333;
  }
}
.store-to-personstore-btn:hover {
  background-color: #fff;
  border: 1px solid #d4cbbf;
  a {
    color: #a9987f;
  }
}
.books_list_con {
  width: 780px;
  float: left;
  margin-top: 10px;
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
  width: 230px;
  margin-right: 20px;
  font-size: 14px;
  line-height: 22px;
  a {
    color: var(--vt-c-href-color) !important;
  }
}
.list-user {
  width: 210px;
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
.quick-buy-btn-text {
  color: #bf7f5f;
}
</style>
