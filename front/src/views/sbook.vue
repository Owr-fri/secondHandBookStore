<template>
  <div class="shop-top-text">{{ data.user.user_name }}</div>
  <div class="nav-box">
    <div class="header clearfix">
      <div class="header-left">
        <a :href="'/all/' + data.user.id">所有商品</a>
      </div>
      <div class="header-right">
        <div class="store-search-box">
          <input
            type="text"
            id="storeSearchInput"
            class="store-search-input"
            v-model="searchKey"
            placeholder="本店搜索"
            @keyup.enter="searchBook(searchKey)"
          />
          <span class="search-btn" @click="searchBook(searchKey)"
            ><i class="iconfont">&#xe752;</i></span
          >
        </div>
      </div>
    </div>
  </div>
  <div class="shop-main">
    <div class="main-top clearfix">
      <div class="main-left clearfix f_left">
        <div class="exhibition">
          <div class="exhibition-book-img f_left">
            <a :href="data.image" target="_blank">
              <el-image
                style="width: 300px; height: 300px"
                fit="scale-down"
                :src="data.image"
              >
                <template #error>
                  <div class="image-slot">本书目未收录图片</div>
                </template>
              </el-image>
            </a>
          </div>
          <div class="f_left major">
            <div class="base-info">
              <h3 class="book-title">
                {{ data.name }}
              </h3>
              <div class="describe">
                <p>七天无理由退货让您购物无忧</p>
              </div>
              <div class="book-define" v-if="data.originbook">
                <ul class="book-define-left f_left">
                  <li>
                    <span>作者：</span>
                    <a
                      :href="
                        'https://www.baidu.com/s?wd=' + data.originbook.author
                      "
                      target="_blank"
                    >
                      <span style="color: var(--vt-c-href-color)">{{
                        data.originbook.author
                      }}</span></a
                    >
                  </li>
                  <li>
                    <span>出版社：</span>
                    <span>{{ data.originbook.press }}</span>
                  </li>
                  <li>
                    <span>ISBN：</span>
                    <span>{{ data.originbook.isbn }}</span>
                  </li>
                  <li>
                    <span> 出版时间：</span>
                    <span>{{ data.originbook.published_date }}</span>
                  </li>
                </ul>
                <ul class="book-define-right f_left">
                  <li>
                    <span>页数：</span>
                    <span>{{ data.originbook.page_numbers }}页</span>
                  </li>
                  <li>
                    <span>版次：</span>
                    <span>{{ data.originbook.revision }}</span>
                  </li>
                  <li></li>
                </ul>
              </div>
            </div>
            <div class="price-box">
              <div class="now-price-box">
                <span class="now-price-title">售价</span>
                <span>
                  <span class="now-price-icon">￥</span>
                  <span class="now-price-text">{{ data.price }}</span>
                </span>
              </div>
              <div class="old-price-box" v-if="data.originbook">
                <span class="old-price-title">原价</span>
                <span class="old-price">
                  <span class="old-price-icon">￥</span>
                  <span class="old-price-text">{{
                    data.originbook.original_price
                  }}</span>
                </span>
              </div>
              <div class="quality-box" v-if="data.originbook">
                <span class="quality-title">品相</span>
                <span class="quality-desc">全新</span>
              </div>
            </div>
            <div class="carry">
              <span class="title">运费</span>
              <span>湖南省长沙市</span>
              <span style="margin: 0 20px">至</span>
              <span>{{ location.province }}{{ location.city }}</span>
              <span style="margin: 0 10px 0 15px">快递</span>
              <span>￥5.00</span>
            </div>
            <div class="up-book-date">
              <span class="up-book-date-title"> 上书时间 </span>
              <span class="up-book-date-time">{{ data.ptime }}</span>
            </div>
            <div class="on-sell clearfix">
              <div class="go-buy">
                <a @click="easyBuy(data.id, data.user_id)" class="buy-btn"
                  >立即购买</a
                >
              </div>
              <div class="add-cart">
                <span class="add-cart-btn" @click="addCart(data.id)"
                  >添加购物车</span
                >
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="main-right f_right">
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
          <div style="width: 100%" class="store-btn-box clearfix">
            <div class="store-to-personstore-btn">
              <a :href="'/all/' + data.user.id"> 进店逛逛</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div class="desc-main">
    <div class="desc-main-top">
      <div class="nav-tab-box">
        <div class="page-tab">
          <div class="item-detail-page page-activate">
            <span class="page-tab-title">商品描述</span>
          </div>
        </div>
      </div>
    </div>
    <div class="page-con">
      <div class="book-cat" v-if="data.originbook">
        <span>商品分类：</span>
        <span>{{ data.originbook.category_name }}</span>
      </div>
      <div class="book-id">
        <span>货号：</span>
        <span>{{ data.id }}</span>
      </div>
      <div class="book-quality">
        <h3 class="book-quality-title">品相描述：全新</h3>
        <span class="book-quality-text"> 正版特价新书 </span>
      </div>
      <div class="book-describe">
        <h3 class="book-describe-title">商品描述</h3>
        <div class="book-describe-text">
          <span style="font-weight: bold">原书简介</span>
          <p class="orginbook-desc-text" v-if="data.originbook">
            {{ data.originbook.describe }}
          </p>
          <!-- <span style="font-weight: bold">简介</span>
          <p class="book-desc-text" v-if="data.originbook">
            {{ data.originbook.describe }}
          </p> -->
        </div>
      </div>
      <div class="book-img-desc">
        <h3 class="book-img-desc-title">商品图片</h3>
        <div class="img-list-box">
          <el-image style="height;: 100%" fit="scale-down" :src="data.image">
            <template #error>
              <div class="image-slot">本书目未收录图片</div>
            </template>
          </el-image>
          <div style="text-align: center; height: 30px; line-height: 30px">
            图1
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- <div class="recommendbooks">
    <h3>书籍推荐</h3>
  </div> -->
