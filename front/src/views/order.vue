<template>
  <div class="content">
    <div class="win-mask" v-show="showWin">
      <div class="addr_win_box">
        <div class="close-btn">
          <a id="loginWinCloseBtn" href="javascript:;" @click="closeWin">
            <span class="iconfont close-icon">&#xe60e;</span>
          </a>
        </div>
        <div class="overwin">
          <createAddr
            @reload-addr="reloadAddr"
            ref="addaddr"
            :id="editAddrId"
          />
        </div>
      </div>
    </div>
    <div class="win-mask" v-show="showConfirm">
      <div class="addr_win_box">
        <div class="close-btn">
          <a id="loginWinCloseBtn" href="javascript:;" @click="closeConfirmWin">
            <span class="iconfont close-icon">&#xe60e;</span>
          </a>
        </div>
        <div class="overwin clearfix">
          <h3 class="overwin_title">付款</h3>
          <div class="overwin_con">
            <div class="payment_info">
              <div>
                <span>代付订单：</span> <span>共 <span>1</span> 笔</span>
              </div>
              <div>
                <span>支付金额：￥{{ totalPrice }}</span>
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
      </div>
    </div>
    <div class="content-header">
      <div class="header-box">
        <Search />
      </div>
    </div>
    <div class="orderlist-box">
      <div class="address_h3"><span class="bold">收货地址</span></div>
      <div class="addr_list" v-if="data.addressList.length">
        <ul>
          <li
            v-for="item in data.addressList"
            class="addr_item_box clearfix"
            :class="selectedAddr == item.id ? 'addr_item_box_active' : ''"
            @mouseenter="showEditBtn(item.id)"
            @mouseleave="editBtnId = 0"
          >
            <div class="addr_checkbox f_left">
              <input
                type="radio"
                name="selected"
                :value="item.id"
                class="addr_item"
                v-model="selectedAddr"
                :id="item.id"
                @click="selectedAddr = item.id"
              />
              <label :for="item.id"></label>
            </div>
            <div class="addr_info f_left">
              <div class="name_box f_left">
                <span class="receiver_name_span f_left">{{ item.name }}</span>
                <span class="phone_span f_left">({{ item.phone }})</span>
              </div>
              <div class="desc_addr f_left">
                <span class="desc_addr_span">{{ item.total_address }}</span>
              </div>
            </div>
            <div class="edit_box f_right">
              <span class="defualt_addr f_left" v-show="item.default"
                >默认地址</span
              >
              <a
                href="javascript:;"
                class="edit_addr"
                @click="editAddr(item)"
                v-if="item.id == editBtnId"
              >
                修改
              </a>
            </div>
          </li>
        </ul>
        <div class="addr_bottom">
          <a href="javascript:;" class="add_addr" @click="showWin = true"
            >+添加收货地址</a
          >
          <a href="user/receive_address" class="manage_addr f_right"
            >管理收货地址</a
          >
        </div>
      </div>
      <div class="addr_create_item" v-else>
        <createAddr @reload-addr="reloadAddr" />
      </div>
      <div class="address_h3"><span class="bold">商品清单</span></div>
      <div class="shop_book_con">
        <div class="shop_name_title"></div>
        <div class="order_con">
          <div class="clearfix order_item" v-for="item in data.booklist">
            <div class="item-img">
              <div class="img-box f_left">
                <a :href="item.image">
                  <el-image
                    style="width: 88px; height: 88px"
                    fit="scale-down"
                    :src="item.image"
                  >
                    <template #error>
                      <div class="image-slot">本书目未收录图片</div>
                    </template>
                  </el-image></a
                >
              </div>
            </div>
            <div class="item_name f_left">
              <a :href="'sbook/' + item.id">{{ item.name }}</a>
            </div>
            <div class="item_user f_left">
              <a :href="'shop/' + item.user.id" class="user_text">{{
                item.user.user_name
              }}</a>
            </div>
            <div class="item_price f_left">
              {{ item.price }}
            </div>
            <div class="item_num f_left">× 1件</div>
            <div class="item_price_all f_right">{{ item.price }}</div>
          </div>
          <div class="clearfix order_item" v-for="item in data.cartlist">
            <div class="item-img">
              <div class="img-box f_left">
                <a :href="proxy.$API.BASE_URL + item.book.image">
                  <el-image
                    style="width: 88px; height: 88px"
                    fit="scale-down"
                    :src="proxy.$API.BASE_URL + item.book.image"
                  >
                    <template #error>
                      <div class="image-slot">本书目未收录图片</div>
                    </template>
                  </el-image></a
                >
              </div>
            </div>
            <div class="item_name f_left">
              <a :href="'sbook/' + item.book.id">{{ item.book.name }}</a>
            </div>
            <div class="item_user f_left">
              <a :href="'shop/' + item.book.dianpu_id" class="user_text">{{
                item.user_name
              }}</a>
            </div>
            <div class="item_price f_left">
              {{ item.book.price }}
            </div>
            <div class="item_num f_left">× 1件</div>
            <div class="item_price_all f_right">{{ item.book.price }}</div>
          </div>
        </div>
      </div>
      <div class="orderlist_bottom clearfix">
        <div class="delivery_box f_right">
          <i class="iconfont delivery_icon">&#xecea;</i>
          <span class="m_r20">运送方式：</span>
          <span class="m_r20">生成订单后请与卖家确认运费</span>
          <span class="m_l100"
            >运费：
            <span class="orange">—</span>
          </span>
        </div>
      </div>
      <div class="shop_summary_box">
        <div>
          <span class="total_text"
            >共计
            <span class="red">{{
              data.booklist.length + data.cartlist.length
            }}</span>
            件商品，应付总金额</span
          >
          <span class="red total_price">{{ totalPrice }}</span>
        </div>
        <div class="submit_order_box">
          <a href="javascript:;" class="submit_order_btn" @click="confirm"
            >确认并提交订单</a
          >
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import createAddr from "@/components/createAddr.vue";
import { regionData, CodeToText } from "element-china-area-data";
import { ElMessage } from "element-plus";
import {
  ref,
  getCurrentInstance,
  reactive,
  onBeforeMount,
  inject,
  computed,
  nextTick,
} from "vue";
import Search from "../components/SearchBox.vue";

