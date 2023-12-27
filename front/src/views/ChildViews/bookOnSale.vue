<template>
  <div class="book_on_sale_con">
    <div>
      <el-image-viewer
        v-if="imageViewerFlag"
        @close="closeImageViewer"
        :url-list="[imageViewerImage]"
      />
      <div class="win-mask" v-show="showWin">
        <div class="win_box">
          <div class="close-btn">
            <a
              id="loginWinCloseBtn"
              href="javascript:;"
              @click="showWin = false"
            >
              <span class="iconfont close-icon">&#xe60e;</span>
            </a>
          </div>
          <div class="overwin clearfix">
            <h3 class="title pl_30">修改书籍信息</h3>
            <el-form
              :label-position="'right'"
              label-width="100px"
              :model="reEditBookInfo"
              :inline="true"
            >
              <el-form-item label="书名" style="width: 100%">
                <el-input v-model="reEditBookInfo.name" style="width: 30%" />
              </el-form-item>
              <el-form-item label="价格" style="width: 100%">
                <el-input-number
                  v-model="reEditBookInfo.price"
                  :precision="2"
                  :step="0.1"
                  :max="999"
                />
              </el-form-item>
              <el-form-item label="是否出售" style="width: 25%">
                <el-switch
                  disabled
                  v-model="reEditBookInfo.sold"
                  class="mt-2"
                  inline-prompt
                  :active-icon="Check"
                  :inactive-icon="Close"
                />
              </el-form-item>
              <el-form-item label="是否退单" style="width: 25%">
                <el-switch
                  disabled
                  v-model="reEditBookInfo.returns"
                  class="mt-2"
                  inline-prompt
                  :active-icon="Check"
                  :inactive-icon="Close"
                />
              </el-form-item>
              <el-form-item label="是否发货" style="width: 25%">
                <el-switch
                  v-model="reEditBookInfo.transit"
                  class="mt-2"
                  disabled
                  inline-prompt
                  :active-icon="Check"
                  :inactive-icon="Close"
                />
              </el-form-item>
              <el-form-item label="图片信息" style="width: 100%">
                <div class="clearfix">
                  <div class="book_img">
                    <img
                      class="f_left"
                      :src="reEditBookInfo.image"
                      :height="200"
                      @click.native="uploadSecondHandBookImage()"
                      v-if="reEditBookInfo.image"
                    />
                    <div
                      v-else
                      class="no_image"
                      @click.native="uploadSecondHandBookImage()"
                    >
                      暂无图片
                    </div>
                  </div>
                </div>
              </el-form-item>
              <el-form-item label="是否下架" style="width: 25%">
                <el-switch
                  v-model="reEditBookInfo.remove"
                  class="mt-2"
                  inline-prompt
                  style="
                    --el-switch-on-color: #ff4949;
                    --el-switch-off-color: #13ce66;
                  "
                  :active-icon="Check"
                  :inactive-icon="Close"
                />
              </el-form-item>
              <div class="submit_box">
                <input
                  class="submit_btn"
                  type="button"
                  value="保存修改"
                  @click="saveSBookInfo"
                />
              </div>
            </el-form>
          </div>
        </div>
      </div>
      <el-table :data="data.books" height="450" style="width: 100%">
        <el-table-column fixed prop="name" label="书名" width="170" />
        <el-table-column label="图片" width="120">
          <template #default="scope">
            <el-button
              link
              type="primary"
              size="default"
              @click="showImageViewer(scope.row.image)"
              >查看图片</el-button
            >
          </template>
        </el-table-column>
        <el-table-column label="发布时间" prop="ptime" sortable width="180">
          <template #default="scope">
            <span>{{ scope.row.ptime.replace("T", " ").split(".")[0] }}</span>
          </template>
        </el-table-column>
        <el-table-column label="价格" prop="price" sortable width="90">
          <template #default="scope">
            <span style="font-weight: 700">{{ scope.row.price }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="是否售出"
          prop="sold"
          width="120"
          :align="'center'"
          :filter-method="filterSold"
          :filters="[
            { text: '是', value: true },
            { text: '否', value: false },
          ]"
        >
          <template #default="scope">
            <span>{{ scope.row.sold ? "是" : "否" }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="是否运输"
          prop="transit"
          width="120"
          :align="'center'"
          :filter-method="filterTransit"
          :filters="[
            { text: '是', value: true },
            { text: '否', value: false },
          ]"
        >
          <template #default="scope">
            <span>{{ scope.row.transit ? "是" : "否" }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="是否退单"
          prop="returns"
          width="120"
          :align="'center'"
          :filter-method="filterReturns"
          :filters="[
            { text: '是', value: true },
            { text: '否', value: false },
          ]"
        >
          <template #default="scope">
            <span>{{ scope.row.returns ? "是" : "否" }}</span>
          </template>
        </el-table-column>
        <el-table-column
          label="是否下架"
          prop="remove"
          width="120"
          :align="'center'"
          :filter-method="filterRemove"
          :filters="[
            { text: '是', value: true },
            { text: '否', value: false },
          ]"
        >
          <template #default="scope">
            <span>{{ scope.row.remove ? "是" : "否" }}</span>
          </template>
        </el-table-column>
        <el-table-column fixed="right" label="操作" width="120">
          <template #default="scope">
            <el-button
              link
              type="primary"
              size="default"
              @click="reEditBook(scope.row)"
              >编辑</el-button
            >
            <el-popover
              placement="top"
              :width="160"
              :visible="scope.$index == showPopper"
            >
              <p>确定删除这条书籍信息吗？</p>
              <div style="text-align: right; margin: 0">
                <el-button size="small" text @click="showPopper = -1"
                  >取消</el-button
                >
                <el-button
                  size="small"
                  type="danger"
                  @click="confirmDel(scope.row.id)"
                  >确定删除</el-button
                >
              </div>
              <template #reference>
                <el-button
                  link
                  type="primary"
                  size="default"
                  @click="showPopper = scope.$index"
                  >删除</el-button
                >
              </template>
            </el-popover>
          </template>
        </el-table-column>
      </el-table>
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
import { useUserStore } from "@/stores/store";
import { storeToRefs } from "pinia";
import { Check, Close } from "@element-plus/icons-vue";
import { ElMessage, ElImageViewer } from "element-plus";

