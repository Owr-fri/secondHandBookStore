<template>
  <div class="transactions_con">
    <el-image-viewer
      v-if="imageViewerFlag"
      @close="closeImageViewer"
      :url-list="[imageViewerImage]"
    />
    <div class="win-mask" v-show="showWin">
      <div class="win_box">
        <div class="close-btn">
          <a id="loginWinCloseBtn" href="javascript:;" @click="showWin = false">
            <span class="iconfont close-icon">&#xe60e;</span>
          </a>
        </div>
        <div class="overwin clearfix">
          <h3 class="title pl_30">填写快递单号</h3>
          <div class="input_box">
            <span class="input_box_label">快递单号</span>
            <div style="width: 240px; display: inline-block">
              <el-input v-model="currentTrade.courier_number" width="200" />
            </div>
          </div>
          <div class="submit_box">
            <input
              class="submit_btn"
              type="button"
              value="保存修改"
              @click="saveCourierNumber"
            />
          </div>
        </div>
      </div>
    </div>
    <el-table :data="data.orders" height="450" style="width: 100%">
      <el-table-column
        fixed
        sortable
        prop="trade.num"
        label="订单号"
        width="160"
      />
      <el-table-column label="书名" width="150" prop="goods.name" />
      <el-table-column prop="trade.address.name" label="购买人" width="100" />
      <el-table-column prop="trade.address.phone" label="手机号" width="130" />
      <el-table-column
        prop="trade.address.total_address"
        label="收货地址"
        width="240"
      />
      <el-table-column label="价格" width="80" prop="goods.price" />
      <el-table-column
        prop="is_pay"
        label="是否支付"
        width="100"
        :align="'center'"
        :filter-method="filterIsPay"
        :filters="[
          { text: '是', value: true },
          { text: '否', value: false },
        ]"
      >
        <template #default="scope">
          <span>{{ scope.row ? "是" : "否" }}</span>
        </template>
      </el-table-column>

      <el-table-column label="图片" width="100">
        <template #default="scope">
          <el-button
            link
            type="primary"
            size="default"
            @click="showImageViewer(scope.row.goods.image)"
            >查看图片</el-button
          >
        </template>
      </el-table-column>
      <el-table-column prop="courier_number" label="快递单号" width="140">
        <template #default="scope">
          <el-button
            v-if="scope.row.courier_number == null"
            link
            type="primary"
            size="default"
            @click="delivery(scope.row)"
            >点击发货</el-button
          >
          <div v-else>
            <span>{{ scope.row.courier_number }}</span>
            <el-button
              class="ml_5"
              link
              type="primary"
              size="small"
              @click="delivery(scope.row)"
              >修改</el-button
            >
          </div>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>
<script setup lang="ts">
import { ref, reactive, onBeforeMount, getCurrentInstance, inject } from "vue";
import { ElMessage, ElImageViewer } from "element-plus";
import { useUserStore } from "@/stores/store";
import { storeToRefs } from "pinia";

const { proxy } = getCurrentInstance() as any;
const axios: any = inject("axios");

const store = useUserStore();
const userInfoSotre = storeToRefs(store);

let data: any = reactive({
  orders: [],
});

let currentTrade = ref<any>("");
let imageViewerFlag = ref<boolean>(false);
let imageViewerImage = ref<string>("");
let showWin = ref<boolean>(false);

onBeforeMount(() => {
  axios.get(proxy.$API.API_TRANSACTIONS).then((res: any) => {
    if (res.code == 401) {
      ElMessage({
        type: "error",
        message: res.error,
      });
      userInfoSotre.notLogin.value = true;
    } else {
      console.log(res);
      data.orders = res;
    }
  });
});

// 打开书籍图片
const showImageViewer = (val: string) => {
  imageViewerImage.value = val;
  imageViewerFlag.value = true;
};
// 关闭书籍图片
const closeImageViewer = () => {
  imageViewerFlag.value = false;
  imageViewerImage.value = "";
};

const filterIsPay = (value: any, row: any) => {
  return row.is_pay === value;
};

// 发货
const delivery = (val: any) => {
  showWin.value = true;
  currentTrade.value = val;
};

// 提交快递单号
const saveCourierNumber = () => {
  console.log(currentTrade.value);
  axios
    .put(proxy.$API.API_TRANSACTIONS, {
      trade: currentTrade.value.trade.num,
      n: currentTrade.value.courier_number,
    })
    .then((res: any) => {
      if (res.code == 200) {
        ElMessage({
          type: "success",
          message: res.msg,
        });
        showWin.value = false;
      } else {
        ElMessage({
          type: "error",
          message: res.error,
        });
      }
    });
};
</script>

<style scoped lang="scss">
.ml_10 {
  margin-left: 10px;
}
.ml_5 {
  margin-left: 5px;
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
.win_box {
  position: fixed;
  top: 60%;
  left: 60%;
  z-index: 1001;
  width: 630px;
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
.title {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 20px;
}
.pl_30 {
  padding-left: 30px;
}
.input_box {
  margin-left: 30px;
}
.input_box_label {
  margin-right: 20px;
  line-height: 32px;
}
.submit_btn {
  float: right;
  margin-top: 60px;
  margin-right: 50px;
  background-color: #8c222c;
  border: 0px;
  font-size: 17px;
  padding: 7px 25px;
  border-radius: 5px;
  color: #fff;
  font-weight: bold;
  cursor: pointer;
}
.submit_btn:active {
  opacity: 0.7;
}
</style>
