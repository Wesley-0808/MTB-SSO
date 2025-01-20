<template>
    <button type="primary" aria-label="返回" style="width: 80px;height: 32px;padding: 0px 8px;" @click="back"
        v-if="!checkfalse" class="mtb-btn mtb-btn-black mtb-btn-primary mtb-btn-large mtb-btn-block">
        <svg t="1686655706696" class="icon" viewBox="0 0 1024 1024" version="1.1"
            xmlns="http://www.w3.org/2000/svg" p-id="2378" width="16" height="16">
            <path
                d="M297.813333 491.648l1.365334-1.749333 379.093333-376.149334a38.784 38.784 0 0 1 5.077333-4.096 34.346667 34.346667 0 0 1 14.293334-4.992c2.218667-0.170667 2.176-0.170667 4.394666-0.170666a33.493333 33.493333 0 0 1 14.549334 4.181333c12.330667 6.997333 18.688 21.76 15.274666 35.498667-1.237333 5.077333-7.04 13.44-7.04 13.44l-355.498666 352.853333 354.090666 354.389333s6.272 7.978667 7.893334 12.928a32.213333 32.213333 0 0 1-33.749334 41.557334c-6.656-0.682667-17.749333-7.68-17.749333-7.68l-379.221333-377.984-1.28-1.450667a30.378667 30.378667 0 0 1-7.893334-17.749333 31.018667 31.018667 0 0 1 3.712-18.602667 27.221333 27.221333 0 0 1 2.688-4.224z"
                p-id="2379" fill="#ffffff"></path>
        </svg>
        <span style="word-break: keep-all;letter-spacing: 3px;margin-left: 5px;"> 返回 </span>
    </button>
    <div class="reset-password">
        <h1 class="mtb-page-title page-title mtb-title-small">修改密码</h1>
        <!---->
        <div class="reset-password-box" v-if="current == 1">
            <div class="verify-user">
                <div class="mtb-form-input" v-if="checkfalse">
                    <div style="display: flex;justify-content: center;padding: 22px 0px;">
                        <svg aria-hidden="true" class="mtb-svg-icon mtb-logo"
                            style="width: 42px; height: 42px; color: rgb(51, 51, 51);transform: scale(1.8);">
                            <use xlink:href="#close"></use>
                        </svg>
                    </div>
                    <div class="mtb-input-label" style="text-align: center;margin-top: 18px;font-size: 18px;">
                        验证失败，请重新登录
                    </div>
                    <!---->
                    <button type="primary" aria-label="返回登录" @click="back" style="margin-top: 33px"
                        class="mtb-btn mtb-btn-black mtb-btn-primary mtb-btn-large mtb-btn-block">
                        <!----><span> 返回登录 </span>
                    </button>
                    <!---->
                </div>
                <!---->
                <div class="mtb-form-input" v-else>
                    <div class="mtb-input-group">
                        <!---->
                        <div style="display: flex;justify-content: center;padding: 38px 0px;"
                            v-if="state != '验证成功'">
                            <div class="circle-loader">
                                <div></div>
                                <div></div>
                                <div></div>
                                <div></div>
                                <div></div>
                                <div></div>
                                <div></div>
                                <div></div>
                            </div>
                        </div>
                        <!---->
                        <div v-else style="display: flex;justify-content: center;padding: 14px 0px;">
                            <svg aria-hidden="true" class="mtb-svg-icon mtb-logo"
                                style="width: 42px; height: 42px; color: rgb(51, 51, 51);transform: scale(1.4);">
                                <use xlink:href="#check"></use>
                            </svg>
                        </div>
                    </div>
                    <!---->
                    <div class="mtb-input-label" style="text-align: center;margin-top: 18px;font-size: 18px;"
                        v-if="state != '验证成功'">
                        <span>正在验证账号</span>{{ state }}
                    </div>
                    <!---->
                    <div class="mtb-input-label" style="text-align: center;margin-top: 14px;font-size: 18px;"
                        v-else>{{ state }}
                    </div>
                    <!---->
                </div>
                <!---->
                <div class="action">
                    <button type="primary" aria-label="下一步" @click="nextstep" v-if="checkok"
                        class="mtb-btn mtb-btn-black mtb-btn-primary mtb-btn-large mtb-btn-block">
                        <!----><span> 下一步 </span>
                    </button>
                </div>
            </div>
        </div>
        <!---->
        <div class="reset-password-box" v-if="current == 2">
            <div class="verify-user">
                <div class="mtb-form-input">
                    <div class="mtb-input-label" :class="{ 'text-danger': formstate.oldpws }">请输入账号原密码</div>
                    <div class="mtb-input-group">
                        <!---->
                        <div class="mtb-input-wrapper">
                            <input name="username" placeholder="" maxlength="100" aria-label="请输入账号原密码"
                                type="password" class="mtb-input" v-model="form.oldpws"
                                :class="{ 'mtb-input-error': formstate.oldpws, }" @focus="input_focus(1)" />
                        </div>
                    </div>
                    <!---->
                    <div class="mtb-error-msg text-danger mtb-input-helper mtb-error-msg-left"
                        v-if="formstate.oldpws">
                        <svg aria-hidden="true" class="mtb-error-icon mtb-svg-icon"
                            style="width: 14px; height: 14px">
                            <use xlink:href="#error"></use>
                        </svg>
                        <span>{{ formstate.oldpwstip }}</span>
                    </div>
                    <!---->
                </div>
                <!---->
                <div class="action">
                    <button type="primary" aria-label="上一步" @click="laststep"
                        style="background: transparent;border: 3px solid #262626;color: #262626;font-weight: bold;"
                        class="mtb-btn mtb-btn-black mtb-btn-primary mtb-btn-large mtb-btn-block">
                        <!----><span> 上一步 </span>
                    </button>
                    <button type="primary" aria-label="下一步" @click="nextstep"
                        class="mtb-btn mtb-btn-black mtb-btn-primary mtb-btn-large mtb-btn-block">
                        <!----><span> 下一步 </span>
                    </button>
                </div>
            </div>
        </div>
        <!---->
        <div class="reset-password-box" v-if="current == 3">
            <div class="verify-user">
                <div class="mtb-form-input">
                    <div class="mtb-input-label" :class="{
                        'text-danger': formstate.newpws
                    }">请输入账号新密码</div>
                    <div class="mtb-input-group">
                        <!---->
                        <div class="mtb-input-wrapper">
                            <input name="username" placeholder="" maxlength="100" aria-label="请输入账号新密码"
                                type="password" class="mtb-input" v-model="form.newpws"
                                :class="{ 'mtb-input-error': formstate.newpws, }" @focus="input_focus(2)" />
                        </div>
                    </div>
                    <!---->
                    <div class="mtb-error-msg text-danger mtb-input-helper mtb-error-msg-left"
                        v-if="formstate.newpws">
                        <svg aria-hidden="true" class="mtb-error-icon mtb-svg-icon"
                            style="width: 14px; height: 14px">
                            <use xlink:href="#error"></use>
                        </svg>
                        <span>{{ formstate.newpwstip }}</span>
                    </div>
                    <!---->
                </div>
                <!---->
                <div class="action">
                    <button type="primary" aria-label="上一步" @click="laststep"
                        style="background: transparent;border: 3px solid #262626;color: #262626;font-weight: bold;"
                        class="mtb-btn mtb-btn-black mtb-btn-primary mtb-btn-large mtb-btn-block">
                        <!----><span> 上一步 </span>
                    </button>
                    <button type="primary" aria-label="下一步" @click="nextstep"
                        class="mtb-btn mtb-btn-black mtb-btn-primary mtb-btn-large mtb-btn-block">
                        <!----><span> 提交 </span>
                    </button>
                </div>
            </div>
        </div>
        <!---->
        <div class="mtb-service-links">
            <div class="mtb-divider"><span></span></div>
            <p style="padding-bottom: 4px">
                遇到问题？
                <a href="javascript:void(0)" target="_blank" class="mtb-link mtb-link-primary ml-2 mtb-link-primary">联系技术人员</a>
            </p>
        </div>
    </div>
