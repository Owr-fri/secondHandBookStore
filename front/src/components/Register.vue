<template>
  <div class="register">
    <div class="register-wrap">
      <div class="title">
        <h3>注册</h3>
        <a
          href="javascript:;"
          id="toLogin"
          class="a-gray to-login"
          @click="$emit('toLogin')"
        >
          快速登录
        </a>
      </div>
      <el-form
        ref="registerRuleFormRef"
        :model="ruleForm"
        :rules="rules"
        label-width="70px"
        label-position="top"
        class="register-ruleForm"
        :inline-message="true"
      >
        <el-form-item label="" prop="email">
          <el-input v-model="ruleForm.email" type="email" placeholder="邮箱" />
        </el-form-item>
        <el-form-item label="" prop="name">
          <el-input v-model="ruleForm.name" type="text" placeholder="显示名" />
        </el-form-item>
        <el-form-item label="" prop="pass">
          <el-input
            v-model="ruleForm.pass"
            type="password"
            placeholder="设置密码"
          /> </el-form-item
        ><el-form-item label="" prop="checkPass">
          <el-input
            v-model="ruleForm.checkPass"
            type="password"
            placeholder="确认密码"
          />
        </el-form-item>
        <input
          class="register-btn"
          type="button"
          @click="register(registerRuleFormRef)"
          value="注 册"
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
const registerRuleFormRef = ref<FormInstance>();
const ruleForm = reactive({
  email: "431306642@qq.com",
  name: "owr",
  pass: "123456789",
  checkPass: "123456789",
});

const emit = defineEmits(["update:show"]);

const validatePass = (rule: any, value: any, callback: any) => {
  if (value === "") {
    callback(new Error("请输入密码!"));
  } else {
    if (ruleForm.checkPass !== "") {
      if (!registerRuleFormRef.value) return;
      registerRuleFormRef.value.validateField("checkPass", () => null);
    }
    callback();
  }
};

const validatePass2 = (rule: any, value: any, callback: any) => {
  if (value !== ruleForm.pass) {
    callback(new Error("两次输入的密码不一致!"));
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

const checkName = (rule: any, value: any, callback: any) => {
  const reName = /^[a-zA-Z0-9_-]+$/;
  if (reName.test(value)) {
    callback();
  } else {
    callback(new Error("昵称只能包括字母,数字,下划线,减号!"));
  }
};

const rules = reactive({
  email: [
    { required: true, message: "请输入邮箱!" },
    { validator: checkEmail, trigger: "blur" },
  ],
  name: [{ required: true, message: "请输入昵称!" }, { validator: checkName }],
  pass: [
    { validator: validatePass, required: true },
    { min: 6, max: 18, message: "密码长度必须在6-18之间" },
  ],
  checkPass: [
    {
      required: true,
      message: "请二次输入密码!",
    },
    { validator: validatePass2, trigger: "blur" },
  ],
});

const register = (form: FormInstance | undefined) => {
  if (!form) return;
  form.validate((valid) => {
    if (valid) {
      axios
        .post(proxy.$API.API_REGISTER, {
          name: ruleForm.name,
          email: ruleForm.email,
          password: ruleForm.pass,
          password_confirmation: ruleForm.checkPass,
        })
        .then((res: any) => {
          if (res.code == 200) {
            emit("update:show", false);
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
.register-wrap {
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
.register-btn {
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
  margin-top: 25px;
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
.to-login:hover {
  color: #333 !important;
}
.to-login {
  float: right;
  margin-top: 10px;
  font-size: 12px;
}
.register-ruleForm {
  margin-top: 30px;
}
</style>
