const { createApp} = Vue;
const vm = createApp({
  delimiters:['%{', '}%'],
  data(){
               return {
               elementAudioPc: null,
               elementAudioPcBar: null,
               element10Pi : null,
               element20Pi : null,
               element30Pi : null,
               element10Pc : null,
               element20Pc : null,
               element30Pc : null,
               musicPcPlaying : false,
               musicPiPlaying : false,
               musicPcPlayMode : 0,
               musicPiPlayMode : 0,
               playRatePc : 1 ,
               playRatePi : 1 ,
               fileList : [],
               dir :"./static/assets/",
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
               downStatus : false,
               sleepTimePc: 5,
               sleepTimePcShow: "No ",
               sleepTimerPc: null,
               sleepTimePi: 5,
               sleepTimePiShow: "No ",
               sleepTimerPi: null,
               cronTimeHour: 6,
               cronTimeMin :0,
               cronStatus: false,
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
           
            contuineplaying(){
              var self = this;
              this.elementAudioPc.addEventListener("ended",function() {
              if(self.musicPcPlaying == true){
                 console.log("Continue Playing");
                 self.playNextPc();
                }
              });
             },
            setSleepTimePc(){
              a=[10,20,30,1000];
              clearTimeout(this.sleepTimer);
              this.sleepTimePc = this.sleepTimePc + 1
              if(this.sleepTimePc> 3 ){ this.sleepTimePc = 0};
              switch (this.sleepTimePc) {
                      case 0 : { this.sleepTimePcShow = "10 min";  break;}
                      case 1 : { this.sleepTimePcShow = "20 min";  break;}
                      case 2 : { this.sleepTimePcShow = "30 min";  break;}
                      case 3 : { this.sleepTimePcShow = "No";  break;}
                     }
              ts=a[this.sleepTimePc]*1000*60;
              console.log(ts);
              this.sleepTimerPc=setTimeout(this.stopPlayingPc,ts)
             },
             stopPlayingPc(){
              this.elementAudioPc.pause();
              this.musicPcPlaying = false;
              this.elementRadioPc.pause();
              this.radioPcPlayingNo = 0;
             },
             playSelectedPc(){
                num=this.num4dPc.join("");
                console.log("current keyno is: "+num);
                this.indexPc= num % this.indexMax;
                this.filePc=this.fileList[this.indexPc];
                console.log(this.dir+this.fileList[this.indexPc]);
                dirfilePc=this.dir+this.fileList[this.indexPc];
                this.elementAudioPc.pause();
                this.elementAudioPc.setAttribute('src',dirfilePc);
                this.elementAudioPc.load();
                this.elementAudioPc.play();
                this.musicPcPlaying = true;
                this.num4dPc[0]=0;
                this.num4dPc[1]=0;
                this.num4dPc[2]=0;
                this.num4dPc[3]=0;
                this.keytimerPcRunning = false;
             },
            playIndexPc(event){
                this.indexPc = event.target.selectedIndex - 1;
                this.filePc=this.fileList[this.indexPc];
                dirfilePc=this.dir+this.fileList[this.indexPc];
                this.elementAudioPc.pause();
                this.elementAudioPc.setAttribute('src',dirfilePc);
                this.elementAudioPc.load();
                this.elementAudioPc.play();
                this.musicPcPlaying = true;
             },
             setPlayModePc(){
                this.musicPcPlayMode = this.musicPcPlayMode +1
                this.musicPcPlayMode = this.musicPcPlayMode % 2;
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
            playPausePc(){
                dirfilePc=this.dir+this.fileList[this.indexPc];
                console.log(dirfilePc); 
                this.elementAudioPc.setAttribute('src',dirfilePc);
                if(this.musicPcPlaying == false){
                //this.elementAudioPc.currentTime=this.elementAudioPcBar.value;
                this.elementAudioPc.play();
                this.musicPcPlaying = true;
                console.log("playPausePc to Play"); 
                console.log(this.musicPcPlaying);
                }
                else{
                //this.elementAudioPcBar.value=this.elementAudioPc.currentTime;
                this.elementAudioPc.pause();
                this.musicPcPlaying = false;
                console.log("playPausePc to Pause"); 
                }
           	  },
            playPrePc(){
                if(this.musicPcPlayMode==1){
                rn = this.getRandom(this.indexMax-1, 0);
                this.indexPc = rn
                  }
                else{
                this.indexPc = this.indexPc - 1;
                  }
                if(this.indexPc < 0){
                  this.indexPc = this.indexMax - 1;
                  }
                this.filePc=this.fileList[this.indexPc];
                dirfilePc=this.dir+this.fileList[this.indexPc];
                this.elementAudioPc.setAttribute('src',dirfilePc);
                this.elementAudioPc.load();
                this.elementAudioPc.play();
                this.musicPcPlaying = true; 
                console.log(this.indexPc);
                console.log(this.filePc);
                console.log("playPrePc works");
              },
            playNextPc(){
                if(this.musicPcPlayMode==1){
                rn = this.getRandom(this.indexMax-1, 0);
                this.indexPc = rn
                  }
                else{
                this.indexPc = this.indexPc + 1;
                  }
                if(this.indexPc >= this.indexMax){
                  this.indexPc = 0;
                  }
                this.filePc=this.fileList[this.indexPc];
                dirfilePc=this.dir+this.fileList[this.indexPc];
                console.log(dirfilePc);
                this.elementAudioPc.pause();
                this.elementAudioPc.setAttribute('src',dirfilePc);
                this.elementAudioPc.load();
                this.elementAudioPc.play();
                this.musicPcPlaying = true;
                console.log(this.indexPc);
                console.log(this.filePc);
                console.log("playNextPc works");
              },
             setPlayRatePc(){
                this.playRatePc = this.playRatePc +0.5;
                if (this.playRatePc > 2.5){
                    this.playRatePc = 0.5;
                }
                this.elementAudioPc.playbackRate = this.playRatePc;
              },
            volumeDownPc(){
                this.volumePc = this.volumePc - 0.2;
                if(this.volumePc < 0 ){this.volumePc =0;}
                this.elementAudioPc.volume= this.volumePc;
                this.elementRadioPc.volume= this.volumePc;
                console.log("volumeDownPc works");
              },
            volumeUpPc(){
                this.volumePc = this.volumePc + 0.2;
                if(this.volumePc > 1){this.volumePc =1;}
                this.elementAudioPc.volume = this.volumePc; 
                this.elementRadioPc.volume = this.volumePc; 
                console.log("volumeUpPc works");
              },
            volumeMutePc(){
                if(this.volumePc != 0 ){this.volumePc =0;}
                this.elementAudioPc.volume = 0; 
                this.elementRadioPc.volume = 0; 
                console.log("volumeMutePc works");
              },
            playRadioPc(event){
                this.radioPcPlayingNo = event.target.value;
                console.log("this.radioPcPlayingNo:"+this.radioPcPlayingNo);
                if(this.radioPcPlayingNo==0){
                  this.element10Pc.value = "0";
                  this.element20Pc.value = "0";
                  this.element30Pc.value = "0";
                }
                else if(this.radioPcPlayingNo>0 && this.radioPcPlayingNo<11){
                  this.element10Pc.value = this.radioPcPlayingNo;
                  this.element20Pc.value = "0";
                  this.element30Pc.value = "0";
                }
                else if(this.radioPcPlayingNo>10 && this.radioPcPlayingNo<21){
                  this.element10Pc.value = "0";
                  this.element20Pc.value = this.radioPcPlayingNo;
                  this.element30Pc.value = "0";
                }
                else{
                  this.element10Pc.value = "0";
                  this.element20Pc.value = "0";
                  this.element30Pc.value = this.radioPcPlayingNo;
                }
                let url = "";
                if(this.radioPcPlayingNo == 0){
                this.elementRadioPc.pause();
                      }
                else{
                switch (this.radioPcPlayingNo) {
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
                this.elementRadioPc.pause();
                this.elementRadioPc.setAttribute('src',url);
                this.elementRadioPc.load();
                this.elementRadioPc.play();
                console.log("radioPcPlayingNo: "+this.radioPcPlayingNo);
                }
              },

            playSelectedPi(){
                num=this.num4dPi.join("");
                axios.post('/playSelectedPi',{"num":num}).then(res => {
                this.musicPiPlaying = res.data.musicPiPlaying;
                this.indexPi = res.data.indexPi;
                this.filePi=this.fileList[this.indexPi];
                console.log(this.filePi)
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
             setPlayRatePi(){
                axios.post('/setPlayRatePi').then(res => {
                this.playRatePi = res.data.playRatePi;
                })
                .catch(error => {
                console.log("handle error =>", error);
                })
             },
             setPlayModePi(mode){
                this.musicPiPlayMode = this.musicPiPlayMode + 1;
                this.musicPiPlayMode = this.musicPiPlayMode % 2;
                mode = this.musicPiPlayMode
                axios.post('/setPlayModePi',{"mode":mode}).then(res => {
                this.musicPiPlayMode = res.data.musicPiPlayMode;
                })
                .catch(error => {
                console.log("handle error =>", error);
                })
             },
            setSleepTimePi(){
              axios.post('/setSleepTimePi').then(res => {
                this.sleepTimePi = res.data.sleepTimePi; 
                this.musicPiPlaying = res.data.musicPiPlaying; 
                this.radioPiPlayingNo = res.data.radioPiPlayingNo; 
              switch (this.sleepTimePi) {
                case 0 : { this.sleepTimePiShow = "10 min";  break;}
                case 1 : { this.sleepTimePiShow = "20 min";  break;}
                case 2 : { this.sleepTimePiShow = "30 min";  break;}
                case 3 : { this.sleepTimePiShow = "No ";  break;}
                     }
                console.log("works setSleepTimePi");
                })
             },
             playPausePi(){
                axios.post('/playPausePi').then(res => {
                this.musicPiPlaying = res.data.musicPiPlaying; 
                this.indexPi = res.data.indexPi;
                console.log(this.filePi)
                this.filePi = this.fileList[res.data.indexPi];
                console.log("works playPausePi");
                })
                .catch(error => {
                console.log("handle error =>", error);
                })
           	  },
             playPrePi(){
                axios.post('/playPrePi').then(res => {
                this.indexPi = res.data.indexPi;
                this.filePi = this.fileList[res.data.indexPi];
                console.log(this.filePi)
                this.musicPiPlaying = res.data.musicPiPlaying; 
                console.log("playPrePi works");
                })
                .catch(error => {
                console.log("handle error =>", error);
                })
              },
            playNextPi(){
                axios.post('/playNextPi').then(res => {
                this.indexPi = res.data.indexPi;
                this.filePi = this.fileList[res.data.indexPi];
                console.log(this.filePi)
                dir_filePi = this.dir+this.fileList[this.indexPi];
                this.musicPiPlaying = res.data.musicPiPlaying; 
                console.log("playNextPi works");
                })
                .catch(error => {
                console.log("handle error =>", error);
                })
              },
            playIndexPi(event){
                var indexPi = event.target.selectedIndex - 1;
                axios.post('/playIndexPi',{"indexPi":indexPi}).then(res => {
                this.indexPi = res.data.indexPi;
                this.filePi = this.fileList[res.data.indexPi];
                console.log(this.filePi)
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
                axios.post('/playRadioPi',{"radioNo":this.radioPiPlayingNo}).then(res => {
                this.radioPiPlayingNo = res.data.radioPiPlayingNo;
                if(this.radioPiPlayingNo==0){
                  this.element10Pi.value = "0";
                  this.element20Pi.value = "0";
                  this.element30Pi.value = "0";
                }
                else if(this.radioPiPlayingNo>0 && this.radioPiPlayingNo <11){
                  this.element10Pi.value = this.radioPiPlayingNo; 
                  this.element20Pi.value = "0";
                  this.element30Pi.value = "0";
                }
                else if(this.radioPiPlayingNo>10 && this.radioPiPlayingNo<21){
                  this.element10Pi.value = "0";
                  this.element20Pi.value = this.radioPiPlayingNo; 
                  this.element30Pi.value = "0";
                }
                else{
                  this.element10Pi.value = "0";
                  this.element20Pi.value = "0";
                  this.element30Pi.value = this.radioPiPlayingNo; 
                }
                console.log("After radioPiPlayingNo:"+ this.radioPiPlayingNo);
                console.log("playRadioPi works");
                })
                .catch(error => {
                console.log("handle error =>", error);
                })
              },
            volumeDownPi(){
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
            volumeUpPi(){
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
            volumeMutePi(){
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
              },
            refreshList(){
                this.indexMax = this.fileList.length;
                rn = this.getRandom(this.indexMax-1, 0);
                this.indexPc=rn;
                this.filePc=this.fileList[rn];
                this.filePi=this.fileList[this.indexPi];
              },
            getFileList(style){
                document.getElementById("my-audio").pause();
                this.musicPcPlaying = false;
                this.musicPiPlaying = false;
                axios.post('/getFileList',{"style":style}).then(res => {
                this.fileList = res.data.fileList;
                this.indexPi = res.data.indexPi;
                this.refreshList();
                console.log(this.fileList);
                console.log("FileList Refresh");
                })
                .catch(error => {
                console.log("handle error =>", error);
                })
              },
            downPodcastFile(){
                axios.post('/downPodcastFile2').then(res => {
                this.downStatus = res.data.downStatus;
                var msg = res.data.msg;
                console.log("downStatus:" + this.downStatus);
                console.log(msg);
                })
                .catch(error => {
                console.log("handle error =>", error);
                })
              },
            setCronHour(){
              },
            setCronMin(){
              },
            setCron(){
              var Hour =document.getElementById("cronHour").value;
              var Min =document.getElementById("cronMin").value;
              var cronStatus= true;
              axios.post('/setCron',{"Hour":Hour,"Min":Min}).then(res => {
                this.cronTimeHour = res.data.cronTimeHour;
                this.cronTimeMin = res.data.cronTimeMin;
                this.cronStatus = res.data.cronStatus;
                console.log("set Time Hour as:"+ this.cronTimeHour); 
                console.log("set Time Min as:"+ this.cronTimeMin); 
                console.log("cron Status :"+ this.cronStatus); 
                })
                .catch(error => {
                console.log("handle error =>", error);
                })
              },
              //--------------------------------------------------------------------------------------------------
            mDur(){
                console.log("mDur")
                this.elementAudioPcBar.max= this.elementAudioPc.duration
                let totalDuration= this.calculateTotalValue(this.elementAudioPc.duration)
                console.log(totalDuration)
                a=document.getElementById("endText");
                a.textContent=totalDuration;

               },
            mUpdate(){
                console.log("mUpdate")
                this.elementAudioPcBar.value=this.elementAudioPc.currentTime
                let currentTime = this.calculateCurrentValue(this.elementAudioPc.currentTime);
                console.log(currentTime)
                b=document.getElementById("startText");
                if(this.musicPcPlaying== true){
                b.textContent=currentTime;
                }
               },
            mSet(){
                console.log("mSet")
                this.elementAudioPc.currentTime=this.elementAudioPcBar.value
               },
            mPlay(){
                console.log("mPlay")
                //this.elementAudioPc.currentTime=this.elementAudioPcBar.value
               },
            mPause(){
                console.log("mPause")
                //thes.elementAudioPc.currentTime=this.elementAudioPcBar.value
                //let currentTime = this.calculateCurrentValue(this.elementAudioPc.currentTime);
                //b=document.getElementById("startText");
                //b.textContent=currentTime;
               },
              //--------------------------------------------------------------------------------------------------
            calculateTotalValue(length) {
                let minutes = Math.floor(length / 60),
                seconds_int = length - minutes * 60,
                seconds_str = seconds_int.toString(),
                seconds = seconds_str.substr(0, 2),
                time = minutes + ':' + seconds
                return time;
                },
            calculateCurrentValue(currentTime) {
                let current_hour = parseInt(currentTime / 3600) % 24,
                current_minute = parseInt(currentTime / 60) % 60,
                current_seconds_long = currentTime % 60,
                current_seconds = current_seconds_long.toFixed(),
                current_time = (current_minute < 10 ? "0" + current_minute : current_minute) + ":" + (current_seconds < 10 ? "0" + current_seconds : current_seconds);
                return current_time;
                },
              //--------------------------------------------------------------------------------------------------
            loading(){
              axios.post('/').then(res => {
              this.indexPi=res.data.indexPi;
              this.musicPiPlaying=res.data.musicPiPlaying;
              this.playRatePi=res.data.playRatePi;
              this.musicPiPlayMode=res.data.musicPiPlayMode;
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
              console.log("musicPiPlaying: "+this.musicPiPlaying);
              console.log("musicPiPlayMode: "+this.musicPiPlayMode);
              console.log("radioPiPlayingNo: "+this.radioPiPlayingNo);
              console.log("volumePi: "+this.volumePi);
              console.log("volumePiMute: "+this.volumePiMute);
              
              this.elementAudioPc = document.getElementById("my-audio");
              this.elementAudioPcBar = document.getElementById("my-audio-bar");
              this.elementAudioPc.volume = this.volumePc; 

              this.elementRadioPc = document.getElementById("my-radio");
              this.elementRadioPc.volume = this.volumePc;
              
              this.contuineplaying();
              this.element10Pi = document.getElementById("sel10Pi");
              this.element20Pi = document.getElementById("sel20Pi");
              this.element30Pi = document.getElementById("sel30Pi");
              this.element10Pc = document.getElementById("sel10Pc");
              this.element20Pc = document.getElementById("sel20Pc");
              this.element30Pc = document.getElementById("sel30Pc");

              if(this.radioPiPlayingNo==0){
                this.element10Pi.value = "0"
                this.element20Pi.value = "0"
                this.element30Pi.value = "0"
              }
              else if(this.radioPiPlayingNo>0 && this.radioPiPlayingNo <11){
                this.element10Pi.value = this.radioPiPlayingNo
                this.element20Pi.value = "0"
                this.element30Pi.value = "0"
              }
              else if(  this.radioPiPlayingNo>11 && this.radioPiPlayingNo<21){
                this.element10Pi.value = "0"
                this.element20Pi.value = this.radioPiPlayingNo
                this.element30Pi.value = "0"
              }
              else{
                this.element10Pi.value = "0"
                this.element20Pi.value = "0"
                this.element30Pi.value = this.radioPiPlayingNo
              }
            });
            }
          },
  created:function(){
               this.loading();
          }
       })
  vm.mount('#app');
//   my-Audio.addEventListener("ended", playnext);
