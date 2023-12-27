<template>
  <div class="order_list_con">
    <div class="win-mask" v-show="showConfirm">
      <div class="addr_win_box">
        <div class="close-btn">
          <a id="loginWinCloseBtn" href="javascript:;" @click="closeConfirmWin">
            <span class="iconfont close-icon">&#xe60e;</span>
          </a>
        </div>
        <div class="overwin clearfix">
          <div class="payment_con" v-if="payNow">
            <h3 class="overwin_title">付款</h3>
            <div class="overwin_con">
              <div class="payment_info">
                <div>
                  <span>代付订单：</span> <span>共 <span>1</span> 笔</span>
                </div>
                <div>
                  <span>支付金额：￥{{ unpaymentOrder.price }}</span>
                </div>
              </div>
              <div class="payment_methods_con clearfix">
                <div><h4 class="payment_methods_title">支付方式</h4></div>
                <div
                  class="f_left Alipay_btn"
                  @click="selectMehtod(0, !payMehtods[0].flag)"
                  :class="payMehtods[0].flag ? 'btn_active' : ''"
                >
                  <i class="iconfont icon ali_icon">&#xe634;</i>
                  <span class="payment_text">支付宝支付</span>
                </div>
              </div>
            </div>
            <div class="pay_box f_right">
              <a href="javascript:;" class="pay_btn" @click="pay">跳转支付</a>
            </div>
          </div>
          <div class="order_detail" v-else-if="orderDetail">
            <h3 class="overwin_title">订单详情</h3>
            <div class="overwin_con">
              <div class="collapse">
                <el-menu
                  :default-active="activeTrade"
                  class="el-menu-demo"
                  mode="horizontal"
                  @select="handleTradeChange"
                >
                  <el-menu-item
                    :index="String(item.id)"
                    v-for="item in orderItem"
                    >{{ item.goods.name }}</el-menu-item
                  >
                </el-menu>
              </div>
              <OderDetial
                :id="Number(activeTrade)"
                :CourierNumber="activeCourierNumber"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
    <ul v-if="data.orderList.length">
      <li v-for="item in data.orderList" class="clearfix">
        <div class="order_item">
          <div class="head_info_box">
            <span>订单编号：{{ item.trade }}</span>
          </div>
          <div class="order_desc_box clearfix">
            <table width="100%" border="0" cellspacing="0">
              <tr class="book_item clearfix">
                <td class="desc_box_left">
                  <table
                    width="100%"
                    height="100px"
                    border="0"
                    cellspacing="0"
                    class="in_tab"
                  >
                    <tr
                      v-for="(i, index) in item.items"
                      :class="
                        index === item.items.length - 1
                          ? 'final_in_tab_tr'
                          : 'in_tab_tr'
                      "
                    >
                      <td class="w20" style="padding: 0 10px">
                        {{ index + 1 }}
                      </td>
                      <td class="book_img_td w70">
                        <div class="img_box">
                          <a :href="'/sbook/' + i.goods.id">
                            <el-image
                              style="width: 66px; height: 66px"
                              fit="scale-down"
                              :src="i.goods.image"
                            >
                              <template #error>
                                <div class="image-slot">本书目未收录图片</div>
                              </template>
                            </el-image></a
                          >
                        </div>
                      </td>
                      <td class="book_name" valign="top">
                        <a :href="'/sbook/' + i.goods.id" style="color: #049"
                          ><span class="product_name">{{
                            i.goods.name
                          }}</span></a
                        >
                      </td>
                      <td
                        class="w50 s_font"
                        valign="top"
                        style="vertical-align: middle"
                      >
                        <span>1件</span>
                      </td>
                      <td class="w80 s_font right">
                        <p>
                          <span>
                            {{ i.goods.price }}
                          </span>
                        </p>
                        <p>
                          <span>元/件</span>
                        </p>
                      </td>
                    </tr>
                  </table>
                </td>
                <td class="w_120 info_td" valign="middle">
                  <p>订单总金额(元)</p>
                  <p style="color: #f00; font-size: 16px">{{ item.price }}</p>
                </td>
                <td class="w_120 info_td" valign="middle">
                  <div v-if="item.cancel">
                    <p style="font-size: 14px; font-weight: 700">买家已取消</p>
                  </div>
                  <div v-else-if="item.is_pay == false">
                    <p style="font-size: 14px; font-weight: 700">
                      等待买家付款
                    </p>
                  </div>
                  <div v-else>
                    <p style="font-size: 14px; font-weight: 700">买家已付款</p>
                  </div>
                  <p>
                    <a
                      href="javascript:void(0);"
                      class="btn_order_details"
                      @click="showOrderDetailBtn(item)"
                      >订单详情</a
                    >
                  </p>
                </td>
                <td class="info_td" valign="middle">
                  <div v-if="item.cancel">
                    <a
                      href="javascript:;"
                      class="delete_order"
                      @click="deleteOrder(item)"
                      >删除</a
                    >
                  </div>
                  <div v-else-if="item.is_pay == false">
                    <a
                      href="javascript:;"
                      class="pay_order"
                      @click="showPayWin(item)"
                      >付款</a
                    >
                    <p style="margin-top: 10px">
                      <a
                        href="javascript:;"
                        class="cancel_order"
                        @click="cancelOrder(item)"
                        >取消订单</a
                      >
                    </p>
                  </div>
                  <div v-else>
                    <a
                      href="javascript:;"
                      class="delete_order"
                      @click="deleteOrder(item)"
                      >删除</a
                    >
                  </div>
                </td>
              </tr>
            </table>
          </div>
          <div class="order_bottom_box">
            <span>收货人信息：{{ item.address.name }}</span>
            ,
            <span>{{ item.address.phone }}</span>
            ,
            <span>{{ item.address.total_address }}</span>
          </div>
        </div>
      </li>
    </ul>
    <div v-else>暂无订单</div>
    <div class="pagination">
      <el-pagination
        small
        background
        layout="prev, pager, next"
        :page-size="20"
        :pager-count="7"
        :total="totalCount"
        :hide-on-single-page="true"
        class="mt-4"
        :current-page="currentPage"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>
