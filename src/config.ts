
const config = {
    version: "2.0.0",
    debug: false,
    jump_login: false,
    skip_login_check: false,
    apiHost: "https://sso-api.mtb.wesley.net.cn/",
    oaApi: "https://oa-api.mtb.wesley.net.cn/v2",
    api: "https://sso-api.mtb.wesley.net.cn/v2/OAuth",
    wxApi: "https://sso-api.mtb.wesley.net.cn/v2/WxAuth",
    jump_defaultURL: "http://10.3.146.12/system",
}

export const { version, apiHost, api, wxApi, jump_defaultURL } = config

export default config