<template>
  <div class="page-background" :style="{ backgroundImage: `url(${img.Url})` }">
    <div class="banner-author">
      <div>{{ img.Title }}</div>
      <div>
        <!----><span>{{ img.Copyright }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { MessagePlugin } from "tdesign-vue-next";

import b1 from "../assets/depj1.jpg";
import b2 from "../assets/depj2.jpg";
import b3 from "../assets/depj3.jpg";
import b4 from "../assets/depj4.jpg";
import b5 from "../assets/depj5.jpg";
import b6 from "../assets/depj6.jpg";
import b7 from "../assets/depj7.jpg";
import b8 from "../assets/depj8.jpg";
import b9 from "../assets/depj9.jpg";
import b10 from "../assets/depj10.jpg";

var apiurl = "https://api.mtb.wesley.net.cn";

export default {
  name: "BackgroundImage",
  data() {
    return {
      defimg: [b1, b2, b3, b4, b5, b6, b7, b8, b9, b10],
      img: {
        Url: "",
        Title: "",
        Copyright: "",
      },
    };
  },
  mounted() {
    var listurl = apiurl + "/api/getBackgroundImage?resolution=UHD&random=true";
    const xhr = new XMLHttpRequest();
    xhr.open("get", listurl, true);
    xhr.setRequestHeader(
      "Content-Type",
      "application/x-www-form-urlencoded; charset=UTF-8"
    );
    xhr.da;
    xhr.onload = () => {
      this.$data.img.Url = this.defimg[Math.floor(Math.random() * this.defimg.length)];
      if (xhr.status != 200) return false;
      var result = JSON.parse(xhr.response.replace(/\r|\n/gi, ""));
      if (result.errcode == 0) {
        if (result.data.length >1){
          console.log("请求背景图片失败，因为返回数据数量不正确")
          return false;
        }
        console.log(result.data);
        this.$data.img.Url = result.data.url;
        this.$data.img.Title = result.data.title;
        this.$data.img.Copyright = result.data.copyright;
      } else {
        console.log("请求错误了", xhr);
      }
    };
    xhr.onerror = () => {
      this.$data.img.Url = this.defimg[Math.floor(Math.random() * this.defimg.length)];
      console.log(xhr);
      console.log("请求错误了", xhr);
    };
    xhr.send();
  },
};
</script>
