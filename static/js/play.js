const { createApp} = Vue;
const vm = createApp({
  delimiters:['%{', '}%'],
  data(){
               return {
               playingPc : false,
               playingPi : false,
               mp3Pc : '',
               mp3Pi : '',
               mp3Pc_i : 0,
               mp3Pi_i : 0,
               num4dPc : [0,0,0,0],
               num4dPi : [0,0,0,0],
               num4dPc_i : 4,
               num4dPi_i : 4,
               dir :"/static/assets/",
               mp3_list : [],
               mp3_i_max : 0 ,
               keytimerPc : null,
               keytimerPi : null,
               keytimerPcRunning: false,
               keytimerPiRunning: false,
               radioPlayingPcNo: 0,
               radioPlayingPiNo: 0,
               //broswer audio play src
               BBCurl:"https://stream.live.vc.bbcmedia.co.uk/bbc_world_service",
               CNNurl:"https://npr-ice.streamguys1.com/live.mp3",
               NPRurl:"https://npr-ice.streamguys1.com/live.mp3",
               FOXurl:"https://prod-18-232-88-129.wostreaming.net/foxnewsradio-foxnewsradioaac-imc?session-id=0f99acd44126cef33b40ce217c9ea1ad",
               MSCurl:"https://npr-ice.streamguys1.com/live.mp3",
               BLBurl:"https://npr-ice.streamguys1.com/live.mp3",
               TPEurl:"https://npr-ice.streamguys1.com/live.mp3",
               ICRurl:"https://icrt.leanstream.co/ICRTFM-MP3?args=web",
               WWXurl:"https://eclassicalradiow-hichannel.cdn.hinet.net/live/RA000018/media_641018.ts"
                }
          },
  methods:{
            getRandom(min,max){
              return Math.floor(Math.random()*(max-min+1))+min;
            },
            loading(){
                axios.post('/').then(res => {
                this.mp3Pi_i=res.data.mp3Pi_i;
                this.playingPi=res.data.playingPi;
                this.mp3_list = res.data.mp3_list;
                this.radioPlayingPiNo = res.data.radioPlayingPiNo;   
                this.mp3_i_max = this.mp3_list.length;
                rn = this.getRandom(this.mp3_i_max-1, 0);
                //rn = rn % this.mp3_i_max;
                this.mp3Pc_i=rn;
                this.mp3Pc=this.mp3_list[rn];
                this.mp3Pi=this.mp3_list[this.mp3Pi_i];
                console.log("mp3Pc: "+this.mp3Pc);
                console.log("mp3Pi: "+this.mp3Pi);
                console.log("payingPi: "+this.playingPi);
                  });
             },
             playSelectSongPc(){
                num=this.num4dPc.join("");
                num = num-1;
                console.log("current keyno is: "+num);
                this.mp3Pc_i= num % this.mp3_i_max;
                this.mp3Pc=this.mp3_list[this.mp3Pc_i];
                console.log(this.dir+this.mp3_list[this.mp3Pc_i]);
                dirmp3Pc=this.dir+this.mp3_list[this.mp3Pc_i];
                document.getElementById("my-audio").pause();
                document.getElementById("my-audio").setAttribute('src',dirmp3Pc);
                document.getElementById("my-audio").load();
                document.getElementById("my-audio").play();
                this.playingPc = true;
                this.num4dPc[0]=0;
                this.num4dPc[1]=0;
                this.num4dPc[2]=0;
                this.num4dPc[3]=0;
                this.keytimerPcRunning = false;
                
             },
             keyInputPc(keyno){
                if(this.keytimerPcRunning == true){
                  clearTimeout(this.keytimerPc);
                  this.keytimerPcRunning = false;
                  }
                this.num4dPc_i= this.num4dPc_i - 1;
                if(this.num4dPc_i< 0){
                    this.num4dPc_i = 3 };
                this.num4dPc[0] = this.num4dPc[1]; 
                this.num4dPc[1] = this.num4dPc[2];
                this.num4dPc[2] = this.num4dPc[3];
                this.num4dPc[3] = keyno ;
                this.keytimerPc=setTimeout(this.playSelectSongPc,3000);
                this.keytimerPcRunning = true;
                },
            playPausePc(event){
                dirmp3Pc=this.dir+this.mp3_list[this.mp3Pc_i];
                document.getElementById("my-audio").setAttribute('src',dirmp3Pc);
                if(this.playingPc == false){
                document.getElementById("my-audio").play();
                this.playingPc = true;
                console.log("playPausePc to Play"); 
                }
                else{
                document.getElementById("my-audio").pause();
                this.playingPc = false;
                console.log("playPausePc to Pause"); 
                }
           	  },
            playPrePc(event){
                this.mp3Pc_i = this.mp3Pc_i-1
                if(this.mp3Pc_i < 0){
                  this.mp3Pc_i = this.mp3_i_max - 1;
                  }
                this.mp3Pc=this.mp3_list[this.mp3Pc_i];
                dirmp3Pc=this.dir+this.mp3_list[this.mp3Pc_i];
                document.getElementById("my-audio").setAttribute('src',dirmp3Pc);
                document.getElementById("my-audio").load();
                document.getElementById("my-audio").play();
                this.playingPc = true; 
                console.log(this.mp3Pc_i);
                console.log(this.mp3Pc);
                console.log("playPrePc works");
              },
            playNextPc(event){
                this.mp3Pc_i = this.mp3Pc_i+1
                if(this.mp3Pc_i >= this.mp3_i_max){
                  this.mp3Pc_i = 0;
                  }
                this.mp3Pc=this.mp3_list[this.mp3Pc_i];
                dirmp3Pc=this.dir+this.mp3_list[this.mp3Pc_i];
                document.getElementById("my-audio").pause();
                document.getElementById("my-audio").setAttribute('src',dirmp3Pc);
                document.getElementById("my-audio").load();
                document.getElementById("my-audio").play();
                this.playingPc = true;
                console.log(this.mp3Pc_i);
                console.log(this.mp3Pc);
                console.log("playNextPc works");
              },
            playRadioPc(radioNo){
                let url = "";
                if(this.radioPlayingPcNo == radioNo){
                document.getElementById("my-radio").pause();
                this.radioPlayingPcNo = 0;
                console.log("Raido No: "+this.radioPlayingPcNo);
                      }
                else{
                document.getElementById("my-radio").pause();
                switch(radioNo){
                      case 1 :{ url = this.BBCurl;  break;}
                      case 2 :{ url = this.CNNurl;  break;}
                      case 3 :{ url = this.NPRurl;  break;}
                      case 4 :{ url = this.FOXurl;  break;}
                      case 5 :{ url = this.NPRurl;  break;}
                      case 6 :{ url = this.NPRurl;  break;}
                      case 7 :{ url = this.TPEurl;  break;}
                      case 8 :{ url = this.ICRurl;  break;}
                      case 9 :{ url = this.WWXurl;  break;}
                      default :{break;}
                      }
                document.getElementById("my-radio").setAttribute('src',url);
                document.getElementById("my-radio").load();
                document.getElementById("my-radio").play();
                this.radioPlayingPcNo = radioNo;
                console.log("Radio No: "+this.radioPlayingPcNo);
                }
              },
            playSelectedPi(){
                num=this.num4dPi.join("");
                axios.post('/playSelectedPi',{"num":num}).then(res => {
                this.playingPi = res.data.playingPi;
                this.mp3Pi_i = res.data.mp3Pi_i;
                this.mp3Pi=this.mp3_list[this.mp3Pi_i];
                console.log("works playSelectedPi");
                  })
                  .catch(error => {
                  console.log("handle error =>", error);
                  })
                this.num4dPi[0]=0;
                this.num4dPi[1]=0;
                this.num4dPi[2]=0;
                this.num4dPi[3]=0;
              },
            keyInputPi(keyno){
                if(this.keytimerPiRunning == true){
                  clearTimeout(this.keytimerPi);
                  this.keytimerPiRunning = false;
                  }
                this.num4dPi_i= this.num4dPi_i - 1;
                if(this.num4dPi_i< 0){
                    this.num4dPi_i = 3 };
                this.num4dPi[0] = this.num4dPi[1]; 
                this.num4dPi[1] = this.num4dPi[2];
                this.num4dPi[2] = this.num4dPi[3];
                this.num4dPi[3] = keyno ;
                this.keytimerPi=setTimeout(this.playSelectedPi,3000);
                this.keytimerPiRunning = true;
              },
             playPausePi(event){
                axios.post('/playPausePi').then(res => {
                this.playingPi = res.data.playingPi; 
                this.mp3Pi_i = res.data.mp3Pi_i;
                this.mp3Pi = this.mp3_list[res.data.mp3Pi_i];
                console.log("works playPausePi");
                })
                .catch(error => {
                console.log("handle error =>", error);
                })
           	  },
             playPrePi(event){
                axios.post('/playPrePi').then(res => {
                this.mp3Pi_i = res.data.mp3Pi_i;
                this.mp3Pi = this.mp3_list[res.data.mp3Pi_i];
                console.log("playPrePi works");
                })
                .catch(error => {
                console.log("handle error =>", error);
                })
              },
            playNextPi(event){
                axios.post('/playNextPi').then(res => {
                this.mp3Pi_i = res.data.mp3Pi_i;
                this.mp3Pi = this.mp3_list[res.data.mp3Pi_i];
                dir_mp3Pi = this.dir+this.mp3_list[this.mp3Pi_i];
                console.log("playNextPi works");
                })
                .catch(error => {
                console.log("handle error =>", error);
                })
              },
            playRadioPi(radioNo){
                if(this.radioPlayingPiNo == radioNo){
                   this.radioPlayingPiNo = 0 ;

                }else{this.radioPlayingPiNo =radioNo;} 
                console.log("BerfoeNo:"+ this.radioPlayingPiNo);
                axios.post('/playRadioPi',{"radioNo":this.radioPlayingPiNo}).then(res => {
                this.radioPlayingPiNo = res.data.radioPlayingPiNo;
                console.log("AfterNo:"+ this.radioPlayingPiNo);
                console.log("playRadioPi works");
                })
                .catch(error => {
                console.log("handle error =>", error);
                })
              }
          },
  created:  function(){
                this.loading();
          }
           
       })

  vm.mount('#app');
//   my-Audio.addEventListener("ended", playnext);
