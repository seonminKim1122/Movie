<template>
  <div class="content-container">
    <img class="left-arrow" src="@/assets/arrow-left-circle.svg" @click="goback()"/>
    <div class="contents">
      <p class="title">내가 만든 파티</p>
      <!-- 내가 만든 파티가 있을 때 -->
      <MyPartyCreated v-if="store.parties.own && store.parties.own.length > 0" :own-parties="store.parties.own"/>
      <div v-else class="content">
        <RouterLink :to="{name: 'PartyCreateView'}">
          <div class="join-btn">
            <img src="@/assets/person-add.svg" alt="">
            <p class="description">파티 생성하기!</p>
          </div>
        </RouterLink>
        <p>내가 만든 파티가 아직 없어요!</p>
      </div>

      <p class="title">내가 참여중인 파티</p>
      <!-- 내가 참여중인 파티가 있을 때 -->
      <MyPartyJoined v-if="store.parties.participate && store.parties.participate.length > 0" :participate-parties="store.parties.participate"/>
      <!-- 내가 참여중인 파티가 없을 때 -->
      <div v-else class="content">
        <RouterLink :to="{name: 'PartyJoinView'}">
          <div class="join-btn">
            <img src="@/assets/box-arrow-in-right.svg" alt="">
            <p class="description">파티 참여하기!</p>
          </div>
        </RouterLink>
        <p>내가 참여중인 파티가 아직 없어요!</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import MyPartyCreated from '@/components/otts/MyPartyCreated.vue';
import MyPartyJoined from '@/components/otts/MyPartyJoined.vue';
import { useMovieStore } from '@/stores/movie';
import { onMounted } from 'vue';
import { RouterLink } from 'vue-router';
import { useRouter } from 'vue-router';

// 내가 개설한 파티가 있을 때 없을 때 
// 내가 참여중인 파티가 있을 때 없을 때
// 구분해서 구성요소를 보여주는 로직이 필요합니다.
const store = useMovieStore();
// const {parties, getParties} = store;

onMounted(() => {
  store.getParties();
});

const router = useRouter()
const goback = function() {
  router.go(-1);
}
</script>

<style scoped>
.content-container {
  border: 1px solid #595959;
  border-radius: 2rem;

  width: min(75%, 1000px);
  height: 60vh;

  overflow: auto;
}
.content-container::-webkit-scrollbar {
    width: 20px; /* 스크롤바의 너비 */
}

.content-container::-webkit-scrollbar-thumb {
    height: 50%; /* 스크롤바의 길이 */
    background: #595959; /* 스크롤바의 색상 */
    background-clip: padding-box;
    border:8px solid transparent;
    border-radius: 20px;
    border-top-width: 100px;
    border-bottom-width: 100px;
}

.content-container::-webkit-scrollbar-track {
    background: transparent /*스크롤바 뒷 배경 색상*/
}

.left-arrow {
  width: 45px;
  height: 45px;

  margin-top: 5%;
  margin-left: 5%;
}

.contents {
  width: 80%;
  margin-left: 10%;

  margin-bottom: 10%;
}

.title {
  font-size: 24px;
  font-weight: bold;

  margin-top: min(5%, 30px);
  margin-bottom: min(5%, 30px);
}

.content {
  display: flex;
  flex-direction: column;
  align-items: center;
}

a {
  text-decoration: none;
}

.join-btn {
  border: 1px solid #595959;
  border-radius: 1rem;

  display: flex;
  align-items: center;
  justify-content: center;

  width: 265px;
  height: 78px;

  padding-right: 55px;

  margin-bottom: 10px;

  padding-left: 40px;
  padding-right: 55px;

  cursor: pointer;
}

.join-btn:hover {
  background-color: #191919;
}

.description {
  margin-bottom: 0px;
  font-size: 18px;

  margin-left: auto;
}
</style>