<script setup lang="ts">
import { ref, reactive, onBeforeMount, getCurrentInstance, inject } from "vue";
import { ElMessage } from "element-plus";
import OderDetial from "../../components/OrderDetail.vue";

const { proxy } = getCurrentInstance() as any;
const axios: any = inject("axios");

let data: any = reactive({
  orderList: [],
});

let currentPage = ref(1);
let totalCount = ref(0);
let showConfirm = ref(false);
let unpaymentOrder: any = ref({});
let showWin = ref<boolean>(false);
let payNow = ref<boolean>(false);
let orderDetail = ref<boolean>(false);
let activeTrade = ref<string>("0");
let activeCourierNumber = ref<string>("");
let orderItem = ref<any>({});
let payMehtods = ref([
  { payment: "支付宝", flag: false },
  { payment: "微信", flag: false },
]);

onBeforeMount(() => {
  axios.get(proxy.$API.API_ORDER).then((res: any) => {
    totalCount.value = res.count;
    data.orderList = res.results;
  });
});

const handleCurrentChange = (val: number) => {
  axios
    .get(proxy.$API.API_ORDER, {
      params: {
        page: val,
      },
    })
    .then((res: any) => {
      data.orderList = res.results;
      currentPage.value = val;
    });
};

const cancelOrder = (val: any) => {
  axios.put(proxy.$API.API_ORDER + `${val.id}/`).then((res: any) => {
    if (res.code == 200) {
      val.cancel = true;
    }
  });
};

const deleteOrder = (val: any) => {
  axios.delete(proxy.$API.API_ORDER + `${val.id}/`).then((res: any) => {
    axios
      .get(proxy.$API.API_ORDER, {
        params: {
          page: currentPage.value,
        },
      })
      .then((res: any) => {
        data.orderList = res.results;
        currentPage.value = val;
      });
  });
};

const showPayWin = (val: any) => {
  unpaymentOrder.value = val;
  payNow.value = true;
  showConfirm.value = true;
};
const showOrderDetailBtn = (val: any) => {
  activeTrade.value = String(val.items[0].id);
  activeCourierNumber.value = val.items[0].courier_number;
  orderItem.value = val.items;
  orderDetail.value = true;
  showConfirm.value = true;
};
const closeConfirmWin = (val: any) => {
  activeTrade.value = "0";
  activeCourierNumber.value = "";
  showConfirm.value = false;
  payNow.value = false;
  orderDetail.value = false;
};

const selectMehtod = (val: number, flag: boolean) => {
  payMehtods.value.forEach((e: any) => {
    e.flag = false;
  });
  payMehtods.value[val].flag = flag;
};

const pay = () => {
  if (payMehtods.value[0].flag) {
    axios
      .post(proxy.$API.API_ORDER + `${unpaymentOrder.value.id}/`)
      .then((res: any) => {
        if (res.code == 200) {
          window.location.href = res.redirect;
        } else if (res.code == 400) {
          ElMessage({
            type: "error",
            message: res.error,
          });
        }
      });
  } else {
    ElMessage({
      type: "error",
      message: "请选择支付方式",
    });
  }
};

