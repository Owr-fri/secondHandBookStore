<template>
  <div class="user-info-edit clearfix">
    <ul class="clearfix">
      <li>
        <span class="title">显示名：</span>
        <div v-if="editNameTag">
          <div class="name-input-box">
            <el-input v-model="currentName" placeholder="Please input" />
          </div>
          <span class="save" @click="saveName(currentName)">保存</span>
          <span class="cancel" @click="editName(false)">取消</span>
        </div>
        <div v-else>
          <span class="nickname">{{ currentName }}</span>
          <span class="editNickname" @click="editName(true)">修改</span>
        </div>
        <div v-show="editNameTag" class="edit-tips">
          2-20个字,可由中英文、数字_-组成,此字段用于显示
        </div>
      </li>
      <li>
        <span class="title">昵称：</span>
        <div v-if="editNickNameTag">
          <div class="nickname-input-box">
            <el-input v-model="currentNickName" placeholder="Please input" />
          </div>
          <span class="save" @click="saveNickName(currentNickName)">保存</span>
          <span class="cancel" @click="editNickName(false)">取消</span>
        </div>
        <div v-else>
          <span class="nickname" v-if="currentNickName">{{
            currentNickName
          }}</span>
          <span v-else>暂无昵称</span>
          <span class="editNickname" @click="editNickName(true)">修改</span>
        </div>
        <div v-show="editNickNameTag" class="edit-tips">
          2-8个字,此字段用于联系时的称呼
        </div>
      </li>
      <li>
        <span class="title">头像：</span>
        <div class="avatar-box" @click.native="upStart">
          <el-avatar shape="square" :size="120" fit="fit" :src="currentAvatar">
          </el-avatar>
        </div>
      </li>
      <li>
        <span class="title h_32">性别：</span>
        <div>
          <el-radio-group v-model="currentInfoForm.gender">
            <el-radio :label="1">男</el-radio>
            <el-radio :label="0">女</el-radio>
          </el-radio-group>
        </div>
      </li>
      <li>
        <span class="title h_26">最近登录：</span>
        <span class="last-login-time h_26">{{ data.last_login }}</span>
      </li>
      <li style="padding-top: 10px">
        <span class="title h_32">所在地：</span>
        <div class="address">
          <el-cascader
            size="default"
            :options="options"
            v-model="selectedOptions"
            @change="handleChange"
          >
          </el-cascader>
        </div>
      </li>
      <li>
        <span class="title">个性签名：</span>
        <div class="signature-input-box">
          <el-input
            v-model="currentInfoForm.signature"
            maxlength="50"
            show-word-limit
            type="textarea"
            :rows="3"
            :autosize="false"
          />
        </div>
      </li>
    </ul>
    <div class="submit-box">
      <input
        class="submit-btn"
        type="button"
        value="提交"
        @click="saveUserInfo"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useUserStore } from "@/stores/store";
import { storeToRefs } from "pinia";
import { ref, onBeforeMount, inject, getCurrentInstance, reactive } from "vue";
import { avatarEmits, ElMessage } from "element-plus";
import { regionData, CodeToText } from "element-china-area-data";

const { proxy } = getCurrentInstance() as any;
const axios: any = inject("axios");

const store = useUserStore();
const userInfoSotre = storeToRefs(store);

const options = reactive(regionData);
let selectedOptions = reactive(["110000", "110100", "110101"]);

let data: any = ref({});
let editNickNameTag = ref(false);
let editNameTag = ref(false);
let currentNickName = ref("");
let currentAvatar = ref("");
let currentName = ref("");
let currentInfoForm = reactive({
  gender: 1,
  province: "",
  city: "",
  county: "",
  sendaddress: "",
  signature: "",
});

onBeforeMount(() => {
  axios.get(proxy.$API.API_USERINFO).then((res: any) => {
    if (res.code == 401) {
      ElMessage({
        type: "error",
        message: res.error,
      });
      userInfoSotre.notLogin.value = true;
    }
    data.value = res;
    currentName.value = res.name;
    currentNickName.value = res.nickname;
    currentAvatar.value = res.avatar;
    currentInfoForm.gender = res.gender;
    currentInfoForm.province = res.province;
    currentInfoForm.city = res.city;
    currentInfoForm.county = res.county;
    currentInfoForm.sendaddress = res.sendaddress;
    currentInfoForm.signature = res.signature;
    currentInfoForm.gender = res.gender;
    selectedOptions[0] = res.province;
    selectedOptions[1] = res.city;
    selectedOptions[2] = res.county;
  });
});

const editNickName = (val: boolean) => {
  editNickNameTag.value = val;
};

const editName = (val: boolean) => {
  editNameTag.value = val;
};

