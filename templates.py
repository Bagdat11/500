# templates.py

HTML_CONTROLLER = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Taldyk Summer - Бөлек Жіберу</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>
<body class="h-screen bg-slate-950 text-white flex flex-col justify-between p-6 text-center select-none overflow-hidden">
    <div>
        <span class="text-xs font-bold text-fuchsia-500 uppercase tracking-widest">Taldyk Summer • Crowd DJ</span>
        <h1 class="text-xl font-black mt-1 text-cyan-400">🔥 ИНТЕРАКТИВТІ БАСҚАРУ</h1>
        <p class="text-xs text-gray-400 mt-1">Әнді де, суретті де бір-біріне кедергісіз бөлек жібере беріңіз!</p>
    </div>

    <div class="space-y-4 my-auto">
        <div class="bg-slate-900/80 border border-slate-800 p-4 rounded-2xl space-y-2 shadow-xl">
            <h3 class="text-xs font-bold text-fuchsia-400 uppercase text-left">🎼 1. Ән таңдау:</h3>
            <div class="flex gap-2">
                <input type="text" id="songInput" placeholder="Шашлындос, Ворона, Истерика..." 
                       class="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:border-fuchsia-400">
                <button onclick="sendSong()" class="bg-fuchsia-600 hover:bg-fuchsia-700 text-black font-black px-4 rounded-xl text-xs uppercase tracking-wider">
                    ҚОСУ
                </button>
            </div>
        </div>

        <div class="bg-slate-900/80 border border-slate-800 p-4 rounded-2xl space-y-2 shadow-xl">
            <h3 class="text-xs font-bold text-cyan-400 uppercase text-left">📸 2. Залдан Селфи (Фото):</h3>
            <div class="flex flex-col gap-2">
                <input type="file" id="photoInput" accept="image/*"
                       class="w-full bg-slate-950 border border-slate-700 rounded-xl px-2 py-2 text-xs text-gray-400 focus:outline-none">
                <button onclick="sendPhoto()" class="w-full bg-cyan-500 hover:bg-cyan-600 text-black font-black py-2 rounded-xl text-xs uppercase tracking-wider">
                    📸 ЭКРАНҒА СУРЕТТІ ҰШЫРУ
                </button>
            </div>
        </div>
    </div>

    <div class="bg-black/30 p-2 rounded-xl border border-white/5">
        <div class="text-emerald-400 text-[10px] font-bold">ЖҮЙЕ ДАЙЫН СЕРВЕР ТІРІ 🌐</div>
    </div>

    <script>
        // Тек ән жіберу функциясы
        async function sendSong() {
            const songInput = document.getElementById('songInput');
            if(!songInput.value.trim()) return alert("Ән атын жазыңыз!");

            try {
                const formData = new FormData();
                formData.append('title', songInput.value.trim());

                const response = await fetch('/vote', { method: 'POST', body: formData });
                const result = await response.json();
                if(result.status === "success") {
                    alert(`"${songInput.value}" кезекке резервке қосылды! 🎵`);
                    songInput.value = '';
                }
            } catch (error) { alert("Сервер жауап бермеді."); }
        }

        // Тек сурет жіберу функциясы
        async function sendPhoto() {
            const photoInput = document.getElementById('photoInput');
            if(!photoInput.files[0]) return alert("Алдымен сурет таңдаңыз немесе селфи түсіріңіз!");

            try {
                const formData = new FormData();
                formData.append('title', ''); // Әнді бос жібереміз
                formData.append('photo', photoInput.files[0]);

                const response = await fetch('/vote', { method: 'POST', body: formData });
                const result = await response.json();
                if(result.status === "success") {
                    alert("Фото экрандағы слайдерге сәтті ұшырылды! 📸✨");
                    photoInput.value = '';
                }
            } catch (error) { alert("Сервер жауап бермеді."); }
        }
    </script>
