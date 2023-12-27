<template>
  <div class="user-center">
    <div class="user-center-top clearfix">
      <a href="/user/center"><h3 class="user-center-title">个人中心</h3></a>
      <div class="search-box">
        <Search />
      </div>
    </div>
    <div class="content">
      <div class="left-bar f_left">
        <div class="left-menu-box">
          <div class="menu-box">
            <div class="lead-title">
              <h3 class="title-text">账号管理</h3>
            </div>
            <div class="lead-con">
              <ul class="user-list1">
                <li>
                  <a
                    href="javascript:void(0);"
                    @click="toChildPage('/user/center')"
                    :class="currentPath == '/user/center' ? 'current' : ''"
                    >个人资料</a
                  >
                </li>
                <li>
                  <a
                    href="javascript:void(0);"
                    @click="toChildPage('/user/changePwd')"
                    :class="currentPath == '/user/changePwd' ? 'current' : ''"
                    >修改登录密码</a
                  >
                </li>
                <li>
                  <a
                    href="javascript:void(0);"
                    @click="toChildPage('/user/bindPhone')"
                    :class="currentPath == '/user/bindPhone' ? 'current' : ''"
                    >绑定手机号</a
                  >
                </li>
              </ul>
            </div>
          </div>
          <div class="menu-box">
            <div class="lead-title">
              <h3 class="title-text">买家中心</h3>
            </div>
            <div class="lead-con">
              <ul class="user-list1">
                <li>
                  <a
                    href="javascript:void(0);"
                    @click="toChildPage('/cart')"
                    :class="currentPath == '/user/cart' ? 'current' : ''"
                    >我的购物车</a
                  >
                </li>
                <li>
                  <a
                    href="javascript:void(0);"
                    @click="toChildPage('/user/order')"
                    :class="currentPath == '/user/order' ? 'current' : ''"
                    >我的订单</a
                  >
                </li>
                <li>
                  <a
                    href="javascript:void(0);"
                    @click="toChildPage('/user/buyedBook')"
                    :class="currentPath == '/user/buyedBook' ? 'current' : ''"
                    >已买书籍</a
                  >
                </li>
                <li>
                  <a
                    href="javascript:void(0);"
                    @click="toChildPage('/user/receive_address')"
                    :class="
                      currentPath == '/user/receive_address' ? 'current' : ''
                    "
                    >我的收货地址</a
                  >
                </li>
              </ul>
            </div>
          </div>
          <div class="menu-box">
            <div class="lead-title">
              <h3 class="title-text">卖家中心</h3>
            </div>
            <div class="lead-con">
              <ul class="user-list1">
                <li>
                  <a
                    href="javascript:void(0);"
                    @click="toChildPage('/user/sell')"
                    :class="currentPath == '/user/sell' ? 'current' : ''"
                    >我想卖书</a
                  >
                </li>
              </ul>
              <ul class="user-list1">
                <li>
                  <a
                    href="javascript:void(0);"
                    @click="toChildPage('/user/bookonsale')"
                    :class="currentPath == '/user/bookonsale' ? 'current' : ''"
                    >商品管理</a
                  >
                </li>
              </ul>
              <ul class="user-list1">
                <li>
                  <a
                    href="javascript:void(0);"
                    @click="toChildPage('/user/transactions')"
                    :class="
                      currentPath == '/user/transactions' ? 'current' : ''
                    "
                    >订单交易</a
                  >
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
      <div class="right-con f_left">
        <div class="bread">
          <a href="/user/" style="color: var(--vt-c-href-color)">个人中心</a>
          <span style="margin: 10px">></span>
          <span>{{ crumbs }}</span>
        </div>
        <div class="app-box clearfix">
          <router-view></router-view>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeMount, getCurrentInstance, watch } from "vue";
import { ArrowRight } from "@element-plus/icons-vue";
import Search from "../components/SearchBox.vue";

const { proxy } = getCurrentInstance() as any;
const currentPath = ref(proxy.$route.path);

let crumbs = ref("");

let mainbaoxueDict: any = {
  "/user/center": "个人资料",
  "/user/changePwd": "修改密码",
  "/user/order": "我的订单",
  "/user/buyedBook": "已买书籍",
  "/user/receive_address": "我的收货地址",
  "/user/sell": "我想卖书",
  "/user/bookonsale": "商品管理",
  "/user/bindPhone": "绑定手机号",
  "/user/transactions": "订单交易",
};

onBeforeMount(() => {
  crumbs.value = mainbaoxueDict[currentPath.value];
});

watch(
  () => proxy.$route.path,
  (value, oldValue) => {
    currentPath.value = value;
    crumbs.value = mainbaoxueDict[currentPath.value];
  }
);

const toChildPage = (url: string) => {
  proxy.$router.push(url);
};
</script>

<style scoped lang="scss">
.user-center {
  width: 1000px;
  margin: 0 auto;
}
.user-center-top {
  height: 86px;
  padding-top: 31px;
}
.user-center-title {
  position: relative;
  font-weight: 600;
  float: left;
  line-height: 55px;
  font-size: 24px;
  color: #8c222c;
  letter-spacing: 15px;
}
.search-box {
  float: right;
  position: relative;
  top: 5px;
}
.content {
  margin-top: 20px;
}
.left-bar {
  width: 170px;
  min-height: 20px;
  position: relative;
  margin-right: 10px;
}
.left-menu-box {
  border: 1px solid #dcdcdc;
  zoom: 1;
}
.menu-box {
  margin-bottom: 1px;
}
.lead-title {
  background-color: #c63b40;
}
.title-text {
  padding-left: 25px;
  height: 33px;
  line-height: 33px;
  color: #fff;
  font-size: 16px;
  font-weight: bold;
  height: 33px;
}
.lead-con {
  padding: 5px 0;
}
.user-list1 {
  margin-left: 25px;
  li {
    height: 30px;
    line-height: 30px;
    position: relative;
    vertical-align: middle;
    overflow: hidden;
  }
  li > a:hover {
    color: #c63b40;
  }
}
.current {
  color: #c63b40;
}
.right-con {
  width: 800px;
}
.bread {
  border-bottom: 1px solid #dcdcdc;
  height: 34px;
  line-height: 34px;
  padding-left: 10px;
  font-size: 12px;
}
.app-box {
  border: 1px solid #d7d7d7;
  margin-top: 20px;
  padding: 20px 10px;
}
</style>
