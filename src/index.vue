<template>
    <svgList />
    <div id="page" class="page page-cn page-pc page-banner page-wrapper-full">
        <BackgroundImage />
        <router-view v-slot="{ Component, route }">
            <!-- <transition name="fade"> -->
            
            <!-- </transition> -->
            <div class="wrapper" v-if="!['/CHANGELOG','/changelog'].includes(route.path)">
                <div class="container" style="padding-bottom: 36px">
                    <!---->
                    <component :is="Component" :param="param" :login="already_login" :username="username" :userInfo="userInfo"/>
                    <!---->
                </div>
            </div>
            <!---->
            <div class="transparentContainer" v-else>
                <div class="BackToIndex" @click="() => $router.push('/')">返回登录页</div>
                <div class="innerHolder">
                    <component :is="Component" :param="param" :login="already_login" :username="username" :userInfo="userInfo"/>
                </div>
            </div>
            <!---->
        </router-view>
        <!---->
        <footer class="mtb-footer text-center" style="opacity: 1">
            <div class="mtb-footer-copyright">
                <span class="mr-1">
                    Copyright © 2021-2024 顺德中专团委学生会媒体部 版权所有
                    <span class="changelogEntrance">
                        <a href="https://github.com/wesley-0808/MTB-SSO" target="__blank">仓库地址</a>
                    </span>
                    <span class="changelogEntrance" @click="goToChangelog">更新日志</span>
                </span>
            </div>
        </footer>
    </div>
</template>

<script setup lang="ts">
import { onBeforeMount, onMounted, ref } from "vue";
import BackgroundImage from "./components/backgroundImage.vue";
import svgList from "./components/svg.vue";
import config from "./config";
import { useRoute, useRouter } from 'vue-router'
import { MessagePlugin } from "tdesign-vue-next";
import { logout } from "./components/hooks.ts";

const already_login = ref(false);
const param = ref({});
const username = ref("");
const userInfo = ref({})
const diyPages = ref(["/CHANGELOG","/changelog"].includes(window.location.href))
const route = useRoute()
const router = useRouter()

const getQueryVariable = () => {
    const key = Object.keys(route.query)
    let dataList:{[key:string]:string} = {}
    // 每项只取一个值
    for (const i of key) {
        dataList[i] = typeof route.query[i] === "string" ? route.query[i] : (route.query[i] as Array<string>)[0]
    }
    return dataList
}

const loadParam = () => {
    // 获取url参数
    router.isReady().then(() => {
        const { backUrl=getQueryVariableBySearch("backUrl"), strongAuth, actionType=getQueryVariableBySearch("login"), loginType="account" } = getQueryVariable()
        var params = {
            backUrl: backUrl,
            strongAuth: strongAuth,
            actionType: actionType,
            loginType: loginType,
        };
        param.value = params;
        console.log(route)
        // 如果无actionType参数，则刷新页面并加上actionType=Login
        if (!actionType) {
            if (window.location.href.indexOf("?") == -1) {
                window.location.href = window.location.href + "?actionType=login";
            }
            else {
                window.location.href = window.location.href + "&actionType=login";
            }
        }
        console.log("backUrl: "+backUrl)
        console.log("actionType: "+actionType)
        if (actionType === "logout") {
            logout()
        }
    })
}

const init = () => {
    // 初始化一些内容
    already_login.value = false;
    if (!config.skip_login_check) {
        // 判断是否登录
        var loginstate = localStorage.getItem("loginstate");
        if (loginstate != "true") {
            return;
        }
        console.log("检测到了登录态信息，正在判断登录态是否有效。");
        var token = localStorage.getItem("token") as string
        fetch(config.api + "/checkToken",{
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                token: token
            }
        })
        .then( res => res.json() )
        .then((result) => {
            if (result.errcode == 0) {
                if (!result.data.verify) {
                    localStorage.removeItem("loginstate");
                    localStorage.removeItem("token");
                    return;
                }
                // 获取用户名称
                fetch(config.api + "/getLoginUserInfo",{
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                        token: token
                    }
                })
                .then( res => res.json() )
                .then((result) => {
                    if (result.errcode == 0) {
                        already_login.value = true;
                        username.value = result.data.name;
                        userInfo.value = result.data;
                    } else {
                        // 获取用户名称出错了
                        already_login.value = false;
                        console.error("获取用户名称出错了");
                        username.value = "请求出错";
                    }
                })
                .catch((err) => {
                    already_login.value = false;
                    console.log("请求错误", err);
                    username.value = "请求出错";
                })
            } else {
                // 登录失效
                localStorage.removeItem("loginstate");
                localStorage.removeItem("token");
            }
        })
        .catch((err) => {
            console.error("请求错误:",err)
        })
    }
}

/**
 * @getQueryVariable
 * @desc 获取参数
 * @param id 参数名
 */
const getQueryVariableBySearch = (variable:string) => {
    // var query = window.location.hash.substring(1);
    // var vars = query.split("&");
    // for (var i = 0; i < vars.length; i++) {
    //     var pair = vars[i].split("=");
    //     if (pair[0] == variable) {
    //         var res_str = pair[1]
    //             .replaceAll("%3F", "?")
    //             .replaceAll("%3D", "=")
    //             .replaceAll("%26", "&");
    //         return res_str;
    //     }
    // }
    // return false;
    //url例子：www.baidu.com?id="123456"&name="www"；  
    var url = decodeURI(window.location.search); //?id="123456"&name="www";
    var object:{[key:string]: string} = {};
    if (url.indexOf("?") != -1)//url中存在问号，也就说有参数。  
    {
      var str = url.substring(1);  //得到?后面的字符串
      var strs = str.split("&");  //将得到的参数分隔成数组[id="123456",name="www"];
      for (var i = 0; i < strs.length; i++) {
        object[strs[i].split("=")[0]] = strs[i].split("=")[1];//得到{id:'123456',name:'www'}
      }
    }
    return object[variable];
}

const goToChangelog = () => {
    router.push("/CHANGELOG")
}

onBeforeMount(() => {
    loadParam()
})

onMounted(() => {
    init()
})




</script>

<script lang="ts">
export default {
    name: "mtbSSO",
};
</script>

<style>
.--we-tag-black.t-avatar {
    color: #fff;
    background: #979797;
}
</style>
