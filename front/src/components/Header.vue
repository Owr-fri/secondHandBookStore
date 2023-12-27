<template>
  <div id="navHeader" class="nav-header-box">
    <div class="win-mask" v-show="showWin">
      <div class="login-win-box register-win-box">
        <div class="close-btn">
          <a id="loginWinCloseBtn" href="javascript:;" @click="closeWin">
            <span class="iconfont close-icon">&#xe60e;</span>
          </a>
        </div>
        <div class="overwin">
          <LoginWin
            v-if="showLoginWin"
            @update:show="(showLoginWin = $event), (showWin = $event)"
            @update:name="name = $event"
            @update:avatar="avatar = $event"
          ></LoginWin>
          <RegisterWin
            v-if="showRegisterWin"
            @to-login="Login"
            @update:show="(showRegisterWin = $event), (showWin = $event)"
          ></RegisterWin>
        </div>
      </div>
    </div>
    <div class="header-warp">
      <div class="header-left-box">
        <div class="index-box">
          <a href="/"
            ><span class="iconfont index-icon">&#xe61a;</span>
            <span class="index-text">首页</span></a
          >
        </div>
      </div>
      <div class="user-info-box">
        <div
          class="item-info"
          v-if="!name"
          @mouseenter="focusfunc(true, $event)"
          @mouseleave="focusfunc(false, $event)"
        >
          <span class="login-register">登录/注册</span>
          <div v-show="focusItem" class="login-win">
            <div class="login-box">
              <div class="login-btn" @click="Login()">登录</div>
              <div class="register-btn" @click="Register()">注册</div>
            </div>
          </div>
        </div>
        <div
          class="item-info"
          v-else
          @mouseenter="focusfunc(true, $event)"
          @mouseleave="focusfunc(false, $event)"
        >
          <span class="user-name">{{ name }}</span>
          <div v-show="focusItem" class="info-win">
            <div class="user-info clearfix">
              <a href="/user/center" class="to-user-center">
                <img
                  :src="proxy.$API.BASE_URL + avatar"
                  alt=""
                  class="avatar"
                />
              </a>
              <div class="btn-group">
                <a href="/user/center" class="btn-manage">账号管理</a>
                <span class="btn-split">|</span>
                <span class="btn logout-btn" @click="logout">退出</span>
              </div>
            </div>
          </div>
        </div>
        <div class="item-info">
          <a href="/cart" class="cart item-text">
            <i class="iconfont cart-icon">&#xe899;</i>
            购物车
          </a>
        </div>
        <div class="item-info">
          <a href="/user/order" class="item-text"
            ><span class="order">我的订单</span></a
          >
        </div>
        <div class="item-info">
          <a href="/user/center" class="item-text">
            <span class="user-center">个人中心</span>
          </a>
        </div>
        <div class="item-info">
          <a href="/user/sell" class="item-text">
            <span class="user-center">我想卖书</span>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from "@/stores/store";
import { storeToRefs } from "pinia";
import LoginWin from "../components/Login.vue";
import RegisterWin from "../components/Register.vue";
import { ref, onBeforeMount, getCurrentInstance, inject, watch } from "vue";
import { ElMessage } from "element-plus";

const { proxy } = getCurrentInstance() as any;
const axios: any = inject("axios");
const reload: any = inject("reload");

const store = useUserStore();
const userInfoSotre = storeToRefs(store);

let focusItem = ref(false);
let showLoginWin = ref(false);
let showRegisterWin = ref(false);
let showWin = ref(false);
let name = ref(localStorage.getItem("name"));
let avatar = ref(localStorage.getItem("avatar"));

onBeforeMount(() => {});

watch(
  [userInfoSotre.name, userInfoSotre.avatar, userInfoSotre.notLogin],
  ([nameVal, avatarVal, loginVal], [nameOldVal, avatarOldVal, loginOldVal]) => {
    if (nameVal != nameOldVal) {
      name.value = nameVal;
    }
    if (avatarVal != avatarOldVal) {
      avatar.value = avatarVal;
    }
    if (loginVal != loginOldVal) {
      showLoginWin.value = loginVal;
      showWin.value = loginVal;
    }
    // console.log(nameVal, loginVal);
  }
);

const focusfunc = (flag: boolean, event: any) => {
  focusItem.value = flag;
};

const Login = () => {
  showWin.value = true;
  showRegisterWin.value = false;
  showLoginWin.value = true;
};

