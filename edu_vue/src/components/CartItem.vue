<template>
    <div class="cart_item">
        <div class="cart_column column_1">
            <el-checkbox class="my_el_checkbox" v-model="course.selected"></el-checkbox>
        </div>
        <div class="cart_column column_2">
            <img :src="course.image" alt="">
<!--            <router-link to="/course/detail/1">{{course.name}}</router-link>-->
            <span>{{course.name}}</span>
        </div>
        <div class="cart_column column_3">
            <el-select v-model="course.expire_id" size="mini" placeholder="请选择购买有效期" class="my_el_select">
                 <el-option v-for="item in course.expire_list" :label="item.expire_text" :value="item.id"
                           :key="item.id">
                 </el-option>
            </el-select>
        </div>
        <div class="cart_column column_4" v-if="course.expire_id<0">{{ course.price }}元</div>
        <div class="cart_column column_4" v-else>{{course.expire_price}}元</div>
        <div class="cart_column column_4" @click="delete_cart">删除</div>
    </div>
</template>

<script>
    export default {
        name: "CartItem",
        inject:['reload'],
        // 在子组件内部接收到了父组件传递的值
        props: ['course'],
        watch: {
            // 监听勾选状态是否发生了变化
            "course.selected": function () {
                this.change_course_select();
            },

            // 监听有效期是否发生了改变
            "course.expire_id": function () {
                this.change_expire();
            }
        },
        data() {
            return {
                checked: this.course.selected,
                course_id: this.course.course_id,
                expire_id: this.course.expire_id,

            }
        },
        methods: {

            // 发起请求，修改redis中的有效期
            change_expire() {
                let token = localStorage.token || sessionStorage.token;
                // 向后端发请求，修改redis中课程的有效期
                this.$axios.put(this.$settings.HOST+"cart/options/",{
                    expire_id: this.course.expire_id,
                    course_id: this.course.course_id,
                },{
                    headers:{
                        "Authorization": "jwt " + token,
                    },
                }).then(res=>{
                    console.log(res);
                    this.$parent.get_cart_list();

                    // 更新切换有效期的价格
                    // 向父子件提交事件，重新计算总价
                    this.$emit("expire_total");

                }).catch(error => {
                    console.log(error);
                })
            },

            // 发起请求修改redis中的选中状态
            change_course_select() {
                let token = localStorage.token || sessionStorage.token;
                this.$axios.patch(this.$settings.HOST + "cart/option/",{
                    course_id: this.course_id,
                    selected: this.checked,
                },{
                    headers:{
                        "Authorization": "jwt " + token,
                    },
                }).then(res => {
                    console.log(res);
                    if (!this.checked) {
                        this.$message('已勾选 ' + this.course.name);
                        this.checked = !this.checked;
                    } else {
                        this.$message('取消勾选 ' + this.course.name);
                        this.checked = !this.checked;
                    }
                    // 当修改购物车商品时，向状态机提交一个动作修改购物车商品数量
                    this.$store.commit("change_count", res.data.cart_length);
                    localStorage.cart_length = res.data.cart_length
                    // 当修改成功后，子组件通知父组件重新计算购物车中商品的总价格
                    // 向父组件提交事件
                    this.$emit("change_selected");
                }).catch(error => {
                    console.log(error);
                })
            },

            // 删除
            delete_cart(){
                let token = localStorage.token || sessionStorage.token;
                this.$axios.put(this.$settings.HOST + "cart/option/",{
                    course_id: this.course_id,
                    selected: this.checked,
                },{
                    headers:{
                        "Authorization": "jwt " + token,
                    },
                }).then(res => {
                    console.log(res);
                    this.$message('删除成功 ' + this.course.name);
                    // 当删除购物车商品时，向状态机提交一个动作修改购物车商品数量
                    this.$store.commit("change_count", res.data.cart_length);
                    localStorage.cart_length = res.data.cart_length
                    // 当删除成功后，子组件通知父组件重新计算购物车中商品的总价格
                    // 向父组件提交事件
                    this.$emit("delete_cart");
                    // this.$emit("change_selected");
                    this.reload();

                }).catch(error => {
                    console.log(error);
                })
            }

        },
    }
</script>

<style scoped>
    .cart_item::after {
        content: "";
        display: block;
        clear: both;
    }

    .cart_column {
        float: left;
        height: 250px;
    }

    .cart_item .column_1 {
        width: 88px;
        position: relative;
    }

    .my_el_checkbox {
        position: absolute;
        left: 0;
        right: 0;
        bottom: 0;
        top: 0;
        margin: auto;
        width: 16px;
        height: 16px;
    }

    .cart_item .column_2 {
        padding: 67px 10px;
        width: 520px;
        height: 116px;
    }

    .cart_item .column_2 img {
        width: 175px;
        height: 115px;
        margin-right: 35px;
        vertical-align: middle;
    }

    .cart_item .column_3 {
        width: 197px;
        position: relative;
        padding-left: 10px;
    }

    .my_el_select {
        width: 117px;
        height: 28px;
        position: absolute;
        top: 0;
        bottom: 0;
        margin: auto;
    }

    .cart_item .column_4 {
        padding: 67px 10px;
        height: 116px;
        width: 142px;
        line-height: 116px;
    }

</style>
