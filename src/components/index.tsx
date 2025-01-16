import { defineComponent, h } from "vue";

export default defineComponent({
  props:{
    param: {
      type: String,
      default: '',
    },
    login: {
      type: Boolean,
      default: false,
    },
    username: {
      type: String,
      default: '',
    },
    userInfo: {
      type: Object,
      default: {},
    }
  },
  render: function () {
    return(
      <router-view login={this.login} username={this.username} param={this.param} userInfo={this.userInfo}></router-view>
    )
  },
});