const Register = () => {
  showWin.value = true;
  showLoginWin.value = false;
  showRegisterWin.value = true;
};

const closeWin = () => {
  showWin.value = false;
  showRegisterWin.value = false;
  showLoginWin.value = false;
};

const logout = () => {
  axios.get(proxy.$API.API_LOGOUT).then((res: any) => {
    if (res.code == 200) {
      name.value = "";
      avatar.value = "";
      localStorage.removeItem("name");
      localStorage.removeItem("avatar");
      localStorage.removeItem("email");
    } else {
      ElMessage.error("退出当前用户失败!");
    }
    reload();
  });
};
</script>

<style scoped lang="scss">
.nav-header-box {
  position: relative;
  height: 36px;
  background-color: #8c222c;
}
.header-warp {
  position: relative;
  width: 1000px;
  height: 100%;
  margin: 0 auto;
}

.user-info-box {
  position: absolute;
  top: 0;
  right: 0;
  height: 36px;
  font-size: 12px;
  color: #e2c8ca;
}
.item-info {
  float: left;
  line-height: 36px;
  position: relative;
}
.index-box {
  line-height: 36px;
  position: relative;
}
.index-icon,
.index-text {
  color: #e2c8ca;
  margin-right: 5px;
  font-size: 12px;
}
.item-text {
  color: #e2c8ca;
  font-size: 12px;
  height: 36px;
  display: block;
}
.login-register,
.user-name {
  padding: 0 15px;
}
.cart,
.user-center,
.order {
  padding: 0 8px;
}
.item-info:hover {
  background-color: #7b111b;
  cursor: default;
}
.login-box {
  width: 162px;
  padding: 20px 16px 14px;
  background-color: #fff;
}
.login-win {
  left: auto;
  right: 0;
  position: absolute;
  top: 36px;
  z-index: 1000;
  width: auto;
  height: auto;
  border: 1px solid #ccc;
  background-color: #fff;
}
.login-btn {
  width: 130px;
  height: 30px;
  margin-bottom: 15px;
  line-height: 30px;
  text-align: center;
  font-size: 12px;
  border-radius: 3px;
  border: 1px solid #8c222c;
  color: #fff;
  background-color: #8c222c;
  cursor: pointer;
}
.register-btn {
  width: 130px;
  height: 30px;
  margin-bottom: 16px;
  line-height: 30px;
  text-align: center;
  font-size: 12px;
  border-radius: 3px;
  border: 1px solid #d4c4b8;
  color: #8c222c;
  background-color: #f8f7f3;
  cursor: pointer;
}
.win-mask {
  position: fixed;
  top: 0px;
  left: 0px;
  z-index: 1000;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}
.login-win-box,
.register-win-box {
  position: fixed;
  top: 50%;
  left: 50%;
  z-index: 1001;
  width: 450px;
  height: 472px;
  margin-top: -236px;
  margin-left: -200px;
  font-family: "microsoft yahei";
}
.overwin {
  position: relative;
  width: auto;
  height: auto;
  padding: 40px 0 30px 0;
  background: #f7f7f6;
  z-index: 1000002;
  overflow: visible;
}
.close-btn {
  position: absolute;
  z-index: 1;
  right: -52px;
  top: -20px;
  // width: 32px;
  // height: 32px;
}
#loginWinCloseBtn {
  display: block;
  cursor: pointer;
  // width: 32px;
  // height: 32px;
  text-decoration: none;
}
.info-win {
  position: absolute;
  top: 36px;
  z-index: 1000;
  width: auto;
  height: auto;
  border: 1px solid #ccc;
  background-color: #fff;
}
.user-info {
  width: 166px;
  padding: 15px 16px;
}
.to-user-center {
  float: left;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  overflow: hidden;
  text-align: center;
  line-height: 30px;
}
.avatar {
  display: inline-block;
  max-width: 100%;
  max-height: 100%;
  vertical-align: middle;
}
.btn-group {
  float: right;
}
.btn-split,
.logout-btn,
.btn-manage {
  margin-right: 5px;
}
.btn,
.btn-manage {
  cursor: pointer;
  color: #333;
  text-decoration: none;
}
.btn:hover,
.btn-manage:hover {
  color: #8c222c;
}

.close-icon {
  font-size: 36px;
  color: #ccc;
}
.cart-icon {
  position: relative;
  bottom: -1px;
  padding: 0 2px;
}
@media screen and (min-width: 1600px) {
  .header-warp {
    width: 1200px !important;
  }
}
</style>