let { proxy } = getCurrentInstance() as any;
let axios: any = inject("axios");

let data: any = reactive({
  booklist: [],
  cartlist: [],
  addressList: [],
});

let showWin = ref(false);
let addaddr: any = ref();
let editAddrId = ref(0);
let selectedAddr = ref();
let editBtnId = ref(0);
let showConfirm = ref(false);
const payMehtods = ref([
  { payment: "支付宝", flag: false },
  { payment: "微信", flag: false },
]);

const totalPrice = computed(() => {
  let _sum = 0;
  if (data.booklist.length) {
    return data.booklist[0].price;
  }
  for (let index = 0; index < data.cartlist.length; index++) {
    const element = data.cartlist[index];
    _sum += parseFloat(element.book.price);
  }
  return _sum;
});

onBeforeMount(() => {
  let bookId = proxy.$route.query.bookId;
  let cartIds = proxy.$route.query.cartIds;
  axios.get(proxy.$API.API_ADDRESS).then((res: any) => {
    res.results.forEach((e: any) => {
      if (e.default) {
        selectedAddr.value = e.id;
      }
    });
    data.addressList = res.results;
  });
  if (bookId) {
    axios.get(proxy.$API.API_SINGALBOOK + `${bookId}/`).then((res: any) => {
      data.booklist.push(res);
    });
  }
  if (cartIds) {
    console.log(cartIds instanceof Array);
    let id: any = [];
    if (cartIds instanceof Array) {
      id = cartIds.join("&");
    } else {
      id = cartIds;
    }
    axios
      .get(proxy.$API.API_CART_TO_ORDER_ITEMS, {
        params: {
          id: id,
        },
      })
      .then((res: any) => {
        data.cartlist = res;
      });
  }
});

const reloadAddr = (val: any) => {
  axios.get(proxy.$API.API_ADDRESS).then((res: any) => {
    data.addressList = res.results;
  });
  selectedAddr.value = val.id;
  showWin.value = false;
};

const closeWin = () => {
  showWin.value = false;
  addaddr.value.reloadAddressInform();
};

const editAddr = (val: any) => {
  editAddrId.value = val.id;
  showWin.value = true;
  addaddr.value.initEdit(val);
};

const showEditBtn = (val: number) => {
  editBtnId.value = val;
};

const confirm = () => {
  showConfirm.value = true;
};

const closeConfirmWin = () => {
  showConfirm.value = false;
};

const pay = () => {
  if (payMehtods.value[0].flag) {
    nextTick(() => {
      if (proxy.$route.query.cartIds) {
        let id: any = [];
        if (proxy.$route.query.cartIds instanceof Array) {
          id = proxy.$route.query.cartIds.join("&");
        } else {
          id = proxy.$route.query.cartIds;
        }
        axios
          .post(proxy.$API.API_PAY, {
            price: totalPrice.value,
            cartId: id,
            addr: selectedAddr.value,
          })
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
      }
      if (proxy.$route.query.bookId) {
        axios
          .post(proxy.$API.API_PAY, {
            price: totalPrice.value,
            bookId: proxy.$route.query.bookId,
            addr: selectedAddr.value,
          })
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
      }
    });
  } else {
    ElMessage({
      type: "error",
      message: "请选择支付方式",
    });
  }
};

