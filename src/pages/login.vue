<template>
    <div class="login">
        <h1 class="mtb-page-title page-title mtb-title-small" style="padding-top: 4px">
            团委媒体部
        </h1>
        <h1 class="mtb-page-title page-title mtb-title-small" style="padding-top: 4px">
            统一认证系统 (SSO)
        </h1>
        <div class="mtb-tab-container" v-if="!already_login">
            <!---->
            <div role="tablist" class="mtb-tab login-tab">
                <div class="mtb-tab-lists">
                    <!---->
                    <div
                        class="mtb-tab-item"
                        v-for="(item, index) in tab_items"
                        :class="{ active: item.active }"
                        @click="handleClickTabs(index)">
                        <a class="mtb-link mtb-tab-link mtb-link-normal">{{ item.text }}</a>
                    </div>
                    <!---->
                </div>
            </div>
            <!---->
            <div class="mtb-center">
                <div class="mtb-tab-panel">
                    <!---->
                    <div class="pws_login_content" v-show="tab_items[0].active">
                        <div class="mtb-form-input">
                            <div
                                class="mtb-input-label"
                                :class="{
                                    'text-danger': form_state.account_input.inerror,
                                }">
                                账号
                            </div>
                            <div class="mtb-input-group">
                                <!---->
                                <div class="mtb-input-wrapper">
                                    <input
                                        name="username"
                                        placeholder=""
                                        maxlength="100"
                                        aria-label="账号"
                                        type="text"
                                        class="mtb-input"
                                        :class="{
                                            'mtb-input-error': form_state.account_input.inerror,
                                        }"
                                        @focus="account_input_focus"
                                        v-model="form_data.account" />
                                </div>
                                <!---->
                            </div>
                            <!---->
                            <!-- <div class="mtb-error-msg text-danger mtb-input-helper mtb-error-msg-left" v-if="
                    form_state.account_input.inerror &&
                    !form_state.password_input.inerror
                  ">
                    <svg aria-hidden="true" class="mtb-error-icon mtb-svg-icon" style="width: 14px; height: 14px">
                      <use xlink:href="#error"></use>
                    </svg>
                    <span>{{ form_state.account_input.tip }}</span>
                  </div> -->
                            <!---->
                        </div>
                        <!---->
                        <div class="mtb-form-input" style="margin-top: 12px">
                            <div
                                class="mtb-input-label"
                                :class="{
                                    'text-danger': form_state.password_input.inerror,
                                }">
                                密码
                            </div>
                            <div class="mtb-input-group">
                                <!---->
                                <div class="mtb-input-wrapper mtb-input-wrapper-password">
                                    <input
                                        placeholder=""
                                        maxlength="100"
                                        aria-label="密码"
                                        :type="
                                            form_state.password_input.showpws ? 'text' : 'password'
                                        "
                                        class="mtb-input"
                                        :class="{
                                            'mtb-input-error': form_state.password_input.inerror,
                                        }"
                                        @focus="password_input_focus"
                                        v-model="form_data.password"
                                        @keydown.enter="login" />
                                    <span class="mtb-input-suffix" @click="toggle_password_input">
                                        <svg
                                            aria-hidden="true"
                                            class="mtb-password-icon mtb-svg-icon"
                                            style="width: 20px; height: 20px">
                                            <use
                                                :xlink:href="
                                                    form_state.password_input.showpws
                                                        ? '#eye'
                                                        : '#eye-slash'
                                                "></use>
                                        </svg>
                                    </span>
                                </div>
                                <!---->
                            </div>
                            <!---->
                            <div
                                class="mtb-error-msg text-danger mtb-input-helper mtb-error-msg-left"
                                v-if="form_state.password_input.inerror">
                                <svg
                                    aria-hidden="true"
                                    class="mtb-error-icon mtb-svg-icon"
                                    style="width: 14px; height: 14px">
                                    <use xlink:href="#error"></use>
                                </svg>
                                <span>{{ form_state.password_input.tip }}</span>
                            </div>
                            <!---->
                        </div>
                        <!---->
                        <div class="forget-password">
                            <span
                                @click="goToForgetPWS"
                                style="cursor: pointer"
                                class="mtb-link mtb-link-primary mtb-link-small">
                                忘记密码？
                            </span>
                        </div>
                        <!---->
                        <div class="action">
                            <button
                                aria-label="登录"
                                @click="login"
                                style="transition: all 0.28s cubic-bezier(0.38, 0, 0.24, 1)"
                                class="btn login-btn primary lg mtb-btn mtb-btn-black mtb-btn-primary mtb-btn-large mtb-btn-block">
                                <span> 登录 </span>
                            </button>
                        </div>
                    </div>
                    <!-- 扫码登录  -->
                    <div class="scan_login_content" v-show="tab_items[1].active">
                        <!---->
                        <div>
                            <div
                                class="ac-loading-view login-wechat-loading-page"
                                style="min-height: 24px">
                                <div class="loading-bg"></div>
                                <svg v-if="miniprogramCode.loading && !miniprogramCode.error" aria-hidden="true" class="icon-loading ac-svg-icon" style="width: 24px; height: 24px;"><use xlink:href="#loading-retry"></use></svg>
                                <div v-else></div>
                                <!---->
                                <div id="wechat_login" class="login-wechat-container">
                                    <div class="wrp_code" v-if="miniprogramCode.img">
                                      <img style="width: 192px;height: 192px;margin: 0 auto;border-width: 0;" :src="miniprogramCode.img">
                                    </div>
                                </div>
                                <!---->
                                <div v-if="miniprogramCode.error || miniprogramCode.scaned || miniprogramCode.cancel" class="status-bg"></div>
                                <!---->
                                <div class="wechat-error" v-if="!miniprogramCode.loading && miniprogramCode.error">
                                    <div class="wechat-error-text">{{ miniprogramCode.errMsg }}</div>
                                    <div class="wechat-error-button mt-2" @click="getMiniprogramCode">
                                        <svg aria-hidden="true" class="ac-wechat-retry-icon ac-svg-icon" style="width: 18px; height: 18px;">
                                            <use xlink:href="#retry"></use>
                                        </svg>
                                    </div>
                                </div>
                                <!---->
                                <div class="wechat-scaned" v-if="!miniprogramCode.loading && miniprogramCode.scaned">
                                    <div class="status-icon">
                                        <svg aria-hidden="true">
                                            <use xlink:href="#success"></use>
                                        </svg>
                                    </div>
                                    <div class="status-text">扫描成功，请点击「授权」进行登录</div>
                                </div>
                                <!---->
                                <div class="wechat-scaned" v-if="!miniprogramCode.loading && miniprogramCode.cancel">
                                    <div class="status-icon">
                                        <svg aria-hidden="true">
                                            <use xlink:href="#error"></use>
                                        </svg>
                                    </div>
                                    <div class="status-text">授权失败，您已取消登录</div>
                                </div>
                                <!---->
                                <!---->
                            </div>
                        </div>
                        <p style="font-size: 16px;font-style: normal;font-weight: 600;line-height: 24px;color: rgba(0, 0, 0, 0.85);text-align: center;margin-top: 12px;">
                            使用微信『扫一扫』
                            <br/>
                            进入小程序后授权登录
                        </p>
                    </div>
                    <!---->
                </div>
            </div>
        </div>
        <!-- 已登录 -->
        <div class="mtb-tab-container" v-else>
            <div class="mtb-center">
                <div class="mtb-tab-panel">
                    <div class="al_login_content">
                        <div class="mtb-form-input">
                            <div class="mtb-input-group">
                                <!---->
                                <div
                                    style="
                                        display: flex;
                                        flex-direction: column;
                                        align-items: center;
                                    ">
                                    <t-avatar size="120px" class="--we-tag-black">
                                        <template #icon>
                                            <t-icon name="user" />
                                        </template>
                                    </t-avatar>
                                    <div
                                        class="mtb-input-label"
                                        style="font-size: 19px; margin-top: 24px">
                                        {{ username }}，您已登录
                                    </div>
                                </div>
                                <!---->
                            </div>
                            <!---->
                        </div>

                        <div class="action" style="display: flex;flex-direction: column;gap: 8px;">
                            <button
                                aria-label="重新授权"
                                @click="relogin"
                                style="transition: all 0.28s cubic-bezier(0.38, 0, 0.24, 1)"
                                class="btn login-btn primary lg mtb-btn mtb-btn-black mtb-btn-primary mtb-btn-large mtb-btn-block">
                                <span> 进入媒体部管理系统 </span>
                            </button>
                            <!---->
                            <button
                                aria-label="操作微信"
                                :style="
                                    !userInfo?.openid ? { background: 'transparent', color: '#07c160', border: '3px solid #07c160', fontWeight: 'bold' }
                                    : { background: '#07c160', color: '#fff', border: '3px solid #07c160', fontWeight: 'bold' }"
                                @click="() => { !userInfo?.openid ? bindWechat() : unbindWechat() }"
                                class="btn login-btn success lg mtb-btn mtb-btn-black mtb-btn-success mtb-btn-large mtb-btn-block"
                            >
                                <span>{{ !userInfo?.openid ? '绑定微信' : '解绑微信' }}</span>
                            </button>
                            <!-- <button
                                aria-label="操作微信"
                                style="
                                    background: transparent;
                                    border: 3px solid #07c160;
                                    color: #07c160;
                                    font-weight: bold;
                                "
                                v-if="userInfo?.openid === ''"
                                @click=""
                                class="btn login-btn success lg mtb-btn mtb-btn-black mtb-btn-success mtb-btn-large mtb-btn-block">
                                <span> 绑定微信 </span>
                            </button>
                            <button
                                aria-label="操作微信"
                                style="
                                    background: #07c160;
                                    border: 3px solid #07c160;
                                    color: #fff;
                                    font-weight: bold;
                                "
                                v-else
                                @click="unbindWechat"
                                class="btn login-btn success lg mtb-btn mtb-btn-black mtb-btn-success mtb-btn-large mtb-btn-block">
                                <span> 解绑微信 </span>
                            </button> -->
                            <!---->
                            <div style="display: flex;flex-direction: row;gap: 8px;">
                                <button
                                    aria-label="修改密码"
                                    @click="goToChangePWS"
                                    style="
                                        background: transparent;
                                        border: 3px solid #262626;
                                        color: #262626;
                                        font-weight: bold;
                                    "
                                    class="btn login-btn primary lg mtb-btn mtb-btn-black mtb-btn-primary mtb-btn-large mtb-btn-block">
                                    <span> 修改密码 </span>
                                </button>
                                <!---->
                                <button
                                    aria-label="退出登录"
                                    @click="logoutF"
                                    style="
                                        background: transparent;
                                        border: 3px solid #d32029;
                                        color: #d32029;
                                        font-weight: bold;
                                    "
                                    class="btn login-btn primary lg mtb-btn mtb-btn-danger mtb-btn-primary mtb-btn-large mtb-btn-block">
                                    <span> 退出登录 </span>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!---->
        <div class="mtb-service-links">
            <div class="mtb-divider"><span></span></div>
            <p style="padding-bottom: 4px">
                遇到问题？
                <t-popup>
                    <template #content>
                        <div>
                            <img style="width: 235px;" src="../assets/WxCode.jpg">
                        </div>
                    </template>
                    <a href="javascript:void(0)" class="mtb-link mtb-link-primary ml-2 mtb-link-primary">联系技术人员</a>
                </t-popup>
            </p>
        </div>
        <!---->
        <div class="login-loading" v-if="loading">
            <div class="icon">
                <svg>
                    <use xlink:href="#loading"></use>
                </svg>
            </div>
            <div class="text">
                <div>加载中...</div>
            </div>
        </div>
    </div>
    <!--Dialog-->
    <t-dialog
        v-model:visible="DialogVisible"
        :closeBtn="false"
        :closeOnEscKeydown="false"
        :closeOnOverlayClick="false"
        ref="BindWechatDialog"
        >
        <template #header>
            <span>{{ DialogType === 'bind' ? '绑定' : '解绑' }}微信</span>
        </template>
        <template #cancelBtn>
            <t-button v-if="DialogType === 'unbind'" variant="outline" theme="primary" @click="DialogVisible = false">我再想想</t-button>
        </template>
        <template #confirmBtn>
            <t-button v-if="DialogType === 'bind'" @click="DialogVisible = false">关闭弹窗</t-button>
            <t-button v-else @click="confirmUnbind">确定解绑</t-button>
        </template>
        <template #body>
            <div v-if="DialogType === 'bind'" class="bindWechatDialog">
                <div v-if="DialogInfo.status === 0" class="loading-bg">
                    <svg aria-hidden="true" class="icon-loading ac-svg-icon" style="width: 24px; height: 24px;"><use xlink:href="#loading-retry"></use></svg>
                </div>
                <div v-else></div>
                <!---->
                <div id="wechat_login" class="login-wechat-container">
                    <div class="wrp_code" v-if="DialogInfo.img">
                      <img style="width: 192px;height: 192px;margin: 0 auto;border-width: 0;" :src="DialogInfo.img">
                    </div>
                </div>
                <!---->
                <div v-if="DialogInfo.status !== 0 && DialogInfo.status !== 400 && DialogInfo.status !== 403" class="status-bg">
                <!---->
                <div class="wechat-error" v-if="DialogInfo.status === 404 || DialogInfo.status === 405">
                    <div class="wechat-error-text">{{ DialogInfo.errmsg }}</div>
                    <div class="wechat-error-button mt-2" @click="getBindMiniprogramCode">
                        <svg aria-hidden="true" class="ac-wechat-retry-icon ac-svg-icon" style="width: 18px; height: 18px;">
                            <use xlink:href="#retry"></use>
                        </svg>
                    </div>
                </div>
                <!---->
                <div class="wechat-scaned" v-if="DialogInfo.status === 401">
                    <div class="status-icon">
                        <svg aria-hidden="true">
                            <use xlink:href="#success"></use>
                        </svg>
                    </div>
                    <div class="status-text">扫描成功，请点击「绑定」进行绑定</div>
                </div>
                <!---->
                <div class="wechat-scaned" v-if="DialogInfo.status === 402">
                    <div class="status-icon">
                        <svg aria-hidden="true">
                            <use xlink:href="#error"></use>
                        </svg>
                    </div>
                    <div class="status-text">绑定失败，您已取消绑定</div>
                </div>
                </div>
                <p style="font-size: 16px;font-style: normal;font-weight: 600;line-height: 24px;color: rgba(0, 0, 0, 0.85);text-align: center;margin-top: 12px;">
                    请使用小程序 或 微信 扫码
                    <br/>
                    进行账号绑定
                </p>
            </div>
            <!--解除绑定-->
            <div v-else>
                <div> 确定解绑吗？如需再次使用 微信登录 需要重新进行绑定！ </div>
            </div>
        </template>
    </t-dialog>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from "vue";
