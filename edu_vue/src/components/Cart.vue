<template>
    <div class="cart">
        <Header></Header>
        <div class="cart_info">
            <div class="cart_title">
                <span class="text">我的购物车</span>
                <span class="total">共4门课程</span>
            </div>
            <div class="cart_table">
                <div class="cart_head_row">
                    <span class="doing_row"></span>
                    <span class="course_row">课程</span>
                    <span class="expire_row">有效期</span>
                    <span class="price_row">单价</span>
                    <span class="do_more">操作</span>
                </div>
                <div class="cart_course_list">
                    <CartItem v-for="(course, index) in cart_list" :key="index" :course="course"
                    @change_selected="cart_total" @delete_cart="cart_total" @change_expire="expire_total">

                    </CartItem>
                </div>
                <div class="cart_footer_row">
                    <span class="cart_select">
                        <label>
                        <el-checkbox></el-checkbox>
                            <span>全选</span>
                        </label></span>
                    <span class="cart_delete"><i class="el-icon-delete"></i> <span>删除</span></span>
                    <span class="goto_pay"><router-link to="/order">去结算</router-link></span>
                    <span class="cart_total">总计：{{ total_price }}元</span>
                </div>
            </div>
        </div>
        <Footer></Footer>
    </div>
</template>

<script>

    import Footer from "./common/Footer";
    import Header from "./common/Header";
    import CartItem from "./CartItem";

    export default {
        name: "Cart",
        components: {
            CartItem,
            Footer,
            Header,
        },

        data() {
            return {
                token: "",
                cart_list: [],
                total_price: 0.00,  // 勾选商品总价格
            }
        },
        methods: {
            //全选
        //     checkAll(){
        //         this.inputArr.forEach(item => {
        //   item.checked = true;
        // });
        //     },

            // 向后端发请求获取购物车商品数量
            get_length(){
                let token = this.check_user_login();
                this.$axios.post(this.$settings.HOST + "cart/options/", {
                    course_id: this.course_id
                }, {
                    headers: {
                        // 由于此视图需要认证，所以需要携带token
                        "Authorization": "jwt " + token
                    },
                }).then(res => {
                    this.$message.success(res.data.message);
                    // 当添加购物车时，向状态机提交一个动作修改购物车数量
                    this.$store.commit("change_count", res.data.cart_length);
                    localStorage.cart_length = res.data.cart_length

                }).catch(error => {
                    console.log(error);
                })
            },

            // 计算购物车勾选课程的总价格
            cart_total() {
                let total = 0;
                // 遍历数组
                this.cart_list.forEach((course, key) => {
                    if (course.selected) {
                        total += parseFloat(course.price);
                    }
                })
                this.total_price = total;
            },

             // 计算购物车勾选课程的总价格
            expire_total() {
                let total = 0;
                // 遍历数组
                this.cart_list.forEach((course, key) => {
                    if (course.selected) {
                        total += parseFloat(course.expire_price);
                    }
                })
                this.total_price = total;
            },

            // 获取购物车的数据
            get_cart_list() {
                this.$axios.get(this.$settings.HOST + "cart/option/", {
                    headers: {
                        "Authorization": "jwt " + this.token
                    }
                }).then(res => {
                    console.log(res.data);
                    this.cart_list = res.data;
                    // 获取购物车总价
                    // this.cart_total();
                    this.expire_total();
                }).catch(error => {
                    console.log(error);
                })
            },

            // 用户在操作购物车时必须已经登录
            check_user_login() {
                let token = localStorage.token || sessionStorage.token;
                this.token = token;
                if (!token) {
                    let self = this;
                    this.$confirm("对不起，请登录后再添加购物车！", {
                        callback() {
                            self.$router.push("/login");
                        }
                    })
                    return false;
                }
                return token;
            },
        },

        created() {
            this.check_user_login();
            this.get_cart_list();
            this.get_length();
        },

    }
</script>

<style scoped>
    .cart_info {
        width: 1200px;
        margin: 0 auto 200px;
    }

    .cart_title {
        margin: 25px 0;
    }

    .cart_title .text {
        font-size: 18px;
        color: #666;
    }

    .cart_title .total {
        font-size: 12px;
        color: #d0d0d0;
    }

    .cart_table {
        width: 1170px;
    }

    .cart_table .cart_head_row {
        background: #F7F7F7;
        width: 100%;
        height: 80px;
        line-height: 80px;
        padding-right: 30px;
    }

    .cart_table .cart_head_row::after {
        content: "";
        display: block;
        clear: both;
    }

    .cart_table .cart_head_row .doing_row,
    .cart_table .cart_head_row .course_row,
    .cart_table .cart_head_row .expire_row,
    .cart_table .cart_head_row .price_row,
    .cart_table .cart_head_row .do_more {
        padding-left: 10px;
        height: 80px;
        float: left;
    }

    .cart_table .cart_head_row .doing_row {
        width: 78px;
    }

    .cart_table .cart_head_row .course_row {
        width: 530px;
    }

    .cart_table .cart_head_row .expire_row {
        width: 188px;
    }

    .cart_table .cart_head_row .price_row {
        width: 162px;
    }

    .cart_table .cart_head_row .do_more {
        width: 162px;
    }

    .cart_footer_row {
        padding-left: 30px;
        background: #F7F7F7;
        width: 100%;
        height: 80px;
        line-height: 80px;
    }

    .cart_footer_row .cart_select span {
        margin-left: -7px;
        font-size: 18px;
        color: #666;
    }

    .cart_footer_row .cart_delete {
        margin-left: 58px;
    }

    .cart_delete .el-icon-delete {
        font-size: 18px;
    }

    .cart_delete span {
        margin-left: 15px;
        cursor: pointer;
        font-size: 18px;
        color: #666;
    }

    .cart_total {
        float: right;
        margin-right: 62px;
        font-size: 18px;
        color: #666;
    }

    .goto_pay {
        float: right;
        width: 159px;
        height: 80px;
        outline: none;
        border: none;
        background: #ffc210;
        font-size: 18px;
        color: #fff;
        text-align: center;
        cursor: pointer;
    }
</style>