</template>
<script setup lang="ts">
import { storeToRefs } from "pinia";
import { ElMessage } from "element-plus";
import { useUserStore } from "@/stores/store";
import { ref, onBeforeMount, inject, getCurrentInstance } from "vue";

let axios: any = inject("axios");
let { proxy } = getCurrentInstance() as any;

const store = useUserStore();
const userInfoSotre = storeToRefs(store);

const bookId = proxy.$route.params.id;

let searchKey = ref("");
let data: any = ref([]);
let location: any = ref("暂无位置信息");

onBeforeMount(() => {
  axios.get(proxy.$API.API_SINGALBOOK + `${bookId}/`).then((res: any) => {
    // console.log(res);
    data.value = res;
  });
  proxy
    .$VueJsonp("https://apis.map.qq.com/ws/location/v1/ip", {
      key: "UGVBZ-RH4KU-Q73VP-BEON5-YZ4B2-KRBOV",
      output: "jsonp",
    })
    .then((res: any) => {
      if (res.message == "Success") {
        location.value = res.result.ad_info;

        // 运费API调用
        // axios
        //   .get(proxy.$API.API_GETSHIPPINGCOST, {
        //     params: {
        //       sendProvince: "广东省",
        //       sendCity: "深圳市",
        //       sendCounty: "南山区",
        //       deliveryProvince: location.value.province,
        //       deliveryCity: location.value.city,
        //       deliveryCounty: location.value.district,
        //       weight: "2",
        //     },
        //   })
        //   .then((res: any) => {
        //     console.log(res);
        //   });
      }
    });
});

