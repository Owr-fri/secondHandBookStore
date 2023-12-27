<template>
  <div class="login">
    <div class="login-wrap">
      <div class="title">
        <h3>登录</h3>
      </div>
      <el-form
        ref="loginRuleFormRef"
        :model="ruleForm"
        :rules="rules"
        label-width="70px"
        label-position="top"
        class="login-ruleForm"
        :inline-message="true"
      >
        <el-form-item label="" prop="email">
          <el-input v-model="ruleForm.email" type="email" placeholder="邮箱" />
        </el-form-item>
        <el-form-item label="" prop="pass">
          <el-input
            v-model="ruleForm.pass"
            type="password"
            placeholder="设置密码"
          />
        </el-form-item>
        <div class="forgetPass clearfix">
          <a href="" class="clearfix">忘记密码</a>
        </div>
        <input
          class="login-btn"
          type="button"
          @click="login(loginRuleFormRef)"
          value="登 录"
        />
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, inject, getCurrentInstance } from "vue";
import type { FormInstance } from "element-plus";
import { ElMessage } from "element-plus";

const { proxy } = getCurrentInstance() as any;
const axios: any = inject("axios");
const reload: any = inject("reload");
const loginRuleFormRef = ref<FormInstance>();
const ruleForm = reactive({
  email: "431306642@qq.com",
  pass: "123456",
});

const emit = defineEmits(["update:show", "update:name", "update:avatar"]);

const validatePass = (rule: any, value: any, callback: any) => {
  if (value === "") {
    callback(new Error("请输入密码!"));
  } else {
    callback();
  }
};

const checkEmail = (rule: any, value: any, callback: any) => {
  const reEmail = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
  if (reEmail.test(value)) {
    callback();
  } else {
    callback(new Error("邮箱格式不正确!"));
  }
};

const rules = reactive({
  email: [
    { required: true, message: "请输入邮箱!" },
    { validator: checkEmail, trigger: "blur" },
  ],
  pass: [
    { validator: validatePass, required: true },
    { min: 6, max: 18, message: "密码长度必须在6-18之间" },
  ],
});

const login = (form: FormInstance | undefined) => {
  if (!form) return;
  form.validate((valid) => {
    if (valid) {
      axios
        .post(proxy.$API.API_LOGIN, {
          email: ruleForm.email,
          password: ruleForm.pass,
        })
        .then((res: any) => {
          if (res.code == 200) {
            localStorage.setItem("name", res.info.name);
            localStorage.setItem("email", res.info.email);
            localStorage.setItem("avatar", res.info.avatar);
            emit("update:show", false);
            emit("update:name", res.info.name);
            emit("update:avatar", res.info.avatar);
            reload();
          } else {
            ElMessage({
              message: res.error,
              type: "error",
            });
          }
        });
    } else {
      ElMessage.error("请补全字段");
      return false;
    }
  });
};
</script>

<style scoped lang="scss">
.login-wrap {
  position: relative;
  width: 350px;
  margin: 0 auto;
}
.title h3 {
  height: 35px;
  line-height: 35px;
  font-size: 30px;
  color: #666;
  font-weight: 500;
  overflow: hidden;
  display: inline-block;
}
.login-btn {
  display: block;
  width: 100%;
  background: #8c222c;
  height: 40px;
  line-height: 40px;
  color: #fff;
  font-size: 16px;
  text-align: center;
  border-radius: 3px;
  letter-spacing: 10px;
  cursor: pointer;
  margin-top: 15px;
}
input {
  outline: none;
  border: none;
  background: none;
  vertical-align: middle;
}
a {
  text-decoration: none;
  cursor: pointer;
}
.login-ruleForm {
  margin-top: 30px;
}
.forgetPass a {
  font-size: 12px;
  color: #999 !important;
  float: right;
}
.clearfix:after {
  content: "";
  display: block;
  visibility: hidden;
  clear: both;
}
</style>
