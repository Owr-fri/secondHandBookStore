<template>
  <div class="sell_book_con">
    <div class="steps_con">
      <el-steps
        :active="elStepsActiveId"
        finish-status="success"
        simple
        style="margin-top: 20px"
      >
        <el-step title="编辑原图书" />
        <el-step title="编辑二手图书" />
        <el-step title="发售成功" />
      </el-steps>
    </div>
    <div class="select_book_con" v-if="!editSecondHandBook && !showSuccessPage">
      <div class="clearfix">
        <h3>选择原图书</h3>
        <div class="select">
          <el-select
            v-model="selectedBook"
            filterable
            remote
            reserve-keyword
            placeholder="请输入书名"
            remote-show-suffix
            :remote-method="remoteMethod"
            value-key="id"
            @change="handleSelectChange"
          >
            <el-option
              v-for="item in options"
              :label="item.name"
              :value="item"
              :key="item.id"
            />
          </el-select>
        </div>
        <div class="f_left add_new_book_con" @click="addBook">新增图书</div>
      </div>
      <div class="book_info_form_con clearfix">
        <el-collapse-transition>
          <div v-if="showEditCon">
            <h3>编辑原图书信息</h3>
            <div class="book_info_form">
              <el-form
                :model="selectedBook"
                :label-position="'left'"
                label-width="70px"
                :inline="true"
              >
                <el-form-item label="书名" style="width: 100%">
                  <el-input v-model="selectedBook.name" style="width: 30%" />
                </el-form-item>
                <el-form-item label="isbn" style="width: 100%">
                  <el-input v-model="selectedBook.isbn" style="width: 30%" />
                </el-form-item>
                <el-form-item label="分类" style="width: 100%">
                  <el-select
                    v-model="selectedCategory"
                    filterable
                    remote
                    allow-create
                    default-first-option
                    reserve-keyword
                    placeholder="选择分类"
                    remote-show-suffix
                    :remote-method="remoteGetCategoryOptions"
                    value-key="id"
                  >
                    <el-option
                      v-for="item in categoryOptions"
                      :label="item.name"
                      :value="item"
                      :key="item.id"
                    />
                  </el-select>
                </el-form-item>
                <el-form-item label="作者" style="width: 40%">
                  <el-input v-model="selectedBook.author" />
                </el-form-item>
                <el-form-item label="译者" style="width: 40%">
                  <el-input v-model="selectedBook.translator" />
                </el-form-item>
                <el-form-item label="出版社" style="width: 50%">
                  <el-input v-model="selectedBook.press" />
                </el-form-item>
                <el-form-item label="版本号" style="width: 40%">
                  <el-input-number
                    v-model="selectedBook.revision"
                    :min="0"
                    :max="20"
                    @change="changeRevison"
                  />
                </el-form-item>
                <el-form-item label="出版日期" style="width: 40%">
                  <el-date-picker
                    v-model="selectedBook.published_date"
                    value-format="YYYY-MM-01"
                    type="month"
                    placeholder="请选择日期"
                  />
                </el-form-item>
                <el-form-item label="页数" style="width: 30%">
                  <el-input-number
                    v-model="selectedBook.page_numbers"
                    :min="1"
                    :max="9999"
                    @change="changePageNumbers"
                  />
                </el-form-item>
                <el-form-item label="图片" style="width: 100%">
                  <div class="clearfix">
                    <div class="book_img">
                      <img
                        class="f_left"
                        :src="selectedBook.image"
                        :height="200"
                        @click.native="upStart"
                        v-if="selectedBook.image"
                      />
                      <div v-else class="no_image" @click.native="upStart">
                        暂无图片
                      </div>
                    </div>
                  </div>
                </el-form-item>
                <el-form-item label="作者简介" style="width: 100%">
                  <el-input
                    v-model="selectedBook.author_brief"
                    :rows="4"
                    type="textarea"
                    placeholder="请输入"
                  />
                </el-form-item>

                <el-form-item label="图书简介" style="width: 100%">
                  <el-input
                    v-model="selectedBook.describe"
                    :rows="4"
                    type="textarea"
                    placeholder="请输入"
                  />
                </el-form-item>
                <el-form-item label="图书原价" style="width: 30%">
                  <el-input-number
                    v-model="selectedBook.original_price"
                    :precision="2"
                    :step="0.1"
                    :max="999"
                /></el-form-item>
              </el-form>
            </div>
            <div class="submit-box">
              <input
                v-if="addBookTag"
                class="submit-btn"
                type="button"
                value="新增"
                @click="addBookInfo()"
              />
              <input
                v-else
                class="submit-btn"
                type="button"
                value="保存"
                @click="saveBookInfo()"
              />
            </div>
            <div class="reset-box">
              <input
                class="reset-btn"
                type="button"
                value="重置"
                @click="resetBookInfo()"
              />
            </div>
          </div>
        </el-collapse-transition>
      </div>
    </div>
    <div
      v-else-if="editSecondHandBook && !showSuccessPage"
      class="edit_second_hand_book_con"
    >
      <div class="clearfix">
        <h3>编辑二手图书信息</h3>
        <div class="edit_second_book_form_con clearfix">
          <el-form
            :model="secondHandBookInfo"
            :label-position="'left'"
            label-width="70px"
            :inline="true"
          >
            <el-form-item label="书籍名称" style="width: 40%">
              <el-input v-model="secondHandBookInfo.name" />
            </el-form-item>
            <el-form-item label="图片信息" style="width: 100%">
              <div class="clearfix">
                <div class="book_img">
                  <img
                    class="f_left"
                    :src="secondHandBookInfo.image"
                    :height="200"
                    @click.native="uploadSecondHandBookImage()"
                    v-if="secondHandBookInfo.image"
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
            <el-form-item label="图书二手价" style="width: 30%">
              <el-input-number
                v-model="secondHandBookInfo.price"
                :precision="2"
                :step="0.1"
                :max="999"
            /></el-form-item>
          </el-form>
        </div>
        <div class="submit-box">
          <input
            class="submit-btn"
            type="button"
            value="保存"
            @click="saveSecondHandBookInfo()"
          />
        </div>
        <div class="back-box">
          <input
            class="back-btn"
            type="button"
            value="返回"
            @click="backBookInfo()"
          />
        </div>
      </div>
    </div>
    <div v-else>发售成功！</div>
  </div>