</body>
</html>
"""

HTML_DASHBOARD = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Taldyk Summer Screen Hub</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght=700;900&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Orbitron', sans-serif; background: radial-gradient(circle, #020617 0%, #000000 100%); }
    </style>
</head>
<body class="h-screen flex flex-col justify-between p-6 text-white overflow-hidden">

    <header class="w-full flex justify-between items-center border-b border-slate-800 pb-4">
        <div>
            <span class="text-xs font-bold text-cyan-400 tracking-widest uppercase">Smart Playlist Manager v12</span>
            <h1 class="text-2xl font-black tracking-wider text-white">TALDYK SUMMER <span class="text-fuchsia-500">LIVE SCREEN</span></h1>
        </div>
        <div class="bg-slate-900 border border-cyan-500/30 px-4 py-2 rounded-xl text-center">
            <span class="text-[10px] text-gray-400 block uppercase">ҚАЗІР ОЙНАП ТҰРҒАН РЕМИКС:</span>
            <span id="currentPlaying" class="text-sm font-black text-green-400">ӘН КҮТУДЕ... 🎵</span>
        </div>
    </header>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 my-auto items-center">
        <div class="bg-slate-900/60 border border-slate-800 p-6 rounded-3xl space-y-4">
            <h2 class="text-sm font-black text-fuchsia-400 tracking-wider uppercase border-b border-slate-800 pb-2">📋 АЛДАҒЫ РЕЗЕРВ КЕЗЕГІ:</h2>
            <div id="queueVisualList" class="space-y-2 text-xs h-40 overflow-y-auto">
                <p class="text-gray-500 text-center py-4">Резерв бос. Сөз жазыңыз... 🎼</p>
            </div>
        </div>

        <div class="flex flex-col items-center justify-center relative h-64">
            <div id="ticker" class="absolute top-0 w-full text-center text-xs font-bold text-yellow-300 tracking-wide" style="cursor: pointer;" onclick="forceInitAudio()">
                🚨 ДЫБЫСТЫ ҚОСУ ҮШІН ОСЫ ЖЕРДІ 1 РЕТ БАСЫҢЫЗ!
            </div>

            <audio id="localAudioPlayer" crossorigin="anonymous"></audio>

            <div id="djBall" class="w-32 h-32 rounded-full bg-slate-900 border-4 border-slate-700 flex flex-col items-center justify-center transition-all duration-75 text-center p-2 mt-4">
                <span id="ballStatus" class="text-[10px] font-black text-gray-500 uppercase">КҮТУДЕ</span>
                <span id="bpmText" class="text-[9px] text-cyan-400 font-mono mt-1"></span>
            </div>

            <button onclick="skipTrack()" class="mt-4 bg-gradient-to-r from-red-500 to-fuchsia-600 hover:from-red-600 hover:to-fuchsia-700 text-white font-black px-6 py-2 rounded-xl text-xs tracking-widest shadow-lg border border-white/10 transition-transform active:scale-95">
                ⏭️ КЕЛЕСІ ӘН (SKIP)
            </button>
        </div>

        <div class="bg-slate-900/60 border border-slate-800 p-4 rounded-3xl space-y-4 flex flex-col items-center justify-center h-64 relative">
            <h2 class="text-xs font-black text-cyan-400 tracking-wider uppercase border-b border-slate-800 pb-1 w-full text-left absolute top-4 left-4">📸 ЗАЛДАН ТІКЕЛЕЙ ФОТО:</h2>
            <div id="photoSliderContainer" class="w-full h-44 mt-6 rounded-2xl overflow-hidden border-2 border-fuchsia-500/30 flex items-center justify-center bg-black/50">
                <p id="noPhotoText" class="text-[10px] text-gray-500 text-center p-2">Фото жіберілгенде осы жерде тірілей ауысып тұрады ✨</p>
                <img id="liveImageDisplay" class="w-full h-full object-cover hidden transition-opacity duration-500" style="opacity: 1;">
            </div>
        </div>
    </div>

    <footer class="w-full border-t border-slate-800 pt-4 flex justify-between items-center bg-slate-950 p-4 rounded-2xl">
        <div class="text-[10px] text-gray-400">TALDYK SUMMER PHOTO & QUEUE SYSTEM v12</div>
        <div class="bg-white p-2 rounded-2xl flex items-center gap-4 text-black shadow-lg">
            <div id="qrcode" class="p-1 bg-white rounded-lg"></div>
            <div class="text-left pr-4">
                <h4 class="text-xs font-black uppercase tracking-wide text-slate-950">БАСҚАРУ МЕН СЕЛФИ</h4>
                <p class="text-[9px] text-gray-600 mt-0.5 leading-tight">Сканерле де, әнді немесе фотоны бөлек жібер!</p>
            </div>
        </div>
    </footer>

    <script>
        const phoneUrl = window.location.origin + '/phone';
        new QRCode(document.getElementById("qrcode"), { text: phoneUrl, width: 85, height: 85 });

        const djBall = document.getElementById('djBall');
        const ticker = document.getElementById('ticker');
        const currentPlaying = document.getElementById('currentPlaying');
        const queueVisualList = document.getElementById('queueVisualList');
        const ballStatus = document.getElementById('ballStatus');
        const bpmText = document.getElementById('bpmText');
        const audioPlayer = document.getElementById('localAudioPlayer');
        const totalVotesCount = document.getElementById('totalVotesCount');
        const liveImageDisplay = document.getElementById('liveImageDisplay');
        const noPhotoText = document.getElementById('noPhotoText');

        let beatInterval = null;
        let audioPermissionGranted = false;
        let isPlaying = false;
        let serverQueueList = [];
        let globalPhotos = [];
        let currentPhotoIndex = 0;

        function forceInitAudio() {
            audioPermissionGranted = true;
            ticker.innerText = "🎵 ДЫБЫСТЫҚ ЖҮЙЕ БЕЛСЕНДІ!";
            ticker.style.color = "#10b981";
        }

        async function fetchVotes() {
            try {
                const response = await fetch('/get_votes');
                const data = await response.json();

                serverQueueList = data.queue;
                globalPhotos = data.photos;

                updateQueueUI(data.queue);
                updatePhotoSlider(); 

                if (!isPlaying && data.queue.length > 0) {
                    startNextFromQueue();
                }
            } catch (e) {
                console.log("Дерек алу қатесі");
            }
        }
        setInterval(fetchVotes, 1000);

        function updatePhotoSlider() {
            if (globalPhotos.length === 0) {
                noPhotoText.classList.remove('hidden');
                liveImageDisplay.classList.add('hidden');
                return;
            }
            noPhotoText.classList.add('hidden');
            liveImageDisplay.classList.remove('hidden');
        }

        setInterval(() => {
            if (globalPhotos.length > 0) {
                currentPhotoIndex = (currentPhotoIndex + 1) % globalPhotos.length;
                liveImageDisplay.style.opacity = 0;
                setTimeout(() => {
                    liveImageDisplay.src = globalPhotos[currentPhotoIndex];
                    liveImageDisplay.style.opacity = 1;
                }, 200);
            }
        }, 3000);

        async function startNextFromQueue() {
            if (isPlaying) return;
            isPlaying = true; 

            try {
                const response = await fetch('/pop_queue');
                const result = await response.json();

                if (result.status === "popped") {
                    playLocalTrack(result.song);
                } else {
                    isPlaying = false;
                }
            } catch(err) {
                isPlaying = false;
            }
        }

        function skipTrack() {
            audioPlayer.onended = null; 
            audioPlayer.pause();
            audioPlayer.src = "";
            if (beatInterval) clearInterval(beatInterval);

            isPlaying = false; 

            if (serverQueueList.length > 0) {
                startNextFromQueue();
            } else {
                ballStatus.innerText = "КҮТУДЕ";
                bpmText.innerText = "";
                djBall.style.backgroundColor = '#0f172a';
                djBall.style.boxShadow = 'none';
                currentPlaying.innerText = "РЕЗЕРВ БОС. ӘН КҮТУДЕ... 🎵";
            }
        }

        function playLocalTrack(songKey) {
            let fileTarget = encodeURIComponent("Шашлындос (Хлеб)"); 
            let displayName = "Хлеб - Шашлындос (Remix)";

            if (songKey === "истерика") { fileTarget = encodeURIComponent("Истерика (Джиос)"); displayName = "Джиос - Истерика"; }
            else if (songKey === "девочка") { fileTarget = encodeURIComponent("Девочка (Remix)"); displayName = "Ханза - Девочка (Remix)"; }
            else if (songKey === "ворона") { fileTarget = encodeURIComponent("Ворона (Кэнни)"); displayName = "Кэнни - Ворона"; }
            else if (songKey === "глаза") { fileTarget = encodeURIComponent("Твои глаза (Лейтинк)"); displayName = "Лейтинк - Твои глаза"; }
            else if (songKey === "ню") { fileTarget = encodeURIComponent("Не получается (НЮ)"); displayName = "НЮ - Не получается"; }
            else if (songKey === "пломбир") { fileTarget = encodeURIComponent("Пломбир (RASA)"); displayName = "RASA - Пломбир"; }
            else if (songKey === "любовь") { fileTarget = encodeURIComponent("Все слова о любви"); displayName = "Никита & Мария - Все слова о любви"; }

            currentPlaying.innerText = displayName.toUpperCase();
            ballStatus.innerText = "LIVE PLAYING";
            bpmText.innerText = "🥁 ФОТО СЛАЙДЕР";
            djBall.style.backgroundColor = '#06b6d4';
            djBall.style.boxShadow = '0 0 50px #00f0ff';

            audioPlayer.src = window.location.origin + "/static/" + fileTarget + ".mp3";
            audioPlayer.load();

            let playPromise = audioPlayer.play();
            if (playPromise !== undefined) {
                playPromise.then(_ => {
                    console.log("Ойнап жатыр");
                }).catch(error => {
                    isPlaying = false;
                    skipTrack(); 
                });
            }

            if (beatInterval) clearInterval(beatInterval);
            beatInterval = setInterval(() => {
                djBall.style.transform = 'scale(1.2)';
                setTimeout(() => djBall.style.transform = 'scale(1)', 80);
            }, 450);

            audioPlayer.onended = function() {
                clearInterval(beatInterval);
                isPlaying = false;
                if (serverQueueList.length > 0) {
                    startNextFromQueue();
                } else {
                    ballStatus.innerText = "АЯҚТАЛДЫ";
                    bpmText.innerText = "";
                    djBall.style.backgroundColor = '#0f172a';
                    djBall.style.boxShadow = 'none';
                    currentPlaying.innerText = "ӘН КҮТУДЕ... 🎵";
                }
            };
        }

        function updateQueueUI(queue) {
            if (queue.length === 0) {
                queueVisualList.innerHTML = `<p class="text-gray-500 text-center py-4">Резерв бос. Сөз жазыңыз... 🎼</p>`;
                return;
            }
            queueVisualList.innerHTML = "";
            queue.forEach((song, index) => {
                queueVisualList.innerHTML += `
                    <div class="flex justify-between items-center bg-slate-950 p-2.5 rounded-xl border border-slate-800">
                        <span class="font-bold text-white text-[11px]">${index + 1}. 🎵 ${song.toUpperCase()}</span>
                        <span class="text-[9px] text-fuchsia-400 uppercase tracking-wider font-mono">Резервте</span>
                    </div>`;
            });
        }
    </script>
</body>
</html>
"""