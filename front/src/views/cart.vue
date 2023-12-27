<template>
  <div class="content-box">
    <div class="content-header">
      <div class="header-box">
        <Search />
      </div>
    </div>
    <div class="cart-con bg-gray" v-show="showCartCon">
      <div>
        <div class="cart" v-if="data.cartCount" ref="cart">
          <div class="cart-filter-bar">
            <span class="cart-title">购物车（全部{{ data.cartCount }}）</span>
          </div>
          <div class="cart-table-th clearfix">
            <div class="cart-checkbox-th f_left">
              <div class="cart-checkbox" @click="selectAll(!selectAllKey)">
                <i class="iconfont icon-active bold-icon" v-if="selectAllKey"
                  >&#xe608;</i
                >
                <i class="iconfont bold-icon" v-else>&#xe8ed;</i>

                <span class="cart-checkbox-text">全选</span>
              </div>
            </div>
            <div class="cart-info-th f_left">
              <span class="cart-info-th-text">商品信息</span>
            </div>
            <div class="inner-th f_left"></div>
            <div class="only-price-th f_left">
              <span class="only-price-th-text">单价</span>
            </div>
            <div class="count-th f_left">
              <span class="number-th-text">数量</span>
            </div>
            <div class="item-price-th f_left">
              <span class="item-price-th-text">金额</span>
            </div>
            <div class="action-th f_left">
              <span class="action-th-text">操作</span>
            </div>
          </div>
          <div class="orderList">
            <div class="dianpu" v-for="(item, index) in data.cartData">
              <div class="dianpu-body">
                <div class="item-header">
                  <div class="shop-info">
                    <div
                      class="cart-checkbox"
                      @click="selectdianpu(index, !item.selected)"
                    >
                      <i
                        class="iconfont icon-active bold-icon"
                        v-if="item.selected"
                        >&#xe608;</i
                      >
                      <i class="iconfont bold-icon" v-else>&#xe8ed;</i>
                    </div>
                    <span class="yonghu">用户：</span>
                    <span>{{ item[0].user_name }}</span>
                  </div>
                </div>
              </div>
              <div class="order-body" v-for="d in item">
                <CartCard
                  :data="d"
                  @delete-order="deleteItem"
                  @select-item="selectItem"
                ></CartCard>
              </div>
            </div>
          </div>
          <div :class="fixBottomFlag ? 'fix_bottom' : 'float-bar'">
            <div class="select-all">
              <div class="cart-checkbox" @click="selectAll(!selectAllKey)">
                <i class="iconfont icon-active bold-icon" v-if="selectAllKey"
                  >&#xe608;</i
                >
                <i class="iconfont bold-icon" v-else>&#xe8ed;</i>

                <span class="cart-checkbox-text">全选</span>
              </div>
              <!-- <div @click="selectAll(selectAllKey)">
                <i class="iconfont icon-active bold-icon" v-if="selectAllKey"
                  >&#xe608;</i
                >
                <i class="iconfont bold-icon" v-else>&#xe8ed;</i>

                <span style="margin-left: 10px">全选</span>
              </div> -->
            </div>
            <div class="operations">
              <a
                href="javascript:;"
                class="select-delete"
                @click="selectedDelete()"
                >删除</a
              >
            </div>
            <div class="float-bar-right f_right">
              <div class="price-sum f_left">
                <span>合计（不含运费）：</span>
                <span class="total-price">￥{{ totalPrice }}</span>
              </div>
              <div class="btn-area f_left">
                <a
                  href="javascript:void(0);"
                  class="submit-btn"
                  :class="canSubmit ? 'submit-btn-able' : 'submit-btn-disable'"
                  @click="submitFunc()"
                >
                  <span>结&nbsp;算</span>
                </a>
              </div>
            </div>
          </div>
        </div>
        <div class="cart" v-else>
          <div class="no-goods-con">
            <img
              src="@/assets/image/noGoods.svg"
              alt=""
              width="400"
              class="no-goods"
            />
            <div class="no-goods-text">
              <span>您的购物车是空的，您可以去逛逛</span>
              <div class="top-margin"><a class="btn" href="/">去逛逛</a></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup lang="ts">
import Search from "../components/SearchBox.vue";
import { ElMessage, valueEquals } from "element-plus";
import {
  onBeforeMount,
  ref,
  reactive,
  getCurrentInstance,
  inject,
  computed,
  onMounted,
  onUnmounted,
  watch,
  nextTick,
  onUpdated,
} from "vue";
import CartCard from "../components/CartCard.vue";

const { proxy } = getCurrentInstance() as any;
const axios: any = inject("axios");

const data: any = reactive({
  originData: [],
  cartCount: 0,
  cartData: [],
});

let selectAllKey = ref(false);
let showCartCon = ref(false);
let winHight = ref(0);
let fixBottomFlag = ref(false);

