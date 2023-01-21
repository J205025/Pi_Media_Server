const { createApp} = Vue;
const vm = createApp({
  delimiters:['%{', '}%'],
  data(){
               return {
               musicPcPlaying : false,
               musicPiPlaying : false,
               musicPcPlayMode : 2,
               musicPiPlayMode : 2,
               fileList : [],
               dir :"/home/share/Music/",
               filePc: '',
               filePi : '',
               indexPc : 0,
               indexPi : 0,
               indexMax : 0 ,
               num4dPc : [0,0,0,0],
               num4dPi : [0,0,0,0],
               num4dPc_i : 4,
               num4dPi_i : 4,
               keytimerPc : null,
               keytimerPi : null,
               keytimerPcRunning: false,
               keytimerPiRunning: false,
               radioPiPlayingNo: 0,
               radioPcPlayingNo: 0,
               volumePc : 0.65,
               volumePi : 0.65,
               volumePcMute : false,
               volumePiMute : false,
               //broswer audio play src
               url01:"https://stream.live.vc.bbcmedia.co.uk/bbc_world_service",
               url02:"http://stream.live.vc.bbcmedia.co.uk/bbc_london",
               url03:"https://npr-ice.streamguys1.com/live.file",
               url04:"https://prod-18-232-88-129.wostreaming.net/foxnewsradio-foxnewsradioaac-imc?session-id=0f99acd44126cef33b40ce217c9ea1ad",
               url05:"http://stream.live.vc.bbcmedia.co.uk/bbc_radio_five_live",
               url06:"http://stream.live.vc.bbcmedia.co.uk/bbc_asian_network",
               url07:"http://stream.live.vc.bbcmedia.co.uk/bbc_radio_one",
               url08:"https://icrt.leanstream.co/ICRTFM-MP3?args=web",
               url09:"http://stream.live.vc.bbcmedia.co.uk/bbc_radio_two",
               url10:"http://192.168.1.146:8000/stream.ogg",
               url11:"http://onair.family977.com.tw:8000/live.file",
               url12:"https://n09.rcs.revma.com/aw9uqyxy2tzuv?rj-ttl=5&rj-tok=AAABhZollCEACdvxzVVN61ARVg",
               url13:"https://n10.rcs.revma.com/ndk05tyy2tzuv?rj-ttl=5&rj-tok=AAABhZouFPAAQudE3-49-1PFHQ",
               url14:"https://n09.rcs.revma.com/7mnq8rt7k5zuv?rj-ttl=5&rj-tok=AAABhZovh0cASZAucd0xcmxkvQ",
               url15:"https://n11a-eu.rcs.revma.com/em90w4aeewzuv?rj-tok=AAABhZoyef8AtFfbdaYYtKJnaw&rj-ttl=5",
               url16:"https://n07.rcs.revma.com/78fm9wyy2tzuv?rj-ttl=5&rj-tok=AAABhZozdbQAkV-tPDO6A5aHag",
               url17:"http://stream.live.vc.bbcmedia.co.uk/bbc_radio_three",
               url18:"http://stream.live.vc.bbcmedia.co.uk/bbc_radio_fourfm",
               url19:"http://stream.live.vc.bbcmedia.co.uk/bbc_6music",
               url20:"http://media-ice.musicradio.com:80/ClassicFMMP3",
               url21:"https://prod-18-232-88-129.wostreaming.net/foxnewsradio-foxnewsradioaac-imc?session-id=0f99acd44126cef33b40ce217c9ea1ad",
               url22:"https://prod-18-232-88-129.wostreaming.net/foxnewsradio-foxnewsradioaac-imc?session-id=0f99acd44126cef33b40ce217c9ea1ad",
               url23:"https://prod-18-232-88-129.wostreaming.net/foxnewsradio-foxnewsradioaac-imc?session-id=0f99acd44126cef33b40ce217c9ea1ad",
               url24:"https://prod-18-232-88-129.wostreaming.net/foxnewsradio-foxnewsradioaac-imc?session-id=0f99acd44126cef33b40ce217c9ea1ad",
               url25:"https://prod-18-232-88-129.wostreaming.net/foxnewsradio-foxnewsradioaac-imc?session-id=0f99acd44126cef33b40ce217c9ea1ad",
               url26:"https://prod-18-232-88-129.wostreaming.net/foxnewsradio-foxnewsradioaac-imc?session-id=0f99acd44126cef33b40ce217c9ea1ad",
               url27:"https://prod-18-232-88-129.wostreaming.net/foxnewsradio-foxnewsradioaac-imc?session-id=0f99acd44126cef33b40ce217c9ea1ad",
               url28:"https://prod-18-232-88-129.wostreaming.net/foxnewsradio-foxnewsradioaac-imc?session-id=0f99acd44126cef33b40ce217c9ea1ad",
               url29:"https://prod-18-232-88-129.wostreaming.net/foxnewsradio-foxnewsradioaac-imc?session-id=0f99acd44126cef33b40ce217c9ea1ad",
               url30:"http://media-ice.musicradio.com:80/ClassicFMMP3"
                }
          },
  methods:{
            getRandom(min,max){
              return Math.floor(Math.random()*(max-min+1))+min;
            },
            loading(){
                axios.post('/').then(res => {
                this.indexPi=res.data.indexPi;
                this.musicPiPlaying=res.data.musicPiPlaying;
                this.fileList = res.data.fileList;
                this.radioPiPlayingNo = res.data.radioPiPlayingNo;   
                this.indexMax = this.fileList.length;
                this.volumePi= res.data.volumePi;
                this.volumePiMute= res.data.volumePiMute;
                rn = this.getRandom(this.indexMax-1, 0);
                //rn = rn % this.indexMax;
                this.indexPc=rn;
                this.filePc=this.fileList[rn];
                this.filePi=this.fileList[this.indexPi];
                console.log("filePc: "+this.filePc);
                console.log("filePi: "+this.filePi);
                console.log("musicPiPaying: "+this.musicPiPlaying);
                console.log("radioPiPlayingNo: "+this.radioPiPlayingNo);
                console.log("volumePi: "+this.volumePi);
                console.log("volumePiMute: "+this.volumePiMute);
                var vid1 = document.getElementById("my-audio");
                vid1.volumePc = this.volumePc; 
                var vid2 = document.getElementById("my-radio");
                vid2.volumePc = this.volumePc;

                if(this.radioPiPlayingNo==0){
                  element = document.getElementById("sel10Pi");
                  element.value = "0"
                  element = document.getElementById("sel20Pi");
                  element.value = "0"
                  element = document.getElementById("sel30Pi");
                  element.value = "0"
                }
                else if(this.radioPiPlayingNo>0 && this.radioPiPlayingNo <11){
                  element = document.getElementById("sel20Pi");
                  element.value = "0"
                  element = document.getElementById("sel30Pi");
                  element.value = "0"
                  element = document.getElementById("sel10Pi");
                  element.value = this.radioPiPlayingNo 
                }
                else if(  this.radioPiPlayingNo>11 &&this.radioPiPlayingNo<21){
                  element = document.getElementById("sel10Pi");
                  element.value = "0"
                  element = document.getElementById("sel30Pi");
                  element.value = "0"
                  element = document.getElementById("sel20Pi");
                  element.value = this.radioPiPlayingNo 
                }
                else{
                  element = document.getElementById("sel10");
                  element.value ="0"
                  element = document.getElementById("sel20");
                  element.value = "0"
                  element = document.getElementById("sel30");
                  element.value = this.radioPiPlayingNo 
                }

              });
             },
             playSelectedPc(){
                num=this.num4dPc.join("");
                num = num-1;
                console.log("current keyno is: "+num);
                this.indexPc= num % this.indexMax;
                this.filePc=this.fileList[this.indexPc];
                console.log(this.dir+this.fileList[this.indexPc]);
                dirfilePc=this.dir+this.fileList[this.indexPc];
                document.getElementById("my-audio").pause();
                document.getElementById("my-audio").setAttribute('src',dirfilePc);
                document.getElementById("my-audio").load();
                document.getElementById("my-audio").play();
                this.musicPcPlaying = true;
                this.num4dPc[0]=0;
                this.num4dPc[1]=0;
                this.num4dPc[2]=0;
                this.num4dPc[3]=0;
                this.keytimerPcRunning = false;
             },
             setPlayModePc(mode){
                this.musicPcPlayMode = this.musicPcPlayMode % 3;
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
                this.keytimerPc=setTimeout(this.playSelectedPc,3000);
                this.keytimerPcRunning = true;
                },
            playPausePc(event){
                dirfilePc=this.dir+this.fileList[this.indexPc];
                document.getElementById("my-audio").setAttribute('src',dirfilePc);
                if(this.musicPcPlaying == false){
                document.getElementById("my-audio").play();
                this.musicPcPlaying = true;
                console.log("playPausePc to Play"); 
                }
                else{
                document.getElementById("my-audio").pause();
                this.musicPcPlaying = false;
                console.log("playPausePc to Pause"); 
                }
           	  },
            playPrePc(event){
                this.indexPc = this.indexPc-1
                if(this.indexPc < 0){
                  this.indexPc = this.indexMax - 1;
                  }
                this.filePc=this.fileList[this.indexPc];
                dirfilePc=this.dir+this.fileList[this.indexPc];
                document.getElementById("my-audio").setAttribute('src',dirfilePc);
                document.getElementById("my-audio").load();
                document.getElementById("my-audio").play();
                this.musicPcPlaying = true; 
                console.log(this.indexPc);
                console.log(this.filePc);
                console.log("playPrePc works");
              },
            playNextPc(event){
                this.indexPc = this.indexPc+1
                if(this.indexPc >= this.indexMax){
                  this.indexPc = 0;
                  }
                this.filePc=this.fileList[this.indexPc];
                dirfilePc=this.dir+this.fileList[this.indexPc];
                document.getElementById("my-audio").pause();
                document.getElementById("my-audio").setAttribute('src',dirfilePc);
                document.getElementById("my-audio").load();
                document.getElementById("my-audio").play();
                this.musicPcPlaying = true;
                console.log(this.indexPc);
                console.log(this.filePc);
                console.log("playNextPc works");
              },
            volumeDownPc(event){
                var vid1 = document.getElementById("my-audio");
                var vid2 = document.getElementById("my-radio");
                this.volumePc = this.volumePc - 0.2;
                if(this.volumePc < 0 ){this.volumePc =0;}
                vid1.volumePc = this.volumePc; 
                vid2.volumePc = this.volumePc; 
              },
            volumeUpPc(event){
                var vid1 = document.getElementById("my-audio");
                var vid2 = document.getElementById("my-radio");
                this.volumePc = this.volumePc + 0.2;
                if(this.volumePc > 1){this.volumePc =1;}
                vid1.volumePc = this.volumePc; 
                vid2.volumePc = this.volumePc; 
              },
            volumeMutePc(event){
                var vid1 = document.getElementById("my-audio");
                var vid2 = document.getElementById("my-radio");
                if(this.volumePc != 0 ){this.volumePc =0;}
                vid1.volumePc = 0; 
                vid2.volumePc = 0; 
              },
            playRadioPc(event){
                this.radioPlayingPcNo = event.target.value;
                console.log("this.radioPlayingPcNo:"+this.radioPlayingPcNo);
                if(this.radioPlayingPcNo==0){
                  element = document.getElementById("sel10Pc");
                  element.value = 0
                  element = document.getElementById("sel20Pc");
                  element.value = 0
                  element = document.getElementById("sel30Pc");
                  element.value = 0
                }
                else if(this.radioPlayingPcNo>0 && this.radioPlayingPcNo <11){
                  element = document.getElementById("sel20Pc");
                  element.value = 0
                  element = document.getElementById("sel30Pc");
                  element.value = 0
                  element = document.getElementById("sel10Pc");
                  element.value = this.radioPlayingPcNo 
                }
                else if( this.radioPlayingPcNo>11 && this.radioPlayingPcNo<21){
                  element = document.getElementById("sel10Pc");
                  element.value = 0
                  element = document.getElementById("sel30Pc");
                  element.value = 0
                  element = document.getElementById("sel20Pc");
                  element.value = this.radioPlayingPcNo 
                }
                else{
                  element = document.getElementById("sel10Pc");
                  element.value = 0
                  element = document.getElementById("sel20Pc");
                  element.value = 0
                  element = document.getElementById("sel30Pc");
                  element.value = this.radioPlayingPcNo 
                }
                let url = "";
                if(this.radioPlayingPcNo == 0){
                document.getElementById("my-radio").pause();
                      }
                else{
                document.getElementById("my-radio").pause();
                switch (this.radioPlayingPcNo) {
                      case "1" : { url = this.url01;  break;}
                      case "2" : { url = this.url02;  break;}
                      case "3" : { url = this.url03;  break;}
                      case "4" : { url = this.url04;  break;}
                      case "5" : { url = this.url05;  break;}
                      case "6" : { url = this.url06;  break;}
                      case "7" : { url = this.url07;  break;}
                      case "8" : { url = this.url08;  break;}
                      case "9" : { url = this.url09;  break;}
                      case "10" : { url = this.url10;  break;}
                      case "11" : { url = this.url11;  break;}
                      case "12" : { url = this.url12;  break;}
                      case "13" : { url = this.url13;  break;}
                      case "14" : { url = this.url14;  break;}
                      case "15" : { url = this.url15;  break;}
                      case "16" : { url = this.url16;  break;}
                      case "17" : { url = this.url17;  break;}
                      case "18" : { url = this.url18;  break;}
                      case "19" : { url = this.url19;  break;}
                      case "20" : { url = this.url20;  break;}
                      case "21" : { url = this.url21;  break;}
                      case "22" : { url = this.url21;  break;}
                      case "23" : { url = this.url23;  break;}
                      case "24" : { url = this.url24;  break;}
                      case "25" : { url = this.url25;  break;}
                      case "26" : { url = this.url26;  break;}
                      case "27" : { url = this.url27;  break;}
                      case "28" : { url = this.url28;  break;}
                      case "29" : { url = this.url29;  break;}
                      case "30" : { url = this.url30;  break;}
                      default : {url = this.url01; break;}
                      }
                console.log("url:"+url);
                document.getElementById("my-radio").setAttribute('src',url);
                document.getElementById("my-radio").load();
                document.getElementById("my-radio").play();
                console.log("radioPcPlayingNo: "+this.radioPcPlayingPcNo);
                }
              },

            playSelectedPi(){
                num=this.num4dPi.join("");
                axios.post('/playSelectedPi',{"num":num}).then(res => {
                this.musicPiPlaying = res.data.musicPiPlaying;
                this.indexPi = res.data.indexPi;
                this.filePi=this.fileList[this.indexPi];
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
             setPlayModePi(mode){
                this.musicPiPlayMode = this.musicPiPlayMode % 3;
             },
             playPausePi(event){
                axios.post('/playPausePi').then(res => {
                this.musicPiPlaying = res.data.musicPiPlaying; 
                this.indexPi = res.data.indexPi;
                this.filePi = this.fileList[res.data.indexPi];
                console.log("works playPausePi");
                })
                .catch(error => {
                console.log("handle error =>", error);
                })
           	  },
             playPrePi(event){
                axios.post('/playPrePi').then(res => {
                this.indexPi = res.data.indexPi;
                this.filePi = this.fileList[res.data.indexPi];
                this.musicPiPlaying = res.data.musicPiPlaying; 
                console.log("playPrePi works");
                })
                .catch(error => {
                console.log("handle error =>", error);
                })
              },
            playNextPi(event){
                axios.post('/playNextPi').then(res => {
                this.indexPi = res.data.indexPi;
                this.filePi = this.fileList[res.data.indexPi];
                dir_filePi = this.dir+this.fileList[this.indexPi];
                this.musicPiPlaying = res.data.musicPiPlaying; 
                console.log("playNextPi works");
                })
                .catch(error => {
                console.log("handle error =>", error);
                })
              },
            playRadioPi(event){
                radioNo=event.target.value;
                if(this.radioPiPlayingNo == radioNo){
                   this.radioPiPlayingNo = 0 ;
                }else{this.radioPiPlayingNo =radioNo;} 
                console.log("Before radioPalyingPiNo:"+ this.radioPiPlayingNo);
                axios.post('/playRadioPi',{"radioNo":this.radioPiPlayingNo}).then(res => {
                this.radioPiPlayingNo = res.data.radioPiPlayingNo;

                if(this.radioPiPlayingNo==0){
                  element = document.getElementById("sel10Pi");
                  element.value = 0
                  element = document.getElementById("sel20Pi");
                  element.value = 0
                  element = document.getElementById("sel30Pi");
                  element.value = 0
                }
                else if(this.radioPiPlayingNo>0 && this.radioPiPlayingNo <11){
                  element = document.getElementById("sel20Pi");
                  element.value = 0
                  element = document.getElementById("sel30Pi");
                  element.value = 0
                  element = document.getElementById("sel10Pi");
                  element.value = this.radioPiPlayingNo 
                }
                else if(  this.radioPiPlayingNo>11 &&this.radioPiPlayingNo<21){
                  element = document.getElementById("sel10Pi");
                  element.value = 0
                  element = document.getElementById("sel30Pi");
                  element.value = 0
                  element = document.getElementById("sel20Pi");
                  element.value = this.radioPiPlayingNo 
                }
                else{
                  element = document.getElementById("sel10");
                  element.value = 0
                  element = document.getElementById("sel20");
                  element.value = 0
                  element = document.getElementById("sel30");
                  element.value = this.radioPiPlayingNo 
                }

                console.log("After radioPiPlayingNo:"+ this.radioPiPlayingNo);
                console.log("playRadioPi works");
                })
                .catch(error => {
                console.log("handle error =>", error);
                })
              },
            volumeDownPi(event){
                axios.post('/volumeDownPi').then(res => {
                this.volumePi= res.data.volumePi;
                this.volumePiMute= res.data.volumePiMute;
                console.log("Volume: " + this.volumePi); 
                console.log("Mute: "+ this.volumePiMute); 
                console.log("VolumeDownPi works");
                })
                .catch(error => {
                console.log("handle error =>", error);
                })
              },
            volumeUpPi(event){
                axios.post('/volumeUpPi').then(res => {
                this.volumePi= res.data.volumePi;
                this.volumePiMute= res.data.volumePiMute;
                console.log("Volume: " + this.volumePi); 
                console.log("Mute: "+ this.volumePiMute); 
                console.log("VolumeUpPi works");
                })
                .catch(error => {
                console.log("handle error =>", error);
                })
              },
            volumeMutePi(event){
                axios.post('/volumeMutePi').then(res => {
                this.volumePi= res.data.volumePi;
                this.volumePiMute= res.data.volumePiMute;
                console.log("Volume: " + this.volumePi); 
                console.log("Mute: "+ this.volumePiMute); 
                console.log("VolumeMutePi works");
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
