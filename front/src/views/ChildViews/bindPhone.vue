<template>
  <div class="bind_email_box clearfix">
    <ul class="clearfix">
      <li class="item-top">
        <span class="title">手机号：</span>
        <div class="el-input-box">
          <el-input v-model="phone" placeholder="请输入手机号" />
        </div>
      </li>
    </ul>
    <div class="submit-box">
      <input class="submit-btn" type="button" value="提交" @click="submit()" />
    </div>
  </div>
</template>
<script setup lang="ts">
import { useUserStore } from "@/stores/store";
import { storeToRefs } from "pinia";
import { ElMessage, ElStep } from "element-plus";
import { ref, getCurrentInstance, inject } from "vue";

const { proxy } = getCurrentInstance() as any;
const axios: any = inject("axios");

let phone = ref("");

const submit = () => {
  var reg = /^[1][3,4,5,7,8][0-9]{9}$/;
  console.log(reg.test(phone.value));
  if (reg.test(phone.value)) {
    axios
      .post(proxy.$API.API_BIND_PHONE, {
        phone: phone.value,
      })
      .then((res: any) => {
        if (res.code == 200) {
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
  } else {
    ElMessage({
      message: "手机号格式错误",
      type: "error",
    });
  }
};
</script>
<style scoped lang="scss">
.title {
  width: 100px;
  margin-right: 5px;
  text-align: right;
  float: left;
  line-height: 32px;
}
.el-input-box {
  width: 300px;
  display: inline-block;
}
.item-top,
.item {
  display: block;
}
.item {
  margin-top: 15px;
}
.submit-btn {
  float: right;
  margin-right: 20px;
  margin-top: 20px;
  background-color: #8c222c;
  border: 0px;
  font-size: 16px;
  padding: 7px 25px;
  border-radius: 5px;
  color: #fff;
  font-weight: bold;
  cursor: pointer;
}
.submit-btn:active {
  opacity: 0.7;
}
</style>