const totalPrice = computed(() => {
  let _sum = 0;
  let _data = data.originData;
  _data.forEach((e: any) => {
    if (e.selected) {
      _sum += parseFloat(e.book.price);
    }
  });
  return _sum;
});

const canSubmit = computed(() => {
  let _data = data.originData;
  for (let index = 0; index < _data.length; index++) {
    const element = _data[index];
    if (element.selected) {
      return true;
    }
  }
  return false;
});

onBeforeMount(() => {
  axios.get(proxy.$API.API_CART).then((res: any) => {
    if (res.count) {
      data.originData = res.results;
      data.cartCount = res.count;
      initCartData(false);
    }
    showCartCon.value = true;
  });
  winHight.value =
    window.innerHeight ||
    document.documentElement.clientHeight ||
    document.body.clientHeight;
});

onMounted(() => {
  window.addEventListener("scroll", handleScroll, true);
});
onUnmounted(() => {
  window.removeEventListener("scroll", handleScroll, true);
});
onUpdated(() => {
  if (document.body.clientHeight == winHight.value) {
    fixBottomFlag.value = false;
  }
});

// 防抖
const debounce = (fn: Promise<any>, t: number) => {
  const delay = t || 200;
  let timer: any;
  return () => {
    if (timer) {
      clearTimeout(timer);
    }
    timer = setTimeout(() => {
      timer = null;
      fn;
    }, delay);
  };
};

const handleScroll = () => {
  nextTick(() => {
    let floatBarHeight = 52;
    let afterMountedWinHeight = document.body.clientHeight - floatBarHeight;
    const top =
      document.body.scrollTop ||
      document.documentElement.scrollTop ||
      window.pageYOffset;
    if (winHight.value + top >= afterMountedWinHeight) {
      fixBottomFlag.value = false;
    } else {
      fixBottomFlag.value = true;
    }
    console.log(top);
  });
};

const initCartData = (val: boolean) => {
  let _ = proxy.$lodash.groupBy(data.originData, "dianpu_id");
  Object.keys(_).forEach((e: any) => {
    _[e].selected = val;
  });
  data.cartData = _;
};

const reloadCartData = () => {
  // 重载cartData
  let _ = proxy.$lodash.groupBy(data.originData, "dianpu_id");
  Object.keys(_).forEach((e: any) => {
    _[e].forEach((element: any) => {
      if (!element.selected) {
        _[e].selected = false;
      }
    });
    // console.log(Object.keys(_[e]).indexOf("selected"));
    if (Object.keys(_[e]).indexOf("selected") == -1) {
      _[e].selected = true;
    }
  });
  data.cartData = _;
};

const checkSelectedAll = () => {
  // 判断是否全选
  let _data = data.originData;
  for (let index = 0; index < _data.length; index++) {
    const element = _data[index];
    if (!element.selected) {
      selectAllKey.value = false;
      return;
    }
  }
  selectAllKey.value = true;
};

const selectAll = (val: boolean) => {
  selectAllKey.value = val;
  data.originData.forEach((e: any) => {
    e.selected = val;
  });
  initCartData(val);
  // console.log(totalPrice);
};

const deleteItem = (val: number) => {
  axios.delete(proxy.$API.API_CART + `${val}/`).then((res: any) => {
    if (res.code == 200) {
      ElMessage({
        message: res.msg,
        type: "success",
      });
      data.originData = data.originData.filter((e: any) => {
        if (e.id != val) {
          return e;
        }
      });
      reloadCartData();
      data.cartCount = data.originData.length;
    }
  });
};

const selectItem = (val: number, flag: boolean) => {
  let index = proxy.$lodash.findIndex(data.originData, ["id", val]);
  data.originData[index].selected = flag;
  checkSelectedAll();
  reloadCartData();
};

const selectdianpu = (val: number, flag: boolean) => {
  data.originData.forEach((e: any) => {
    if (e.dianpu_id == val) {
      e.selected = flag;
    }
  });
  // data.cartData[val].selected = flag;
  checkSelectedAll();
  reloadCartData();
};

const selectedDelete = () => {
  let _selected: any = [];
  data.originData.forEach((e: any) => {
    if (e.selected) {
      _selected.push(e.id);
    }
  });
  axios
    .delete(proxy.$API.API_CART, {
      data: _selected,
    })
    .then((res: any) => {
      if (res.code == 200) {
        ElMessage({
          type: "success",
          message: res.msg,
        });
        data.originData = data.originData.filter((e: any) => {
          // 判断书本是存在于被删除的列表里，
          // _selected.inedxOf(e.id)函数中返回了-1就是此书没被删除
          if (_selected.indexOf(e.id) == -1) {
            return e;
          }
        });
        reloadCartData();
        data.cartCount = data.originData.length;
      } else {
        ElMessage({
          type: "error",
          message: res.detail,
        });
      }
    });
};

