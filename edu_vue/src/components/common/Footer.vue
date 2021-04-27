<template>
    <div class="footer">
        <ul>
             <li v-for="(link, index) in link_list" :key="index">
                 <a :href="link.link" v-if="link.is_site">{{ link.title }}</a>
                 <router-link v-else :to="link.link">{{ link.title }}</router-link>
             </li>
        </ul>
    </div>
</template>

<script>
export default {
    name: "Footer",
    data(){
        return {
            link_list: [],
        }
    },
    methods: {
        // 获取导航栏
        get_list_footer(){
              this.$axios({
                  url: this.$settings.HOST + 'home/foot/',
                  method: 'get',
              }).then(res=>{
                  console.log(res.data);
                  this.link_list = res.data;
              }).catch(error=>{
                  console.log(error);
                  this.$message.error("尾部导航栏获取失败");
              })
        },
    },
    created() {
        this.get_list_footer()
    }
}
</script>

<style scoped>
      .footer {
        width: 100%;
        height: 128px;
        background: #25292e;
        color: #fff;
      }

      .footer ul {
        margin: 0 auto 16px;
        padding-top: 38px;
        width: 810px;
      }

      .footer ul li {
        float: left;
        width: 112px;
        margin: 0 10px;
        text-align: center;
        font-size: 14px;

      }

      .footer ul li a {
          color: white;
      }

      .footer ul:after {
        content: "";
        display: block;
        clear: both;
      }

      .footer p {
        text-align: center;
        font-size: 12px;
      }
</style>
