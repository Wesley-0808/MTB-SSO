<template>
    <div class="changelog">
        <div class="changelog-title">统一认证 更新日志</div>
        <div class="changelog-content">
            <!---->
            
            <!---->
            <ul class="changelog-list">
                <li>
                    <div class="changelog-date">v2.0.2 ( 2025/01/21 )</div>
                    <!---->
                    <ul class="changelog-item">
                        <li>支持微信小程序绑定和登录，支持在页面上操作解绑</li>
                        <li>Fetch重构</li>
                        <li>小程序侧API对接优化</li>
                        <li>OA侧对接优化</li>
                        <li>API对接优化</li>
                        <li>TOKEN相关逻辑优化</li>
                    </ul>
                </li>
            </ul>
        </div>
    </div>
</template>

<script lang="ts">
export default {
    name: "ChangeLog",
}
</script>

<style lang="scss">
.changelog {
    color: #fff;
}

.changelog-title {
    font-size: 36px;
    font-weight: 600;
    padding: 12px 0px;
    letter-spacing: 0.2px;
    display: flex;
    align-items: flex-start;
    justify-content: center;
}

.changelog-date{
    font-size: 22px;
    font-weight: 600;
    padding: 6px 0px;
}

.changelog-list {
    margin-left: 34px;
    list-style: disc;
}

.changelog-item {
    font-size: 19px;
    list-style: circle;
    margin-left: 18px;
    >li{
        letter-spacing: 1px;
        margin: 4px 0px;
    }
}

</style>