</template>
<script setup lang="ts">
import { useUserStore } from "@/stores/store";
import { storeToRefs } from "pinia";
import { ElMessage } from "element-plus";
import { forEach } from "lodash";
import { ref, inject, reactive, getCurrentInstance, watch } from "vue";

const { proxy } = getCurrentInstance() as any;
const axios: any = inject("axios");

let elStepsActiveId = ref(0);

const store = useUserStore();
const userInfoSotre = storeToRefs(store);

let options: any = ref({});
let categoryOptions: any = ref({});
let selectedBook = ref<any>({});
let selectedCategory = ref<any>({});
let showEditCon = ref<boolean>(false);
let changeImg = ref<any>("");
let addBookTag = ref<boolean>(false);
let editSecondHandBook = ref<boolean>(false);
let secondHandBookInfo = ref<any>({});
let secondHandBookImg = ref<any>("");
let showSuccessPage = ref<boolean>(false);

const remoteMethod = (query: string) => {
  // 如果query为空就不进行查询操作
  if (query == "") {
    return;
  }
  axios
    .get(proxy.$API.API_SEARCH_BY_NAME, {
      params: {
        key: query,
      },
    })
    .then((res: any) => {
      options.value = res;
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
// 上传二手书图片
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
    secondHandBookInfo.value.image = URL.createObjectURL(file);
    secondHandBookImg.value = file;
    return true;
  };
  //模拟点击
  upload.click();
};

const uploadFile = (e: any) => {
  const file = e.target.files[0];
  selectedBook.value.image = URL.createObjectURL(file);
  changeImg.value = file;
};

const changeRevison = (val: any) => {
  selectedBook.value.revision = val;
};

const changePageNumbers = (val: any) => {
  selectedBook.value.page_numbers = val;
};
// 当选择的书籍切换时响应此函数
const handleSelectChange = (val: any) => {
  showEditCon.value = true;
  addBookTag.value = false;
  categoryOptions.value = [
    {
      name: val.category_name,
      id: val.category,
    },
  ];
  selectedCategory.value = {
    name: val.category_name,
    id: val.category,
  };
};

const remoteGetCategoryOptions = (query: string) => {
  if (query == "") {
    return;
  }
  axios
    .get(proxy.$API.API_SEARCH_CATEGORY, {
      params: {
        key: query,
      },
    })
    .then((res: any) => {
      categoryOptions.value = res;
    });
};
// 保存书籍信息
const saveBookInfo = () => {
  // 向formdata提交数据
  const formdata = new FormData();
  formdata.append("imgFile", changeImg.value);
  Object.keys(selectedBook.value).forEach((e: any) => {
    formdata.append(e, selectedBook.value[e]);
  });
  if (typeof selectedCategory.value == "string") {
    formdata.append("updateCategory", selectedCategory.value);
  } else if (typeof selectedCategory.value == "object") {
    formdata.append("updateCategory", "");
    formdata.set("category", selectedCategory.value.id);
  } else {
    formdata.append("updateCategory", "");
  }
  axios.put(proxy.$API.API_ORIGIN_BOOK, formdata).then((res: any) => {
    if (res.code == 200) {
      ElMessage({
        message: res.msg,
        type: "success",
      });
      editSecondHandBook.value = true;
      elStepsActiveId.value += 1;
    } else {
      ElMessage({
        message: res.error,
        type: "error",
      });
    }
  });
};

const resetBookInfo = () => {
  categoryOptions.value = {};
  selectedBook.value = {};
  selectedCategory.value = {};
  showEditCon.value = false;
};
// 添加新书
const addBook = () => {
  showEditCon.value = true;
  addBookTag.value = true;
};
// 提交新书信息
const addBookInfo = () => {
  const formdata = new FormData();
  formdata.append("imgFile", changeImg.value);
  Object.keys(selectedBook.value).forEach((e: any) => {
    formdata.append(e, selectedBook.value[e]);
  });
  if (typeof selectedCategory.value == "string") {
    formdata.append("updateCategory", selectedCategory.value);
  } else if (typeof selectedCategory.value == "object") {
    formdata.append("updateCategory", "");
    formdata.set("category", selectedCategory.value.id);
  } else {
    formdata.append("updateCategory", "");
  }
  axios.post(proxy.$API.API_ORIGIN_BOOK, formdata).then((res: any) => {
    if (res.code == 200) {
      selectedBook.value.id = res.data.id;
      ElMessage({
        message: res.msg,
        type: "success",
      });
      editSecondHandBook.value = true;
      elStepsActiveId.value += 1;
    } else {
      ElMessage({
        message: res.error,
        type: "error",
      });
    }
  });
};
// 返回至选择原图书界面
const backBookInfo = () => {
  elStepsActiveId.value = 0;
  editSecondHandBook.value = false;
  secondHandBookImg.value = {};
};
// 提交二手信息
const saveSecondHandBookInfo = () => {
  const formdata = new FormData();
  formdata.append("image", secondHandBookImg.value);
  formdata.append("name", secondHandBookInfo.value.name);
  formdata.append("price", secondHandBookInfo.value.price);
  formdata.append("originbook", selectedBook.value.id);
  // 判断字段
  if (!secondHandBookInfo.value.name) {
    ElMessage({
      type: "error",
      message: "请填写书籍名称",
    });
    return;
  }
  if (!secondHandBookImg.value) {
    ElMessage({
      type: "error",
      message: "至少上传一张图片",
    });
    return;
  }
  if (!secondHandBookInfo.value.price) {
    ElMessage({
      type: "error",
      message: "请填写书籍价格",
    });
    return;
  }

  axios.post(proxy.$API.API_SECONDHAND_BOOK, formdata).then((res: any) => {
    if (res.code == 200) {
      ElMessage({
        message: res.msg,
        type: "success",
      });
      showSuccessPage.value = true;
      elStepsActiveId.value += 2;
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
.steps_con {
  margin-bottom: 30px;
}
.select_book_con,
.edit_second_hand_book_con {
  h3 {
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 10px;
  }
}
.select,
.book_info_form {
  margin-left: 10px;
}
.book_info_form_con,
.edit_second_book_form_con {
  margin: 10px 0;
}
.book_img {
  border: 1px solid #e5e5e5;
}
.change_img_text {
  position: relative;
}
.book_img {
  cursor: pointer;
  display: inline-block;

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
.reset-btn,
.back-btn {
  float: right;
  margin-right: 20px;
  margin-top: 20px;
  background-color: #9b9b9b;
  border: 0px;
  font-size: 16px;
  padding: 7px 25px;
  border-radius: 5px;
  color: #fff;
  font-weight: bold;
  cursor: pointer;
}
.select {
  width: 240px;
  float: left;
}
.add_new_book_con {
  line-height: 32px;
  cursor: pointer;
  display: block;
  width: 80px;
  border-radius: 2px;
  background: #fff;
  font-size: 12px;
  text-align: center;
  color: #a9987f;
  border: 1px solid #dad4cc;
  &:hover {
    background: #f8f7f3;
    color: #967f5f;
    border: 1px solid #bbb1a2;
  }
}
.no_image {
  width: 120px;
  height: 100px;
  line-height: 70px;
  text-align: center;
  vertical-align: middle;
}
</style>