</template>
  
<script>
import { LogoutIcon } from 'tdesign-icons-vue-next';
import { MessagePlugin } from 'tdesign-vue-next';
import config from "../config";
import { logout } from "../components/hooks"

var apiurl = config.api

export default {
    name: "changePWS",
    data() {
        return {
            current: 1,
            token: "",
            state: "安全",
            checkok: false,
            checkfalse: false,
            form: {
                account: "",
                oldpws: "",
                newpws: "",
            },
            formstate: {
                oldpws: false,
                newpws: false,
                oldpwstip: "",
                newpwstip: "",
            },
        }
    },
    mounted() {
        var loginstate = localStorage.getItem('loginstate')
        if (loginstate == 'true') {
            console.log("检测到了登录态信息，正在判断登录态是否有效。")
            var token = localStorage.getItem("token");
            this.$data.token = token
            setTimeout(() => {
                this.$data.state = "登录态"
                var that = this
                const xhr = new XMLHttpRequest();
                xhr.open("post", apiurl + "/checkToken", true);
                xhr.setRequestHeader(
                    "Content-Type",
                    "application/x-www-form-urlencoded; charset=UTF-8"
                );
                xhr.setRequestHeader(
                    "token",token
                );
                xhr.onload = () => {
                    // this.$data.loading = false;
                    var result = JSON.parse(xhr.response.replace(/\r|\n/gi, ""));
                    if (result.errcode == 0) {
                        if (result.data.verify) {
                            this.$data.state = "验证成功"
                            this.$data.checkok = true
                        }
                        else{
                            this.$data.state = "验证失败，请重新登录"
                            this.$data.checkfalse = true
                        }
                    }
                    else{
                        localStorage.setItem('loginstate', 'false')
                        this.$data.checkfalse = true
                    }
                };
                xhr.onerror = () => {
                    console.log("请求错误", xhr);
                };
                xhr.send();
            }, 2000);
        }
        else {
            setTimeout(() => {
                this.$data.checkfalse = true
            }, 2000);
        }
    },
    methods: {
        back() {
            location.href = '/';
        },

        input_focus(e) {
            if (e == 1) {
                this.$data.formstate.oldpws = false
                this.$data.formstate.oldpwstip = ""
            }
            if (e == 2) {
                this.$data.formstate.newpws = false
                this.$data.formstate.newpwstip = ""
            }
        },

        nextstep() {
            var current = this.$data.current
            if (current == 1) {
                this.$data.current += 1
            }
            if (current == 2) {
                if (this.$data.form.oldpws == "") {
                    this.$data.formstate.oldpws = true
                    this.$data.formstate.oldpwstip = "请输入旧密码"
                }
                else {
                    this.$data.current += 1
                }
            }
            if (current == 3) {
                if (this.$data.form.newpws == "") {
                    this.$data.formstate.newpws = true
                    this.$data.formstate.newpwstip = "请输入新密码"
                }
                else {
                    this.submit()
                }
            }
        },

        laststep() {
            this.$data.current -= 1;
        },

        submit() {
            var form = this.$data.form
            var acc = form.account
            var opws = form.oldpws
            var npws = form.newpws
            var url = apiurl + "/changePassword";
            const xhr = new XMLHttpRequest();
            xhr.open("post", url, true);
            xhr.setRequestHeader(
                "Content-Type",
                "application/x-www-form-urlencoded; charset=UTF-8"
            );
            xhr.setRequestHeader("token",this.$data.token);
            xhr.onload = () => {
                var result = JSON.parse(xhr.response.replace(/\r|\n/gi, ""));
                if (result.errcode == 0) {
                    MessagePlugin.success("更改成功，请重新登录！")
                    setTimeout(() => {
                        logout()
                    }, 1500);
                }
                else if (result.errcode == -10001) {
                    MessagePlugin.error("操作失败：无法加密密码信息");
                }
                else if (result.errcode == -10002) {
                    MessagePlugin.error("操作失败：找不到用户");
                }
                else if (result.errcode == -10003) {
                    MessagePlugin.error("操作失败：原密码错误。");
                    this.$data.current = 2
                    this.$data.formstate.newpws = true
                    this.$data.formstate.newpwstip = "原密码错误。"
                }
                else if (result.errcode == -1005) {
                    MessagePlugin.error("操作失败：Token不存在或已过期，请重新登录");
                }
                else{
                    MessagePlugin.error("操作失败：" + result.errmsg);
                }
            };
            xhr.onerror = () => {
                console.log("请求错误", xhr);
            };
            xhr.send("key=" + this.$data.key + "&oldpassword=" + opws + "&newpassword=" + npws);
        },
    }
};
</script>

