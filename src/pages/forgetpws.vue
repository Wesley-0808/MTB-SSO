<template>
    <button
        type="primary"
        aria-label="返回"
        style="width: 80px; height: 32px; padding: 0px 8px"
        @click="back"
        class="mtb-btn mtb-btn-black mtb-btn-primary mtb-btn-large mtb-btn-block">
        <svg
            t="1686655706696"
            class="icon"
            viewBox="0 0 1024 1024"
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            p-id="2378"
            width="16"
            height="16">
            <path
                d="M297.813333 491.648l1.365334-1.749333 379.093333-376.149334a38.784 38.784 0 0 1 5.077333-4.096 34.346667 34.346667 0 0 1 14.293334-4.992c2.218667-0.170667 2.176-0.170667 4.394666-0.170666a33.493333 33.493333 0 0 1 14.549334 4.181333c12.330667 6.997333 18.688 21.76 15.274666 35.498667-1.237333 5.077333-7.04 13.44-7.04 13.44l-355.498666 352.853333 354.090666 354.389333s6.272 7.978667 7.893334 12.928a32.213333 32.213333 0 0 1-33.749334 41.557334c-6.656-0.682667-17.749333-7.68-17.749333-7.68l-379.221333-377.984-1.28-1.450667a30.378667 30.378667 0 0 1-7.893334-17.749333 31.018667 31.018667 0 0 1 3.712-18.602667 27.221333 27.221333 0 0 1 2.688-4.224z"
                p-id="2379"
                fill="#ffffff"></path>
        </svg>
        <span style="word-break: keep-all; letter-spacing: 3px; margin-left: 5px"> 返回 </span>
    </button>
    <div class="reset-password">
        <h1 class="mtb-page-title page-title mtb-title-small">重置密码</h1>
        <div class="reset-password-box">
            <div class="verify-user">
                <div class="mtb-form-input">
                    <div class="mtb-input-label">暂不支持的功能，请找管理员重置账号</div>
                    <!-- <div class="mtb-input-label">请输入已注册的账号</div> -->
                    <div class="mtb-input-group">
                        <!---->
                        <!-- <div class="mtb-input-wrapper">
                    <input name="username" placeholder="" maxlength="100" aria-label="请输入已注册的账号" type="text"
                      class="mtb-input" />
                  </div> -->
                    </div>
                    <!---->
                </div>
                <!---->
                <div class="action">
                    <button
                        type="primary"
                        aria-label="下一步"
                        class="mtb-btn mtb-btn-black mtb-btn-primary mtb-btn-large mtb-btn-block">
                        <!----><span> 下一步 </span>
                    </button>
                </div>
            </div>
            <!----><!----><!----><!---->
        </div>
        <div class="mtb-service-links">
            <div class="mtb-divider"><span></span></div>
            <p style="padding-bottom: 4px">
                找回密码遇到问题？
                <a
                    href="javascript:void(0)"
                    target="_blank"
                    class="mtb-link mtb-link-primary ml-2 mtb-link-primary"
                    >联系技术人员</a
                >
            </p>
            <p style="padding-bottom: 4px">
                没有账号？
                <a
                    href="javascript:void(0)"
                    target="_blank"
                    class="mtb-link mtb-link-primary ml-2 mtb-link-primary"
                    >联系技术人员</a
                >
            </p>
        </div>
    </div>
</template>

<script>
import router from '../router.ts'

export default {
    name: "ForGetpws",
    methods: {
        back() {
          router.push('/')
        },
    },
};
</script>
