<template>
  <div class="user_addr_con">
    <div class="win-mask" v-show="showWin">
      <div class="addr_win_box">
        <div class="close-btn">
          <a id="loginWinCloseBtn" href="javascript:;" @click="closeWin">
            <span class="iconfont close-icon">&#xe60e;</span>
          </a>
        </div>
        <div class="overwin">
          <createAddr
            ref="addaddr"
            @reload-addr="reloadAddr"
            :id="editAddrId"
          />
        </div>
      </div>
    </div>
    <el-table :data="data.addrList" height="240" style="width: 100%">
      <el-table-column prop="name" label="收货人" width="100" />
      <el-table-column prop="phone" label="手机" width="150" />
      <el-table-column prop="total_address" label="详细地址" width="300" />
      <el-table-column label="设置" width="120"
        ><template #default="scope">
          <div style="display: flex; align-items: center">
            <span style="margin-left: 3px" v-if="scope.row.default"
              >默认收货地址</span
            >
            <el-button v-else link type="primary" @click="setDefault(scope.row)"
              >设为默认</el-button
            >
          </div></template
        ></el-table-column
      >
      <el-table-column fixed="right" label="操作" width="120">
        <template #default="scope">
          <el-button link type="primary" @click="editAddr(scope.row)"
            >编辑</el-button
          >
          <el-button link type="primary" @click="delAddr(scope.row.id)"
            >删除</el-button
          >
        </template>
      </el-table-column>
    </el-table>
    <div class="submit-box">
      <input
        class="submit-btn"
        type="button"
        value="添加地址"
        @click="showWin = true"
      />
    </div>
  </div>
</template>
<script setup lang="ts">
import {
  ref,
  inject,
  getCurrentInstance,
  reactive,
  onBeforeMount,
  toRefs,
} from "vue";
import { regionData, CodeToText } from "element-china-area-data";
import createAddr from "@/components/createAddr.vue";
import { ElMessage } from "element-plus";

let { proxy } = getCurrentInstance() as any;
let axios: any = inject("axios");

let data: any = reactive({
  addrList: [],
});

let showWin = ref(false);
let addaddr: any = ref();
let editAddrId = ref(0);

onBeforeMount(() => {
  axios.get(proxy.$API.API_ADDRESS).then((res: any) => {
    data.addrList = res.results;
    // console.log(data.addrList);
  });
});

const closeWin = () => {
  showWin.value = false;
  addaddr.value.reloadAddressInform();
};

const editAddr = (val: any) => {
  editAddrId.value = val.id;
  showWin.value = true;
  addaddr.value.initEdit(val);
};

const reloadAddr = (val: any) => {
  axios.get(proxy.$API.API_ADDRESS).then((res: any) => {
    data.addrList = res.results;
  });
  showWin.value = false;
};

const setDefault = (val: any) => {
  axios
    .put(proxy.$API.API_ADDRESS, {
      addressInform: {
        address: val.address,
        city: val.city,
        default: true,
        county: val.county,
        id: val.id,
        name: val.name,
        phone: val.phone,
        province: val.province,
        total_address:
          CodeToText[val.province] +
          " " +
          CodeToText[val.city] +
          " " +
          CodeToText[val.county],
        user: val.user,
      },
      id: val.id,
    })
    .then((res: any) => {
      if (res.code == 200) {
        reloadAddr(res.data);
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
};

const delAddr = (val: number) => {
  axios
    .delete(proxy.$API.API_ADDRESS, {
      params: {
        id: val,
      },
    })
    .then((res: any) => {
      reloadAddr(res);
    });
};
</script>
<style scoped lang="scss">
.win-mask {
  position: fixed;
  top: 0px;
  left: 0px;
  z-index: 1000;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}
.addr_win_box {
  position: fixed;
  top: 50%;
  left: 50%;
  z-index: 1001;
  width: 900px;
  height: 472px;
  margin-top: -288px;
  margin-left: -459px;
  font-family: "microsoft yahei";
}
.close-icon {
  font-size: 36px;
  color: #ccc;
}
.close-btn {
  position: absolute;
  z-index: 1;
  right: -52px;
  top: -20px;
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
.submit-btn {
  float: right;
  margin-right: 20px;
  margin-top: 20px;
  background-color: #8c222c;
  border: 0px;
  font-size: 17px;
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
