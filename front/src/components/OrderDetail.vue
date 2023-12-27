<template>
  <div>
    <div v-if="props.CourierNumber != null">
      <iframe
        src="https://api.kuaidi100.com/tools/map/innerbrqs?mapConfigKey=3cw7Q2Qfsh3ndDgMD6"
        id="mobsf"
        scrolling="no"
        frameborder="0"
        style="width: 100%; height: 300px"
      ></iframe>
      <span class="dialogProcess">
        <el-card class="box-card">
          <div slot="header" class="clearfix">
            <span>运单编号: {{ props.CourierNumber }}</span>
          </div>
          <div>
            <div class="track-rcol">
              <div class="track-list">
                <ul>
                  <div v-for="(item, index) in data.data" :key="index">
                    <!-- 状态 -->
                    <div class="first">
                      <li>
                        <i
                          :class="{
                            'steps-line': index < data.data.length - 1,
                            'steps-no-line': index == data.data.length - 1,
                          }"
                        ></i>
                        <div>
                          <div class="node-icon icon"></div>

                          <span class="title">{{ item.status }}</span>
                        </div>
                        <span class="name">内容:{{ item.context }}</span>
                        <span class="time">{{ item.time }}</span>
                      </li>
                    </div>
                  </div>
                </ul>
              </div>
            </div>
          </div>
        </el-card>
      </span>
    </div>
    <div v-else>
      <span>商品暂未发货</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onBeforeMount, getCurrentInstance, inject } from "vue";
import { ElMessage } from "element-plus";

const { proxy } = getCurrentInstance() as any;
const axios: any = inject("axios");

const data = reactive({
  message: "ok",
  nu: "YT2237659878059",
  ischeck: "1",
  com: "yuantong",
  status: "200",
  data: [
    {
      time: "2022-08-23 14:31:50",
      context: "等待商品发货",
      ftime: "2022-08-23 14:31:50",
      areaCode: null,
      areaName: null,
      status: "代发货",
    },
  ],
  state: "3",
  condition: "H100",
  routeInfo: {
    from: {
      number: "CN440100000000",
      name: "广东,广州市",
    },
    cur: {
      number: "CN330703102000",
      name: "浙江,金华市,金东区,傅村镇",
    },
    to: {
      number: "CN330703102000",
      name: "浙江,金华市,金东区,傅村镇",
    },
  },
  isLoop: false,
  trailUrl:
    "https://api.kuaidi100.com/tools/map/5df2da3f9c318185586333d0f7192648_119.647444,29.079059_6",
  arrivalTime: "2022-08-23 14",
  totalTime: "1天15小时",
  remainTime: "0天0小时",
});

const props = defineProps<{
  id?: number;
  CourierNumber?: string;
}>();

onBeforeMount(() => {
  console.log(props.id, props.CourierNumber);
});
</script>

<style scoped lang="scss">
//css
.dialogProcess {
  .text {
    font-size: 14px;
  }

  .item {
    margin-bottom: 18px;
  }

  .clearfix:before,
  .clearfix:after {
    display: table;
    content: "";
  }

  .clearfix:after {
    clear: both;
  }

  ul li {
    list-style: none;
    font-size: 1rem;
  }

  ul {
    padding-left: 1.5rem;
  }

  // .track-rcol {}

  .track-list ul li {
    position: relative;
    padding: 0px 0px 25px 45px;
  }

  .track-list .node-icon {
    width: 30px;
    height: 30px;
    position: absolute;
    top: 0;
    left: -45px;
  }

  // 圆点
  .track-list .icon {
    width: 30px;
    height: 30px;
    background-color: #efefef;
    border-radius: 20px;
    margin-left: 40upx;
  }

  .track-list li {
    margin-top: 10px;
  }

  .track-list li span {
    position: relative;
    top: 4px;
    display: block;
    // vertical-align: middle;
    margin-bottom: 5px;
    font-size: 14px;
  }

  .track-list li .title {
    font-size: 18px;
    margin-bottom: 10px;
  }

  //线
  .track-list li .steps-line {
    position: absolute;
    top: 2px;
    left: 15px;
    width: 0px;
    height: 100%;
    border-right: 1px solid #999;
  }
}
</style>