const saveNickName = (val: string) => {
  axios
    .put(proxy.$API.API_CHANGENICKNAME, {
      nickName: val,
    })
    .then((res: any) => {
      if (res.code == 200) {
        // localStorage.setItem("name", currentNickName.value);
        // userInfoSotre.name.value = currentNickName.value;
        ElMessage({
          message: res.msg,
          type: "success",
        });
        editNickNameTag.value = false;
      } else if (res.code == 401) {
        ElMessage({
          message: res.error,
          type: "error",
        });
        localStorage.removeItem("name");
        localStorage.removeItem("avatar");
        localStorage.removeItem("email");
        userInfoSotre.notLogin.value = true;
      } else {
        ElMessage({
          message: res.error,
          type: "error",
        });
      }
    });
};

const saveName = (val: string) => {
  console.log(val);
  axios
    .put(proxy.$API.API_CHANGENAME, {
      name: val,
    })
    .then((res: any) => {
      if (res.code == 200) {
        localStorage.setItem("name", currentName.value);
        userInfoSotre.name.value = currentName.value;
        ElMessage({
          message: res.msg,
          type: "success",
        });
        editNameTag.value = false;
      } else if (res.code == 401) {
        ElMessage({
          message: res.error,
          type: "error",
        });
        localStorage.removeItem("name");
        localStorage.removeItem("avatar");
        localStorage.removeItem("email");
        userInfoSotre.notLogin.value = true;
      } else {
        ElMessage({
          message: res.error,
          type: "error",
        });
      }
    });
};

const uploadFile = (e: any) => {
  const file = e.target.files[0];
  const formdata = new FormData();
  formdata.append("imgFile", file);
  axios
    .post(
      proxy.$API.API_UPLOADAVATAR,
      { file },
      {
        headers: { "Content-Type": "multipart/form-data" },
      }
    )
    .then((res: any) => {
      if (res.code == 200) {
        currentAvatar.value = res.avatar;
        userInfoSotre.avatar.value = res.shotURL;
        localStorage.setItem("avatar", res.shotURL);
        ElMessage({
          message: res.msg,
          type: "success",
        });
      } else if (res.code == 401) {
        localStorage.removeItem("name");
        localStorage.removeItem("avatar");
        localStorage.removeItem("email");
        userInfoSotre.notLogin.value = true;

        ElMessage({
          message: res.error,
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

const upStart = () => {
  //创建input
  const upload = document.createElement("input");
  //设置type为file
  upload.type = "file";
  //类型
  upload.accept = "image/png, image/jpeg";
  //添加onchange事件
  upload.onchange = uploadFile;
  //模拟点击
  upload.click();
};

const handleChange = (value: any) => {
  currentInfoForm.province = value[0];
  currentInfoForm.city = value[1];
  currentInfoForm.county = value[2];
  currentInfoForm.sendaddress =
    CodeToText[value[0]] + CodeToText[value[1]] + CodeToText[value[2]];
};

const saveUserInfo = () => {
  console.log(currentInfoForm);
  axios.put(proxy.$API.API_USERINFO, currentInfoForm).then((res: any) => {
    console.log(res);
    if (res.code == 200) {
      ElMessage({
        message: res.msg,
        type: "success",
      });
    } else if (res.code == 401) {
      localStorage.removeItem("name");
      localStorage.removeItem("avatar");
      localStorage.removeItem("email");
      userInfoSotre.notLogin.value = true;

      ElMessage({
        message: res.error,
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
.user-info-edit {
  font-size: 12px;
  ul > li {
    margin-top: 5px;
  }
}
.title {
  width: 100px;
  margin-right: 5px;
  text-align: right;
  float: left;
}
.title,
.nickname,
.editNickname,
.save,
.cancel {
  line-height: 26px;
  color: #333;
}
.editNickname,
.save,
.cancel {
  margin-left: 20px;
  cursor: pointer;
  color: var(--vt-c-href-color);
}
.nickname-input-box,
.name-input-box {
  width: 170px;
  display: inline-block;
  .el-input {
    height: 26px;
  }
}
.edit-tips {
  margin-left: 105px;
  color: #999;
  margin-top: 2px;
}
.avatar-box {
  cursor: pointer;
  display: inline-block;
  margin-top: 7px;
}
.avatar-box::after {
  content: "点击上传";
  width: 100%;
  position: absolute;
  background: #000000;
  color: #ffffff;
  bottom: 4px;
  border-bottom-left-radius: 4px;
  border-bottom-right-radius: 4px;
  opacity: 0.6;
  font-size: 14px;
  text-align: center;
  left: 0px;
}
.last-login-time {
  font-size: 13px;
}
.signature-input-box {
  width: 650px;
  display: inline-block;
  margin-top: 7px;
}
.address {
  display: inline-block;
  :deep(.el-input) {
    width: 300px;
  }
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