const searchBook = (value: string) => {
  console.log(value);
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
.nav-box {
  position: relative;
  min-width: 1000px;
  height: 34px;
  line-height: 34px;
  background-color: #f7f7f6;
  z-index: 200;
}
.header {
  width: 1000px;
  margin: 0 auto;
}

.header-left > a {
  float: left;
  margin: 0 20px 0 8px;
  // margin-right: 0;
  height: 34px;
  font-size: 14px;
}
.header-left {
  position: relative;
  float: left;
}
.header-right {
  top: 4px;
  position: relative;
  float: right;
}
.store-search-box {
  border: 2px solid #8c222c;
  height: 24px;
}
.store-search-input {
  height: 20px;
  line-height: 20px;
  background: #f7f7f6;
  outline: none;
  border: none;
  //   top: -1px;
  color: #666;
  //   padding: 0px;
  margin-right: 10px;
  vertical-align: top;
}
.store-search-box:focus-visible {
  background: #fff;
}
.search-btn {
  vertical-align: top;
  position: relative;
  //   top: -6px;
  font-size: 12px;
  cursor: pointer;
  line-height: 20px;
  margin-right: 5px;
  height: 20px;
}
.shop-main {
  margin: 30px 0;
}
// .exhibition {
//   width: 1000px;
//   margin: 0 auto;
// }
.exhibition-book-img {
  width: 300px;
  position: relative;
  height: 300px;
  line-height: 297px;
  border: 1px solid #e5e5e5;
  text-align: center;
  overflow: hidden;
}
.book-title {
  font-weight: bolder;
  display: inline;
  font-size: 16px;
  line-height: 28px;
  color: #333;
}
.major {
  width: 460px;
  margin-left: 20px;
}
.describe > p {
  padding: 0 2px;
  font-size: 14px;
  line-height: 22px;
  color: #a5806d;
}
.book-define {
  overflow: hidden;
  margin-top: 6px;
  padding: 6px 0 6px 9px;
  font-size: 12px;
  border: 1px solid #e5e5e5;
}
.book-define > ul > li {
  height: 22px;
}
.book-define-left,
.book-define-right {
  width: 50%;
}
.price-box {
  margin-top: 10px;
  position: relative;
  padding: 10px;
  background: #f3f0e9;
}
.now-price-title,
.old-price-title,
.quality-title {
  text-align: left;
  font-size: 12px;
  margin: 0 19px 0 10px;
  color: #999;
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
.old-price-icon {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}
.old-price-text {
  margin-right: 5px;
  font-size: 14px;
  font-weight: 500;
  color: #333;
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
.quality-desc {
  font-size: 12px;
  color: #bf7f5f;
  margin-left: 1px;
  font-weight: bolder;
}
.carry {
  position: relative;
  padding: 10px 10px 5px 10px;
  font-size: 12px;
  border-bottom: 1px solid #e5e5e5;
  .title {
    margin: 0 19px 0 10px;
    color: #999;
  }
}
.up-book-date {
  height: 35px;
  line-height: 40px;
  font-size: 12px;
}
.up-book-date-title {
  padding-left: 20px;
  color: #999;
}
.up-book-date-time {
  margin-left: 20px;
}
.on-sell {
  margin-top: 9px;
}
.buy-btn {
  overflow: hidden;
  float: left;
  width: 152px;
  border-radius: 2px;
  background-color: #f8f7f3;
  color: #8c222c;
  cursor: pointer;
  border: 1px solid #8c222c;
  margin-right: 18px;
  height: 40px;
  font-size: 14px;
  line-height: 38px;
  text-align: center;
}
.add-cart {
  overflow: hidden;
  float: left;
  width: 160px;
  margin-top: -1px;
  border-radius: 2px;
  color: #fff;
  cursor: pointer;
  background-color: #8c222c;
}
.add-cart-btn {
  display: inline-block;
  height: 40px;
  width: 160px;
  font-size: 14px;
  line-height: 38px;
  text-align: center;
  box-sizing: border-box;
  color: #fff;
  cursor: pointer;
}
.main-left {
  width: 800px;
}
.main-top,
.recommendbooks {
  width: 1000px;
  margin: 0 auto;
}
.main-right {
  position: relative;
  width: 200px;
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

.desc-main {
  width: 1000px;
  margin: 0 auto;
  margin-bottom: 10px;
  border-bottom: 1px solid #e5e5e5;
}
.nav-tab-box {
  height: 47px;
}
.page-tab {
  position: relative;
  height: 46px;
  box-sizing: border-box;
  background-color: #fafafa;
  border: 1px solid #e5e5e5;
  border-left: 0;
}
.item-detail-page {
  position: relative;
  height: 45px;
  line-height: 45px;
  width: 180px;
  float: left;
  border-right: 1px solid #e5e5e5;
  border-top: 2px solid transparent;
  text-align: center;
  color: #333;
  cursor: pointer;
}
.page-activate {
  background: #fff;
  border-top: 2px solid #213667;
}
.page-tab-title {
  font-size: 16px;
  color: #333;
}
.page-con {
  padding-top: 5px;
  position: relative;
  overflow: hidden;
  min-height: 50px;
  width: 820px;
  padding-bottom: 25px;
  padding-left: 40px;
  background-color: #fff;
  padding-top: 20px;
}
.book-cat,
.book-id,
.book-quality-text,
.book-describe-text {
  font-size: 14px;
}
.book-id {
  margin: 20px 0;
}
.book-quality-title,
.book-describe-title,
.book-img-desc-title {
  font-weight: bold;
}
.book-describe-title {
  margin-top: 30px;
  margin-bottom: 10px;
}
.orginbook-desc-text,
.book-desc-text {
  margin: 4px 0;
  text-indent: 2em;
  line-height: 28px;
}
.book-img-desc-title {
  margin: 20px 0 10px 0;
}
.img-list-box {
  text-align: center;
}
</style>
