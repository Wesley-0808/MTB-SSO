import { MessagePlugin } from "tdesign-vue-next";
import config, { wxApi } from "../config";

/**
 * @logout
 * @登出
 */
export const logout = () => {
    var token = localStorage.getItem("token") ?? "";
    fetch(config.api + "/logout", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "token": token
        },
    })
    .then( res => res.json() )
    .then((result) => {
        if (result.errcode == 0) {
            MessagePlugin.success("退登成功！",4000);
            localStorage.removeItem("loginstate");
            localStorage.removeItem("token");
            location.href = "/"
        } else {
            MessagePlugin.error("退登失败：" + result.errmsg);
        }
    })
    .catch((err) => {
        console.error("请求错误:",err)
    })
}


// 检测小程序码（扫码）状态
// 关于Key码的Status值定义说明：400-未扫码（初始） | 401-已扫码，未确认 | 402-已扫码，操作取消 | 403-已扫码，已确认 | 404-已扫码，但由于某种原因无法完成授权 | 405-不存在（已过期）
export class checkMiniprogramCodeStatus{
    key: string;
    StatusCallback: Function;
    StartCallback: Function;
    ErrorCallback: Function;
    FinallyCallback: Function;
    IntervalTimer: number | undefined;
    // 构造函数
    constructor(key:string,StatusCallback:Function,StartCallback:Function,ErrorCallback:Function,FinallyCallback:Function = () => {}) {
        this.key = key
        this.StatusCallback = StatusCallback
        this.StartCallback = StartCallback
        this.ErrorCallback = ErrorCallback
        this.FinallyCallback = FinallyCallback
    }
    start() {
        this.IntervalTimer = setInterval(() => {
            this.check()
        }, 1000);
    }
    stop() {
        console.log("停止检测")
        clearInterval(this.IntervalTimer)
        this.FinallyCallback?.()
    }
    check() {
        fetch(wxApi + "/checkCodeStatus", {
            method: "POST",
            body: `key=${this.key}`,
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
        })
        .then( res => res.json() )
        .then((res) => {
            if (res.errcode !== 0) {
                this.ErrorCallback?.(res)
                console.error("发生错误",res)
                return;
            }
            this.StatusCallback?.(res.data)
        })
        .catch((err) => {
            console.log(err)
            this.ErrorCallback?.(err)
        })
        .finally(() => {
            this.FinallyCallback?.()
        })
    }
}