import { MessagePlugin } from "tdesign-vue-next";
import { api, wxApi, jump_defaultURL } from "../config";
import localRouter from "../router.ts";
import { type ParamerData } from "../types.ts"
import { logout, checkMiniprogramCodeStatus } from "../components/hooks.ts";
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const BindWechatDialog = ref("")
const DialogVisible = ref(false)
const DialogType = ref("bind")// bind || unbind
const DialogInfo = reactive({
    key: "",
    img: "",
    status: 0,
    errmsg: "",
})
const getQueryVariable = () => {
    const key = Object.keys(route.query)
    let dataList:{[key:string]:string} = {}
    // 每项只取一个值
    for (const i of key) {
        dataList[i] = typeof route.query[i] === "string" ? route.query[i] : (route.query[i] as Array<string>)[0]
    }
    return dataList
}

onMounted(() => {
    // 获取url参数
    router.isReady().then(() => {
        const { loginType } = getQueryVariable()
        console.log("loginType: "+loginType)
        if (loginType == "scan") {
            // 扫描模式
            handleClickTabs(1)
        }
    })
})

const lock = ref(false);
const prop = defineProps({
    param: {
        type: Object,
    },
    login: {
        type: Boolean,
    },
    username: {
        type: String,
    },
    userInfo: {
        type: Object,
    }
})
const param = ref<ParamerData>(prop.param)
const already_login = ref(prop.login)
const username = ref(prop.username)
const userInfo = ref(prop.userInfo)
setInterval(() => {
    param.value = prop.param
    already_login.value = prop.login
    username.value = prop.username
    userInfo.value = prop.userInfo
}, 1);
const token = ref("")
const form_state = reactive({
    error_type: "",
    account_input: {
        state: "normal",
        inerror: false,
        tip: "",
    },
    password_input: {
        state: "normal",
        inerror: false,
        tip: "",
        showpws: false,
    },
})
const miniprogramCode = reactive({
    key: "",
    img: "",
    loading: true,
    error: false,
    scaned: false,
    cancel: false,
    errMsg: "网络超时，加载失败",
    interval: 0,
})
const form_data = reactive({
    account: "",
    password: "",
})
var checkCodeStatus:checkMiniprogramCodeStatus
const getMiniprogramCode = () => {
    miniprogramCode.loading = true
    miniprogramCode.error = false
    miniprogramCode.scaned = false
    miniprogramCode.cancel = false
    miniprogramCode.key = ""
    miniprogramCode.img = ""
    // clearInterval(miniprogramCode.interval)
    // 请求
    fetch(wxApi + "/getMiniProgramCode", {
        method: "GET",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
    })
    .then( res => res.json() )
    .then((res) => {
        if (res.errcode !== 0) {
            MessagePlugin.error("请求失败，" + (res.errmsg ?? "未知错误"), 3000)
            return;
        }
        miniprogramCode.key = res.data.key
        miniprogramCode.img = res.data.img_base64
        if (!tab_items[1].active) return;
        // 开始循环检测key
        checkCodeStatus = new checkMiniprogramCodeStatus(miniprogramCode.key,(data: any) => {
            if (data.status === 405) {
                checkCodeStatus?.stop()
                // clearInterval(miniprogramCode.interval)
            }
            // 已扫码，未确认
            if (data.status === 401) {
                miniprogramCode.scaned = true
                miniprogramCode.cancel = false
            }
            // 已扫码，但取消了
            if (data.status === 402) {
                miniprogramCode.scaned = false
                miniprogramCode.cancel = true
            }
            if (data.status === 403) {
                // clearInterval(miniprogramCode.interval)
                checkCodeStatus?.stop()
                miniprogramCode.cancel = false
                miniprogramCode.scaned = false
                const { class:classs, code, group, id, name, openid, token } = data.data
                // 登录成功
                MessagePlugin.success("登录成功，请稍后...");
                // 跳转
                setTimeout(() => {
                    jump__(
                        param.value.backUrl,
                        token,
                        code,
                        name,
                        classs,
                    );
                }, 1500);
            }
        },()=>{},(err: any) => {
            MessagePlugin.error("请求失败，" + (err.errmsg ?? err ?? "未知错误"), 3000)
            console.error("发生错误，终止循环")
        })
        checkCodeStatus?.start()
    })
    .catch((err) => {
        console.log(err)
        MessagePlugin.error("请求失败，" + err, 3000)
        miniprogramCode.img = ""
        miniprogramCode.error = false
    })
    .finally(() => {
        miniprogramCode.loading = false
    })
}
const tab_items = reactive([
    {
        id: 1,
        text: "账密登录",
        active: true,
        onChange: getMiniprogramCode,
    },
    {
        id: 2,
        text: "扫码登录",
        active: false,
    },
])
const loading = ref(false)




