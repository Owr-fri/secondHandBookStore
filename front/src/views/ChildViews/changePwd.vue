<template>
  <div class="change-password-box clearfix">
    <ul class="clearfix">
      <li class="item-top">
        <span class="title">原密码：</span>
        <div class="el-input-box">
          <el-input
            v-model="oldPwd"
            placeholder="请输入原密码"
            type="password"
            show-password
          />
        </div>
      </li>
      <li class="item">
        <span class="title">修改密码：</span>
        <div class="el-input-box">
          <el-input
            v-model="newPwd"
            type="password"
            placeholder="请输入新密码"
            show-password
          />
        </div>
      </li>
    </ul>
    <div class="submit-box">
      <input
        class="submit-btn"
        type="button"
        value="提交"
        @click="changePwdfunc()"
      />
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

const store = useUserStore();
const userInfoSotre = storeToRefs(store);

let newPwd = ref("");
let oldPwd = ref("");

const changePwdfunc = () => {
  console.log(newPwd.value, oldPwd.value);
  axios
    .put(proxy.$API.API_CHANGEPWD, {
      new: newPwd.value,
      old: oldPwd.value,
    })
    .then((res: any) => {
      console.log(res);
      if (res.code == 200) {
        ElMessage({
          message: res.msg,
          type: "success",
        });
      } else if (res.code == 401) {
        ElMessage({
          message: res.error,
          type: "error",
        });
        userInfoSotre.notLogin.value = true;
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
