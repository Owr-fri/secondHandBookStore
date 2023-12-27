<template>
  <div class="edit_address_box" :class="error ? 'error_background' : ''">
    <ul class="clearfix">
      <li class="f_left left_fit"><span class="red_d0">*</span> 选择所在地</li>
      <li class="f_left">
        <el-cascader
          size="default"
          :options="options"
          v-model="selectedOptions"
          @change="handleChange"
          @blur="formError.addr = addressInform.county ? false : true"
        >
        </el-cascader>
        <label class="error red_d0" v-show="formError.addr">
          <span class="red_arrow"></span>
          请选择地址</label
        >
      </li>
    </ul>
    <ul class="clearfix">
      <li class="f_left left_fit"><span class="red_d0">*</span> 详细地址</li>
      <li class="f_left">
        <el-input
          style="width: 400px"
          v-model="addressInform.address"
          placeholder="请填写详细到 门牌号、楼层及房间号的详细地址"
          @blur="formError.descAddr = addressInform.address ? false : true"
        />
        <label class="error red_d0" v-show="formError.descAddr">
          <span class="red_arrow"></span>
          请输入详细地址</label
        >
      </li>
    </ul>
    <ul class="clearfix">
      <li class="f_left left_fit"><span class="red_d0">*</span> 收货人姓名</li>
      <li class="f_left">
        <el-input
          style="width: 160px"
          v-model="addressInform.name"
          placeholder=""
          @blur="formError.name = addressInform.name ? false : true"
        />
        <label class="error red_d0" v-show="formError.name">
          <span class="red_arrow"></span>
          请输入收货人姓名</label
        >
      </li>
    </ul>
    <ul class="clearfix">
      <li class="f_left left_fit"><span class="red_d0">*</span> 联系电话</li>
      <li class="f_left">
        <el-input
          style="width: 160px"
          v-model="addressInform.phone"
          placeholder="手机号码"
          @blur="formError.phone = addressInform.phone ? false : true"
        />
        <label class="error red_d0" v-show="formError.phone">
          <span class="red_arrow"></span>
          请输入联系电话</label
        >
      </li>
    </ul>
    <div class="save-con">
      <div @click="addressInform.default = !addressInform.default">
        <i
          class="iconfont defualt_b defualt_addr_icon"
          v-if="addressInform.default"
          >&#xe61d;</i
        >
        <i class="iconfont defualt_b defualt_addr_icon" v-else>&#xe8ed;</i>
        <span>设为默认收货地址</span>
      </div>
      <div class="save">
        <a
          href="javascript:void(0);"
          class="save-btn"
          @click="saveAddr()"
          style="background-color: rgb(123, 17, 27)"
        >
          保存并使用
        </a>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onBeforeUpdate, inject, getCurrentInstance, reactive } from "vue";
import { regionData, CodeToText } from "element-china-area-data";
import { ElMessage } from "element-plus";

const { proxy } = getCurrentInstance() as any;
const axios: any = inject("axios");

const options = reactive(regionData);
let selectedOptions = ref(["110000", "110100", "110101"]);

let error = ref(false);
let addressInform = reactive({
  province: "",
  city: "",
  county: "",
  address: "",
  total_address: "",
  name: "",
  phone: "",
  default: true,
});
let formError: any = reactive({
  addr: false,
  descAddr: false,
  name: false,
  phone: false,
});

const props = defineProps<{
  id?: number;
}>();

// onBeforeUpdate(() => {
//   console.log(addressInform);
// });

const reloadAddressInform = () => {
  addressInform.province = "";
  addressInform.city = "";
  addressInform.county = "";
  addressInform.address = "";
  addressInform.total_address = "";
  addressInform.name = "";
  addressInform.phone = "";
  addressInform.default = true;
  selectedOptions.value = ["110000", "110100", "110101"];
};

const handleChange = (value: any) => {
  addressInform.province = value[0];
  addressInform.city = value[1];
  addressInform.county = value[2];
  addressInform.total_address =
    CodeToText[value[0]] +
    " " +
    CodeToText[value[1]] +
    " " +
    CodeToText[value[2]];
};

const saveAddr = () => {
  formError.addr = addressInform.county ? false : true;
  formError.descAddr = addressInform.address ? false : true;
  formError.name = addressInform.name ? false : true;
  formError.phone = addressInform.phone ? false : true;
  Object.keys(formError).forEach((e) => {
    if (formError[e]) {
      error.value = true;
    }
  });

  if (error.value) {
    return;
  } else {
    if (props.id) {
      addressInform.total_address =
        CodeToText[addressInform.province] +
        " " +
        CodeToText[addressInform.city] +
        " " +
        CodeToText[addressInform.county];
      // console.log(addressInform.total_address);
      axios
        .put(proxy.$API.API_ADDRESS, {
          addressInform,
          id: props.id,
        })
        .then((res: any) => {
          if (res.code == 200) {
            proxy.$emit("reloadAddr", res.data);
            reloadAddressInform();
          } else if (res.code == 400) {
            ElMessage({
              type: "error",
              message: res.error,
            });
          } else {
            ElMessage({
              type: "error",
              message: res.error,
            });
          }
        });
    } else {
      axios
        .post(proxy.$API.API_ADDRESS, {
          addressInform,
        })
        .then((res: any) => {
          if (res.code == 200) {
            proxy.$emit("reloadAddr", res.data);
            reloadAddressInform();
          } else if (res.code == 400) {
            ElMessage({
              type: "error",
              message: res.error,
            });
          } else {
            ElMessage({
              type: "error",
              message: res.error,
            });
          }
        });
    }
  }
};

const initEdit = (val: any) => {
  addressInform.province = val.province;
  addressInform.city = val.city;
  addressInform.county = val.county;
  addressInform.address = val.address;
  addressInform.total_address = val.total_address;
  addressInform.name = val.name;
  addressInform.phone = val.phone;
  addressInform.default = val.default;
  selectedOptions.value = [val.province, val.city, val.county];
};

defineExpose({
  addressInform,
  initEdit,
  reloadAddressInform,
});
</script>

<style scoped lang="scss">
.edit_address_box {
  color: #666;
  font-size: 12px;
  padding: 20px 0;
  ul {
    margin-bottom: 12px;
    line-height: 36px;
  }
  .left_fit {
    width: 130px;
    text-align: right;
    margin-right: 20px;
  }
}
.save-con {
  padding-left: 150px;
}
.defualt_addr_icon {
  position: relative;
  bottom: -1px;
  margin-right: 10px;
  cursor: pointer;
}
.save {
  margin-top: 30px;
}
.save-btn {
  width: 140px;
  height: 36px;
  line-height: 36px;
  color: #fff;
  font-size: 14px;
  border: 1px solid #8c222c;
  display: inline-block;
  text-align: center;
  cursor: pointer;
  white-space: nowrap;
  border-radius: 2px;
}
.red_arrow {
  display: block;
  float: left;
  margin-top: 13px;
  width: 0;
  height: 0;
  border-top: 6px solid transparent;
  border-bottom: 6px solid transparent;
  border-right: 6px solid #d00000;
  margin-right: 9px;
}
.error {
  float: right;
  margin-left: 10px;
}
</style>