const goToForgetPWS = () => {
    localRouter.push({ path: "/forget-password" });
};

const account_input_focus = () => {
    form_state.account_input.state = "normal";
    form_state.account_input.inerror = false;
}

const password_input_focus = () => {
    form_state.password_input.state = "normal";
    form_state.password_input.inerror = false;
    if (form_state.error_type == "accandpasserr") {
        form_state.account_input.inerror = false;
    }
}

const toggle_password_input = () => {
    if (form_state.password_input.showpws) {
        form_state.password_input.showpws = false;
    } else {
        form_state.password_input.showpws = true;
    }
}

const handleClickTabs = (e: number) => {
    for (const key in tab_items) {
        const element = tab_items[key];
        if (element.id == e + 1) {
            element.active = true;
        } else {
            element.active = false;
            element?.onChange?.()
        }
    }
    checkCodeStatus?.stop()
    // clearInterval(miniprogramCode.interval)
}

/**
 * @login
 * @登录
 */
const login = () => {
    loading.value = true;
    if (lock.value) {
        MessagePlugin.warning("重复触发");
        return false;
    }
    lock.value = true;
    var account = form_data.account;
    var password = form_data.password;
    if (account == "") {
        form_state.account_input.state = "danger";
        form_state.account_input.inerror = true;
        form_state.account_input.tip = "";
    }
    if (password == "") {
        form_state.password_input.state = "danger";
        form_state.password_input.inerror = true;
        form_state.password_input.tip = "账号密码不能为空";
    }
    if (account != "" && password != "") {
        const xhr = new XMLHttpRequest();
        xhr.open("post", api + "/login", true);
        xhr.setRequestHeader(
            "Content-Type",
            "application/x-www-form-urlencoded; charset=UTF-8"
        );
        xhr.onload = () => {
            loading.value = false;
            var result = JSON.parse(xhr.response.replace(/\r|\n/gi, ""));
            if (result.errcode == 0) {
                var userdata = result.data;
                token.value = result.data.token;
                localStorage.setItem("loginstate", "true");
                localStorage.setItem("token", result.data.token)
                if (param.value.backUrl != false) {
                    MessagePlugin.success("登录成功，请稍后...");
                    setTimeout(() => {
                        jump__(
                            param.value.backUrl,
                            result.data.token,
                            userdata.usercode,
                            userdata.name,
                            userdata.class,
                        );
                    }, 1500);
                } else {
                    MessagePlugin.success("登录成功");
                    setTimeout(() => {
                        location.reload();
                    }, 1500);
                }
            } else if (result.errcode == -20001) {
                MessagePlugin.error("账户或密码错误");
                form_state.account_input.inerror = true;
                form_state.password_input.inerror = true;
                form_state.password_input.tip = "账户或密码错误";
                form_state.error_type = "accandpasserr";
            } else {
                MessagePlugin.error("登陆失败：" + result.errmsg);
            }
        };
        xhr.onerror = () => {
            loading.value = false;
            MessagePlugin.error("请求出现了错误！Errcode: " + xhr.status);
            console.log(xhr);
            console.log("请求错误啦！！！", xhr);
        };
        xhr.send("account=" + account + "&password=" + password);
    }
    lock.value = false;
}