const selectMehtod = (val: number, flag: boolean) => {
  payMehtods.value.forEach((e: any) => {
    e.flag = false;
  });
  payMehtods.value[val].flag = flag;
};
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
.orderlist-box {
  width: 1000px;
  margin: 0 auto;
}
.address_h3 {
  position: relative;
  font-size: 20px;
  line-height: 40px;
  margin-top: 20px;
}
.shop_name_title {
  line-height: 40px;
  border-bottom: 1px solid #aaa;
  font-size: 12px;
  color: #333;
}
.yonghu:hover {
  color: #8c222c;
}
.order_item {
  border-bottom: 1px solid #e5e5e5;
  padding: 16px 0;
}
.img-box {
  position: relative;
  float: left;
  width: 90px;
  height: 90px;
  line-height: 88px;
  border: 1px solid #e5e5e5;
  text-align: center;
  background-color: #ffffff;
  font-size: 0;
}
.item_name {
  float: left;
  padding-left: 14px;
  width: 400px;
  overflow: hidden;
}
.item_user {
  float: left;
  width: 200px;
  text-align: center;
  margin-left: 14px;
  overflow: hidden;
}
.user_text:hover {
  color: #8c222c;
}
.item_num,
.item_price {
  width: 104px;
  overflow: hidden;
}
.item_price_all {
  width: 80px;
  text-align: right;
  color: #bf7f5f;
  overflow: hidden;
}
.orderlist_bottom {
  padding: 14px 0;
}
.delivery_box {
  font-size: 12px;
  line-height: 24px;
}
.orange {
  color: #bf7f5f;
}
.delivery_icon {
  font-size: 22px;
  position: relative;
  bottom: -4px;
  margin-right: 10px;
}
.shop_summary_box {
  text-align: right;
  border-top: 2px solid #8c222c;
  margin-top: 30px;
  padding-top: 26px;
  font-size: 14px;
  .red {
    color: #8c222c;
  }
}
.total_text {
  font-size: 16px;
}
.total_price {
  font-size: 26px;
  padding: 0 4px;
}
.submit_order_box,
.pay_box {
  margin-top: 20px;
}
.pay_box {
  margin-right: 40px;
}
.submit_order_btn {
  background-color: #8c222c;
  color: #fff;
  width: 180px;
  height: 40px;
  line-height: 40px;
  font-size: 16px;
  display: inline-block;
  text-align: center;
  cursor: pointer;
  white-space: nowrap;
  border-radius: 2px;
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
.addr_item_box {
  height: 50px;
  color: #333;
  // background: #f8f7f3;
  padding: 10px 20px 10px 0;
  .addr_checkbox {
    width: 54px;
    text-align: center;
    margin-left: 15px;
    padding: 4px;
  }
  .addr_info,
  .edit_box {
    line-height: 32px;
    font-size: 12px;
  }
  .name_box {
    width: 190px;
    margin-right: 20px;
  }
  .receiver_name_span {
    max-width: 80px;
    display: inline-block;
    overflow: hidden;
    white-space: nowrap;
    text-overflow: ellipsis;
  }
  .phone_span {
    width: 110px;
    display: inline-block;
    overflow: hidden;
    vertical-align: top;
  }
  .desc_addr {
    width: 550px;
  }
  .desc_addr_span {
    width: 500px;
    display: inline-block;
    overflow: hidden;
  }
  .edit_box {
    width: 120px;
    text-align: right;
  }
  .defualt_addr {
    color: #999;
    margin-right: 10px;
  }
  .edit_addr {
    width: 100px;
    color: #666 !important;
  }
  .edit_addr:hover {
    color: #8c222c !important;
  }
}
.addr_item_box_active {
  background: #f8f7f3;
}
.addr_bottom {
  margin-top: 10px;
  padding-left: 54px;

  .add_addr {
    color: #365899 !important;
    font-size: 12px;
  }
  .add_addr:hover {
    color: #8c222c !important;
  }
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
.overwin {
  position: relative;
  width: auto;
  height: auto;
  padding: 40px 0 30px 0;
  background: #f7f7f6;
  z-index: 1000002;
  overflow: visible;
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
input[type="radio"] + label::before {
  content: "\a0"; /*不换行空格*/
  display: inline-block;
  vertical-align: middle;
  font-size: 14px;
  width: 1em;
  height: 1em;
  margin-right: 0.4em;
  border-radius: 50%;
  border: 1px solid #8c222c;
  text-indent: 0.15em;
}
input[type="radio"]:checked + label::before {
  background-color: #8c222c;
  background-clip: content-box;
  padding: 0.2em;
}
input[type="radio"] {
  position: absolute;
  clip: rect(0, 0, 0, 0);
}
.manage_addr {
  font-size: 12px;
}
.manage_addr:hover {
  color: #8c222c;
}
.overwin_title {
  padding-left: 10px;
  padding-bottom: 10px;
  margin: 0px 40px 0px 10px;
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
.btn_active {
  border-color: #8c222c;
}
.icon {
  font-size: 36px;
}
</style>