const submitFunc = () => {
  let Ids: any = [];
  let secondHandBook = data.originData.filter((e: any) => {
    return e.selected;
  });
  secondHandBook.forEach((e: any) => {
    Ids.push(e.id);
  });
  proxy.$router.push({
    name: "easyBuy",
    query: { cartIds: Ids },
  });
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
.cart-con {
  width: 100%;
  padding-top: 30px;
  min-height: 700px;
}
.cart {
  min-height: 600px;
  margin: 0 auto;
  width: 1000px;
  background-color: #fff;
  -webkit-border-radius: 24px;
  -moz-border-radius: 24px;
  -ms-border-radius: 24px;
  border-radius: 24px;
  // overflow: hidden;
}
.cart-filter-bar {
  overflow: hidden;
  font-size: 12px;
  position: relative;
  height: 72px;
  padding: 0 18px;
  border-bottom: 1px solid #e6e6e6;
}
.cart-title {
  font: 12px/1.5 tahoma, arial, "Hiragino Sans GB", "\5b8b\4f53", sans-serif;
  overflow: hidden;
  color: #000;
  font-size: 18px;
  font-weight: 600;
  height: 72px;
  line-height: 72px;
}
.cart-table-th {
  padding: 0 22px;
  overflow: hidden;
  height: 50px;
  line-height: 50px;
  color: #3c3c3c;
}
.cart-checkbox-th {
  width: 140px;
}
.icon-active {
  color: #a74650;
}
.bold-icon {
  font-weight: 600;
}
.select-all {
  float: left;
  width: 76px;
  height: 72px;
  line-height: 72px;
  padding-left: 5px;
  font-size: 13px;
  cursor: pointer;
}
.cart-checkbox {
  display: inline-block;
  padding: 0px 8px;
  cursor: pointer;
}
.cart-checkbox-text {
  padding-left: 8px;
  width: 15px;
  height: 15px;
  font-weight: 700 !important;
  overflow: hidden;
}
.cart-info-th-text,
.only-price-th-text,
.number-th-text,
.item-price-th-text,
.action-th-text {
  font-weight: 700;
}
.cart-info-th {
  width: 280px;
}
.inner-th {
  width: 100px;
  height: 50px;
}
.only-price-th {
  width: 120px;
}
.count-th {
  width: 104px;
}
.item-price-th {
  width: 100px;
}
.action-th {
  width: 100px;
}
.shop-info {
  line-height: 38px;
  padding-left: 15px;
  font-size: 13px;
  color: #333;
}
.yonghu {
  font-weight: 600 !important;
}
.order-body {
  padding: 5px 0 20px 0;
}
.float-bar {
  height: 72px;
  overflow: hidden;
  padding: 0 24px;
  position: absolute;
  bottom: 0px;
  width: 100%;
}
.fix_bottom {
  position: fixed;
  bottom: 0;
  left: 0;
  width: 1000px;
  right: 0;
  margin: 0 auto;
  background-color: #fff;
  border-radius: 24px;
  z-index: 12;
  padding: 0 24px;
}
.operations {
  float: left;
  line-height: 72px;
  height: 72px;
  font-size: 13px;
}
.select-delete {
  margin-left: 25px;
  float: left;
  position: relative;
  bottom: -1px;
}
.float-bar-right {
  line-height: 72px;
  height: 72px;
  z-index: 4;
  padding-left: 20px;
}
.total-price {
  position: relative;
  bottom: -2px;
  font-weight: 700;
  font-size: 22px;
  color: #f40;
  padding: 0px 4px 0 10px;
}
.submit-btn {
  text-align: center;
  display: inline-block;
  width: 74px;
  height: 42px;
  line-height: 42px;
  color: #fff;
  margin-left: 20px;
  border-radius: 21px;
  font-size: 16px;
  text-decoration: none;
  cursor: pointer;
}
.submit-btn-disable {
  background: #b0b0b0;
}
.submit-btn-able {
  background: #ff5000;
}
.no-goods {
  color: #f40;
  margin: 0px auto;
  display: block;
}
.no-goods-con {
  height: 600px;
  padding: 50px 0px 50px 0px;
}
.no-goods-text {
  position: relative;
  top: -60px;
  span {
    font-weight: 400;
    font-size: 16px;
    color: #666;
    margin: 20px 0;
  }
  text-align: center;
}
.btn {
  display: inline-block;
  width: 88px;
  height: 32px;
  background: #b8333c;
  border-radius: 2px;
  font-weight: 400;
  font-size: 14px;
  color: #fff;
  text-align: center;
  line-height: 32px;
  vertical-align: middle;
  cursor: pointer;
}
.top-margin {
  margin-top: 20px;
}
.orderList {
  padding-bottom: 62px;
}
</style>
