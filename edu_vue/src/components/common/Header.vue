<template>
    <div class="header-box">
        <div class="header">
            <div class="content">
                <div class="logo full-left">
                    <img src="/static/image/logo.jpg" alt="">
                </div>
                <ul class="nav full-left">
                    <li v-for="(link, index) in link_list" :key="index">
                        <a :href="link.link" v-if="link.is_site"><span>{{ link.title }}</span></a>
                        <router-link v-else :to="link.link">{{ link.title }}</router-link>
                   </li>
                </ul>
                <div class="login-bar full-right" v-show="isShow1">
                    <div class="shop-cart full-left">
                        <img src="static/image/cart.jpg" alt="">
                        <router-link to="/cart"> 购物车</router-link>
                    </div>
                    <div class="login-box full-left">
                        <router-link to="/login"><span>登录</span></router-link>
                        &nbsp;|&nbsp;
                        <router-link to="/register"><span>注册</span></router-link>
                    </div>
                </div>

                <div class="login-bar full-right" v-show="isShow2">
                    <div class="shop-cart full-left">
                        <img src="static/image/cart.jpg" alt="">
                        <router-link to="/cart">{{this.$store.state.cart_length}} 购物车</router-link>
                    </div>
                    <div class="login-box full-left">
                        <span>欢迎您，{{ username }}</span>
                        &nbsp;|&nbsp;
                        <router-link to="/orderlist">订单 |</router-link>
                        <router-link to="/login"><span>退出登录</span></router-link>
                    </div>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "Header",
    data() {
        return {
            link_list: [],
            isShow1: true,
            isShow2: false,
            username: '',
            token: "",
            nav_list: [],
        }
    },
    methods: {

        // 获取token验证
        get_user_status() {
            this.token = sessionStorage.token || localStorage.token;
            return this.token
        },

        // 获取导航栏
        get_list_hander() {
            this.$axios({
                url: this.$settings.HOST + 'home/hand/',
                method: 'get',
            }).then(res => {
                console.log(res.data);
                this.link_list = res.data;
            }).catch(error => {
                console.log(error);
                this.$message.error("顶部导航栏获取失败");
            })
        },

        // 用户信息显示
        load_user(){
            let username = sessionStorage.getItem('username');
            if (username){
                this.username = username;
                this.isShow1 = false;
                this.isShow2 = true;
            }else {
                this.isShow1 = true;
                this.isShow2 = false;
            }
        },

    },
    created() {
        this.get_list_hander()
        this.load_user()
        // 更新购物车数量
        // 初始化界面，向状态机提交一个动作修改购物车数量
        this.$store.commit("change_count", localStorage.cart_length);

    }
}
</script>

<style scoped>
    .header-box {
        height: 80px;
    }

    .header {
        width: 100%;
        height: 80px;
        box-shadow: 0 0.5px 0.5px 0 #c9c9c9;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        margin: auto;
        z-index: 99;
        background: #fff;
    }

    .header .content {
        max-width: 1200px;
        width: 100%;
        margin: 0 auto;
    }

    .header .content .logo {
        height: 80px;
        line-height: 80px;
        margin-right: 50px;
        cursor: pointer; /* 设置光标的形状为爪子 */
    }

    .header .content .logo img {
        vertical-align: middle;
    }

    .header .nav li {
        float: left;
        height: 80px;
        line-height: 80px;
        margin-right: 30px;
        font-size: 16px;
        color: #4a4a4a;
        cursor: pointer;
    }

    .header .nav li span {
        padding-bottom: 16px;
        padding-left: 5px;
        padding-right: 5px;
    }

    .header .nav li span a {
        display: inline-block;
    }

    .header .nav li .this {
        color: #4a4a4a;
        border-bottom: 4px solid #ffc210;
    }

    .header .nav li:hover span {
        color: #000;
    }

    .header .login-bar {
        height: 80px;
    }

    .header .login-bar .shop-cart {
        margin-right: 20px;
        border-radius: 17px;
        background: #f7f7f7;
        cursor: pointer;
        font-size: 14px;
        height: 28px;
        width: 100px;
        margin-top: 30px;
        line-height: 32px;
        text-align: center;
    }

    .header .login-bar .shop-cart:hover {
        background: #f0f0f0;
    }

    .header .login-bar .shop-cart img {
        width: 15px;
        margin-right: 4px;
        margin-left: 6px;
    }

    .header .login-bar .shop-cart span {
        margin-right: 6px;
    }

    .header .login-bar .login-box {
        margin-top: 33px;
    }

    .header .login-bar .login-box span {
        color: #4a4a4a;
        cursor: pointer;
    }

    .header .login-bar .login-box span:hover {
        color: #000000;
    }

    a {
        text-decoration: none;
        color: #333;
    }

    .member {
        display: inline-block;
        height: 34px;
        margin-left: 20px;
    }

    .member img {
        width: 26px;
        height: 26px;
        border-radius: 50%;
        display: inline-block;
    }

    .member img:hover {
        border: 1px solid yellow;
    }

    .header .login-bar .login-box1 {
        margin-top: 16px;
    }

    a:hover {
        display: inline-block;
    }
</style>
