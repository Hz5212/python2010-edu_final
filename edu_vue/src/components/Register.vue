<template>
    <div class="box">
        <img src="../../static/image/R_bg.jpg" alt="">
        <div class="register">
            <div class="register_box">
                <div class="register-title">在线平台注册</div>
                <div class="inp">
                    <input v-model="phone" type="text" placeholder="手机号码" class="user" @blur="check_phone">
                    <input v-model="password" type="password" placeholder="登录密码" class="user" @blur="check_password">

                    <div id="geetest"></div>
                    <div class="sms-box">
                        <input v-model="code" type="text" maxlength="6" placeholder="输入验证码" class="user">
                        <div class="sms-btn" @click="time_down" :disabled="disabled">{{ btnText }}</div>
                    </div>
                    <button class="register_btn" @click="user_register">注册</button>
                    <p class="go_login">已有账号
                        <router-link to="/login">直接登录</router-link>
                    </p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Register",
        data() {
            return {
                phone: "",
                password: "",
                code: "",
                disabled: false,
                interval:undefined,
                totalCount:0,
            }
        },
        methods: {
            // 检查密码格式
            check_password(){
                // 验证密码格式
                if(!(/^[a-zA-Z][a-zA-Z0-9]{6,16}$/.test(this.password))){
                    this.$alert("密码格式有误，请确认", "警告");
                    return false;
                }
            },
            //  检查手机号 是否已被注册
            check_phone() {
                // 验证手机号格式
                if(!/^1[34578]\d{9}$/.test(this.phone)){
                    this.$alert("手机号格式有误，请确认", "警告");
                    return false;
                }else {
                // 向后端发请求判断当前输入手机号是否已经被注册
                // 如果被注册，则提示当前手机号已经被占用
                // 发送请求，获取验证码
                this.$axios({
                    url: this.$settings.HOST+"user/check_phone/",
                    method: 'get',
                    params: {
                        phone: this.phone
                    }
                }).then(res=>{
                    console.log(res.data);
                }).catch(error=>{
                    console.log(error.response);
                    this.$message.error("您的信息有误");
                })
                }
            },

            // 为用户发送验证码
            get_code() {
                // 发送请求，获取验证码
                this.$axios({
                    url: this.$settings.HOST+"user/message/",
                    method: 'get',
                    params: {
                        phone: this.phone
                    }
                }).then(res=>{
                    console.log(res.data);
                }).catch(error=>{
                    console.log(error.response);
                    this.$message.error("短信发送失败或已经发送过短信");
                })

            },

            // 用户注册请求
            user_register() {
                this.$axios({
                    url: this.$settings.HOST + "user/register/",
                    method: 'post',
                    data: {
                        phone: this.phone,
                        password: this.password,
                        sms_code: this.code,
                    }
                }).then(res => {
                    // 保持登录状态
                    sessionStorage.token = res.data.token;
                    sessionStorage.username = res.data.username;
                    sessionStorage.id = res.data.id;

                    // 页面跳转
                    let self = this;
                    this.$alert("注册成功", "百知教育", {
                        callback() {
                            self.$router.push("/home");
                        }
                    })

                }).catch(error => {
                    console.log(error);
                })
            },

            // 按钮60秒倒计时
            time_down(){
                this.disabled=true
                this.totalCount=60
                this.get_code()    //60秒过倒计时过后才能调用的事件
                this.interval=setInterval(()=>{
                  this.totalCount--
                  if(this.totalCount === 0){
                    clearInterval(this.interval)
                    this.disabled=false
                  }
                },1000);
            },

        },
        computed: {
            // 计算属性监视
            btnText(){
                return this.totalCount !==0? `${this.totalCount}秒再次获取`: "获取验证码"
            }
        },
    }
</script>

<style scoped>
    .box {
        width: 100%;
        height: 100%;
        position: relative;
        overflow: hidden;
    }

    .box img {
        width: 100%;
        min-height: 100%;
    }

    .box .register {
        position: absolute;
        width: 500px;
        height: 400px;
        top: 0;
        left: 0;
        margin: auto;
        right: 0;
        bottom: 0;
        top: -338px;
    }

    .register .register-title {
        width: 100%;
        font-size: 24px;
        text-align: center;
        padding-top: 30px;
        padding-bottom: 30px;
        color: #4a4a4a;
        letter-spacing: .39px;
    }

    .register-title img {
        width: 190px;
        height: auto;
    }

    .register-title p {
        font-family: PingFangSC-Regular;
        font-size: 18px;
        color: #fff;
        letter-spacing: .29px;
        padding-top: 10px;
        padding-bottom: 50px;
    }

    .register_box {
        width: 400px;
        height: auto;
        background: #fff;
        box-shadow: 0 2px 4px 0 rgba(0, 0, 0, .5);
        border-radius: 4px;
        margin: 0 auto;
        padding-bottom: 40px;
    }

    .register_box .title {
        font-size: 20px;
        color: #9b9b9b;
        letter-spacing: .32px;
        border-bottom: 1px solid #e6e6e6;
        display: flex;
        justify-content: space-around;
        padding: 50px 60px 0 60px;
        margin-bottom: 20px;
        cursor: pointer;
    }

    .register_box .title span:nth-of-type(1) {
        color: #4a4a4a;
        border-bottom: 2px solid #84cc39;
    }

    .inp {
        width: 350px;
        margin: 0 auto;
    }

    .inp input {
        border: 0;
        outline: 0;
        width: 100%;
        height: 45px;
        border-radius: 4px;
        border: 1px solid #d9d9d9;
        text-indent: 20px;
        font-size: 14px;
        background: #fff !important;
    }

    .inp input.user {
        margin-bottom: 16px;
    }

    .inp .rember {
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: relative;
        margin-top: 10px;
    }

    .inp .rember p:first-of-type {
        font-size: 12px;
        color: #4a4a4a;
        letter-spacing: .19px;
        margin-left: 22px;
        display: -ms-flexbox;
        display: flex;
        -ms-flex-align: center;
        align-items: center;
        /*position: relative;*/
    }

    .inp .rember p:nth-of-type(2) {
        font-size: 14px;
        color: #9b9b9b;
        letter-spacing: .19px;
        cursor: pointer;
    }

    .inp .rember input {
        outline: 0;
        width: 30px;
        height: 45px;
        border-radius: 4px;
        border: 1px solid #d9d9d9;
        text-indent: 20px;
        font-size: 14px;
        background: #fff !important;
    }

    .inp .rember p span {
        display: inline-block;
        font-size: 12px;
        width: 100px;
        /*position: absolute;*/
        /*left: 20px;*/

    }

    #geetest {
        margin-top: 20px;
    }

    .register_btn {
        width: 100%;
        height: 45px;
        background: #84cc39;
        border-radius: 5px;
        font-size: 16px;
        color: #fff;
        letter-spacing: .26px;
        margin-top: 30px;
    }

    .inp .go_login {
        text-align: center;
        font-size: 14px;
        color: #9b9b9b;
        letter-spacing: .26px;
        padding-top: 20px;
    }

    .inp .go_login span {
        color: #84cc39;
        cursor: pointer;
    }

    .sms-box {
        position: relative;
    }

    .sms-btn {
        font-size: 14px;
        color: #ffc210;
        letter-spacing: .26px;
        position: absolute;
        right: 16px;
        top: 10px;
        cursor: pointer;
        overflow: hidden;
        background: #fff;
        border-left: 1px solid #484848;
        padding-left: 16px;
        padding-bottom: 4px;
    }
</style>
