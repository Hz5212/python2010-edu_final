<template>
    <el-carousel height="720px" :interval="3000" arrow="always">
        <el-carousel-item v-for="(image, index) in image_list" :key="index">
            <a :href="image.link"><img :src="image.image_url" alt=""></a>
        </el-carousel-item>
    </el-carousel>
</template>

<script>
export default {
    name: "Banner",
    data(){
        return{
            image_list : [],
        }
    },
    methods:{
      // 获取轮播图
      get_image_list(){
          this.$axios({
              url: this.$settings.HOST + 'home/image/',
              method: 'get',
          }).then(res => {
              console.log(res.data);
              this.image_list = res.data;
          }).catch(error => {
              console.log(error);
              this.$message.error("轮播图获取失败")
          })
      },
    },
    created() {
        this.get_image_list()
    }
}
</script>

<style scoped>
  .el-carousel__item h3 {
    color: #475669;
    font-size: 18px;
    opacity: 0.75;
    line-height: 300px;
    margin: 0;
  }

  .el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
  }

  .el-carousel__item:nth-child(2n+1) {
    background-color: #d3dce6;
  }</style>