<style>
.circle-loader {
    position: relative;
    width: auto;
    height: auto;
}

.circle-loader div {
    height: 10px;
    width: 10px;
    background-color: #434343;
    border-radius: 50%;
    position: absolute;
    -webkit-animation: 0.8s opaque ease-in-out infinite both;
    animation: 0.8s opaque ease-in-out infinite both;
}

.circle-loader>div:nth-child(1) {
    top: -25px;
    left: 0;
}

.circle-loader>div:nth-child(2) {
    top: -17px;
    left: 17px;
    -webkit-animation-delay: 0.1s;
    animation-delay: 0.1s;
}

.circle-loader>div:nth-child(3) {
    top: 0;
    left: 25px;
    -webkit-animation-delay: 0.2s;
    animation-delay: 0.2s;
}

.circle-loader>div:nth-child(4) {
    top: 17px;
    left: 17px;
    -webkit-animation-delay: 0.3s;
    animation-delay: 0.3s;
}

.circle-loader>div:nth-child(5) {
    top: 25px;
    left: 0;
    -webkit-animation-delay: 0.4s;
    animation-delay: 0.4s;
}

.circle-loader>div:nth-child(6) {
    top: 17px;
    left: -17px;
    -webkit-animation-delay: 0.5s;
    animation-delay: 0.5s;
}

.circle-loader>div:nth-child(7) {
    top: 0;
    left: -25px;
    -webkit-animation-delay: 0.6s;
    animation-delay: 0.6s;
}

.circle-loader>div:nth-child(8) {
    top: -17px;
    left: -17px;
    -webkit-animation-delay: 0.7s;
    animation-delay: 0.7s;
}

@keyframes opaque {
    0% {
        opacity: 0.1;
    }

    40% {
        opacity: 1;
    }

    80% {
        opacity: 0.1;
    }

    100% {
        opacity: 0.1;
    }
}
</style>
  