const handleTradeChange = (key: string) => {
  console.log(key);
};
</script>
<style scoped lang="scss">
.order_item {
  margin: 10px;
  border: 1px solid #8c222c;
  border-top: 2px solid #8c222c;
}
.head_info_box {
  font-size: 14px;
  background: #fff1f1;
  padding: 0 10px;
  line-height: 32px;
  border-bottom: 1px solid #8c222c;
}
.w20 {
  width: 20px;
}
.w70 {
  width: 70px;
}
.w_120 {
  width: 120px;
}
.book_name {
  width: 150px;
  font-size: 14px;
  padding-top: 10px;
  padding-left: 5px;
}
.book_img_td {
  position: relative;
  padding: 3px;
  //   top: 3px;
}
.img_box {
  border: 1px solid #e5e5e5;
}
.product_name {
  word-wrap: break-word;
  word-break: break-all;
}
.desc_box_left {
  width: 50%;
}
.s_font {
  font-size: 13px;
}
.right {
  text-align: right;
  padding-right: 10px;
}
.in_tab_tr td {
  border-bottom: 1px dotted #dcdcdc;
}
.info_td {
  text-align: center;
  border-left: 1px dotted #dcdcdc;
  padding-top: 5px;
  padding-bottom: 5px;
}
.delete_order {
  color: #049;
}
.delete_order:hover {
  color: #8c222c;
}
.pay_order {
  background-color: #8c222c;
  color: #fff;
  width: 60px;
  height: 32px;
  line-height: 32px;
  font-size: 14px;
  display: inline-block;
  text-align: center;
  cursor: pointer;
  white-space: nowrap;
  border-radius: 2px;
}
.cancel_order {
  font-size: 14px;

  &:hover {
    color: #8c222c;
  }
}
.btn_order_details {
  margin-top: 14px;
  display: inline-block;
  line-height: 24px;
  text-align: center;
  font-size: 14px;
  color: #049;
}
.order_bottom_box {
  border-top: 1px solid #8c222c;
  padding: 5px 10px;
}
.pagination {
  margin-top: 20px;
}
.mt-4 {
  width: 400px;
  margin: 0 auto;
  justify-content: center;
  :deep(.el-pager li.is-active) {
    background-color: #8c222c !important;
  }
  :deep(.el-pager li:hover) {
    color: #c59b9e !important;
  }
}

:deep(.el-pagination button:hover) {
  color: #c59b9e !important;
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
.overwin {
  position: relative;
  max-width: 900px;
  max-height: 600px;
  padding: 40px 0 30px 0;
  background: #f7f7f6;
  z-index: 1000002;
  overflow-y: scroll;
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
.overwin_title {
  padding-left: 10px;
  padding-bottom: 10px;
  margin: 0px 40px 0px 20px;
  font-size: 24px;
  font-weight: 700;
  line-height: 42px;
  border-bottom: 1px solid #666;
}
.overwin_con {
  margin: 10px 40px 0 20px;
  line-height: 33px;
  font-size: 16px;
  padding-bottom: 20px;
  border-bottom: 1px solid #333;
}
.payment_methods_title {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 10px;
}
.Alipay_btn {
  width: 170px;
  height: 50px;
  text-align: center;
  vertical-align: middle;
  line-height: 50px;
  border: 1px solid #333;
  border-radius: 12px;
  cursor: pointer;
  .payment_text {
    line-height: 50px;
    margin-left: 7px;
    position: relative;
    font-weight: 400;
    top: -7px;
  }
  .ali_icon {
    color: #009fe8;
  }
}
.Alipay_btn:hover {
  border-color: #8c222c;
}
.Alipay_btn:hover {
  border-color: #8c222c;
}
.btn_active {
  border-color: #8c222c;
}
.icon {
  font-size: 36px;
}
.pay_box {
  margin-right: 40px;
  margin-top: 20px;
}
.pay_btn {
  background-color: #8c222c;
  color: #fff;
  width: 140px;
  height: 40px;
  line-height: 40px;
  font-size: 16px;
  display: inline-block;
  text-align: center;
  cursor: pointer;
  white-space: nowrap;
  border-radius: 2px;
}

:deep(.el-collapse-item__wrap),
:deep(.el-collapse-item__header),
:deep(.el-menu) {
  background-color: #f7f7f6;
}
</style>
