<template>
  <div>
    <div class="content-header">
      <div class="header-box">
        <Search />
      </div>
    </div>
    <div class="con_center">
      <img
        src="@/assets/image/payment_success.png"
        alt=""
        width="500"
        class="success"
      />
      <h2 class="success_title">订单支付成功</h2>
      <div>
        <span class="tip">您的商品已经购买完毕</span>
      </div>
      <div class="btn_con">
        <a href="/user/order" class="check_order">查看订单</a>
        <a href="/" class="back_index">返回首页</a>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import { inject, ref, reactive, onBeforeMount, getCurrentInstance } from "vue";

const { proxy } = getCurrentInstance() as any;
const axios: any = inject("axios");

onBeforeMount(() => {
  const trade = proxy.$route.query.out_trade_no;
  const sign = proxy.$route.query.sign;
  axios
    .get(proxy.$API.API_PAY, { params: proxy.$route.query })
    .then((res: any) => {
      console.log(res);
    });
});
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
.con_center {
  width: 100%;
  text-align: center;
  margin-top: 20px;
}
.success {
  margin: 0 auto;
}
.success_title {
  font-size: 30px;
  font-weight: 700;
  color: #333;
  margin-bottom: 15px;
}
.tip {
  color: #666;
}
.btn_con {
  margin-top: 20px;
  a {
    margin: 0 14px;
  }
}
.check_order {
  background-color: #8c222c;
  color: #fff;
  width: 160px;
  height: 40px;
  line-height: 40px;
  font-size: 16px;
  display: inline-block;
  text-align: center;
  cursor: pointer;
  white-space: nowrap;
  border-radius: 2px;
}
.back_index {
  color: #a9987f;
  background-color: #fff;
  width: 160px;
  height: 40px;
  line-height: 38px;
  font-size: 16px;
  display: inline-block;
  text-align: center;
  cursor: pointer;
  white-space: nowrap;
  border-radius: 2px;
  border: 1px solid #bbb1a2;
}
</style>