const store = useUserStore();
const userInfoSotre = storeToRefs(store);

let { proxy } = getCurrentInstance() as any;
let axios: any = inject("axios");

let data: any = reactive({
  books: [],
});

let reEditBookInfo = ref<any>({});
let showPopper = ref<number>(-1);
let showWin = ref(false);
let imageViewerFlag = ref<boolean>(false);
let imageViewerImage = ref<string>("");

onBeforeMount(() => {
  axios.get(proxy.$API.API_SECONDHAND_BOOK).then((res: any) => {
    // console.log(res.data);
    if (res.code == 200) {
      data.books = res.data;
    } else {
      ElMessage({
        type: "error",
        message: res.error,
      });
      userInfoSotre.notLogin.value = true;
    }
  });
});

// 打开书籍图片
const showImageViewer = (val: string) => {
  imageViewerImage.value = val;
  imageViewerFlag.value = true;
  console.log(imageViewerImage.value);
};
// 关闭书籍图片
const closeImageViewer = () => {
  imageViewerFlag.value = false;
  imageViewerImage.value = "";
};

// 重新编辑书籍信息
const reEditBook = (val: any) => {
  if (val.sold || val.transit || val.returns) {
    ElMessage({
      type: "error",
      message: "此书籍当前无法修改信息",
    });
    return;
  }
  showWin.value = true;
  reEditBookInfo.value = val;
};

// 确认删除书籍
const confirmDel = (val: any) => {
  axios
    .delete(proxy.$API.API_SECONDHAND_BOOK, {
      params: {
        bid: val,
      },
    })
    .then(() => {
      let did = data.books.findIndex((item: any) => {
        if (item.id == val) {
          return true;
        }
      });
      showPopper.value = -1;
      data.books.splice(did, 1);
    });
};

// 更新书籍图片
const uploadSecondHandBookImage = () => {
  //创建input
  const upload = document.createElement("input");
  //设置type为file
  upload.type = "file";
  //类型
  upload.accept = "image/png, image/jpeg";
  //添加onchange事件
  upload.onchange = (e: any) => {
    const file = e.target.files[0];
    reEditBookInfo.value.image = URL.createObjectURL(file);
    reEditBookInfo.value.imgFile = file;
    return true;
  };
  //模拟点击
  upload.click();
};

// 实现筛选
const filterSold = (value: any, row: any) => {
  return row.sold === value;
};
const filterTransit = (value: any, row: any) => {
  return row.transit === value;
};
const filterReturns = (value: any, row: any) => {
  return row.returns === value;
};
const filterRemove = (value: any, row: any) => {
  return row.remove === value;
};

// 保存修改信息
const saveSBookInfo = () => {
  console.log(reEditBookInfo);
  const formdata = new FormData();
  if (reEditBookInfo.value.imgFile != undefined) {
    formdata.append("imgFile", reEditBookInfo.value.imgFile);
  } else {
    formdata.append("imgFile", "");
  }

  Object.keys(reEditBookInfo.value).forEach((e: any) => {
    formdata.append(e, reEditBookInfo.value[e]);
  });
  axios.put(proxy.$API.API_SECONDHAND_BOOK, formdata).then((res: any) => {
    if (res.code == 200) {
      ElMessage({
        message: res.msg,
        type: "success",
      });
      showWin.value = false;
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
.title {
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 20px;
}
.pl_30 {
  padding-left: 30px;
}

.book_img {
  cursor: pointer;
  display: inline-block;
  border: 1px solid #e5e5e5;
  &::after {
    content: "点击修改图片";
    width: 100%;
    position: absolute;
    background: #000000;
    color: #ffffff;
    bottom: 0px;
    opacity: 0.6;
    font-size: 14px;
    text-align: center;
    left: 0px;
  }
}
.submit_btn {
  margin-left: 95px;
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