const logoutF = () => {
    loading.value = true;
    logout()
}

/**
 * @changepassword
 * @修改密码路由
 */
const goToChangePWS = () => {
    localRouter.push("/change-password")
}

/**
 * @jump__
 * @登录后带参跳转
 */
const jump__ = (URL: string | null, TOKEN: string, CODE: string, NAME: string, CLASS: string) => {
    const BACKURL = URL || param.value.backUrl || jump_defaultURL;
    const TIMESTAMP = Date.now();
    const Paramers: Record<string, string | number> = {
        user_token: TOKEN,
        user_code: CODE,
        user_name: NAME,
        user_class: CLASS,
        login_time: TIMESTAMP,
        actionType: "Login_Back",
    };

    let RETURN_URL = BACKURL.includes("?") ? `${BACKURL}&` : `${BACKURL}?`;
    RETURN_URL += Object.entries(Paramers)
        .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(String(value))}`)
        .join("&");

    const RETURN_A_ELEMENT = document.createElement("a");
    RETURN_A_ELEMENT.style.display = "none";
    RETURN_A_ELEMENT.href = RETURN_URL;
    document.body.appendChild(RETURN_A_ELEMENT);
    RETURN_A_ELEMENT.click();
};

/**
 * @relogin
 * @重新授权
 */
const relogin = () => {
    loading.value = true;
    var token = localStorage.getItem("token") ?? "";
    if (!token) {
        MessagePlugin.error("token不存在，请重新登录");
        setTimeout(() => {
            location.reload();
        }, 1500);
        return;
    }
    fetch(api + "/relogin", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "token": token
        },
    })
    .then( res => res.json() )
    .then((result) => {
        if (result.errcode == 0) {
            const userdata = result.data;
            MessagePlugin.success("授权成功，请稍后...");
            setTimeout(() => {
                jump__(
                    null,
                    token,
                    userdata.code,
                    userdata.name,
                    userdata.class,
                );
            }, 1500);
        } else {
            // 登录失效
            localStorage.removeItem("loginstate");
            localStorage.removeItem("token");
        }
    })
    .catch((err) => {
        console.error("请求错误:",err)
    })
    .finally(() => {
        loading.value = false;
    })
}

const getBindMiniprogramCode = () => {
    fetch(wxApi + `/getMiniProgramCode?type=bind&uid=${userInfo.value?.uid ?? ""}`, {
        method: "GET",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
    })
    .then( res => res.json() )
    .then((res) => {
        if (res.errcode !== 0) {
            MessagePlugin.error("请求失败，" + (res.errmsg ?? "未知错误"), 3000)
            return;
        }
        const { img_base64, key } = res.data
        DialogInfo.img = img_base64
        DialogInfo.key = key
        DialogInfo.status = 400
        // 开始循环检测key
        checkCodeStatus = new checkMiniprogramCodeStatus(DialogInfo.key,(data: any) => {
            if (!BindWechatDialog.value) {
                checkCodeStatus?.stop()
                return;
            }
            // 不存在
            if (data.status === 405) {
                checkCodeStatus?.stop()
                DialogInfo.status = 405
                DialogInfo.errmsg = "小程序码已过期，请重新获取！"
            }
            // 已扫码，未确认
            if (data.status === 401) {
                DialogInfo.status = 401
            }
            // 已扫码，但取消了
            if (data.status === 402) {
                DialogInfo.status = 402
            }
            if (data.status === 403) {
                // 绑定成功
                DialogInfo.status = 403
                checkCodeStatus?.stop()
                MessagePlugin.success("绑定成功，请重新登录！",3500);
                // 登出
                setTimeout(() => {
                    logout()
                }, 2000);
            }
        },()=>{},(err: any) => {
            DialogInfo.status = 404
            DialogInfo.errmsg = err.errmsg ?? err ?? "未知错误"
            MessagePlugin.error("请求失败，" + (err.errmsg ?? err ?? "未知错误"), 3000)
            console.error("发生错误，终止循环")
        })
        checkCodeStatus?.start()
    })
    .catch((err) => {
        console.log(err)
        MessagePlugin.error("请求失败，" + err, 3000)
        DialogInfo.img = ""
        DialogInfo.status = 404
        DialogInfo.errmsg = err
    })
    .finally(() => {
        DialogVisible.value = false;
    })
}

const bindWechat = () => {
    // 先打开弹窗
    DialogVisible.value = true;
    DialogType.value = "bind"
    DialogInfo.img = ""
    DialogInfo.status = 0
    // 再获取小程序码
    getBindMiniprogramCode()
}

const unbindWechat = () => {
    DialogVisible.value = true;
    DialogType.value = "unbind"
}

const confirmUnbind = () => {
    fetch(wxApi + `/unbind`, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `openid=${userInfo.value?.openid ?? ""}`
    })
    .then( res => res.json() )
    .then((res) => {
        if (res.errcode !== 0) {
            MessagePlugin.error("请求失败，" + (res.errmsg ?? "未知错误"), 3000)
            return;
        }
        MessagePlugin.success("解绑成功，请重新登录！",3500);
        setTimeout(() => {
            logout()
        }, 2000);
    })
    .catch((err) => {
        console.log(err)
        MessagePlugin.error("请求失败，" + err, 3000)
    })
    .finally(() => {
        DialogVisible.value = false;
    })
}

onMounted(() => {
    
});

</script>

<script lang="ts">
export default {
    name: "LoGin",
};
</script>

<style lang="scss">
.login-loading {
    position: absolute;
    top: 0px;
    left: 0px;
    height: 100%;
    width: 100%;
    background-color: rgb(0 0 0 / 60%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    .icon {
        >svg {
            width: 90px;
            height: 90px;
        }
    }
    .text {
        font-size: 34px;
        padding: 24px 0px;
        color: #f5f5f5;
        letter-spacing: 0.2px;
        font-weight: 500;
    }
}
</style>