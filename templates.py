# templates.py

HTML_CONTROLLER = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Taldyk Summer - Резервке Қосу</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>
<body class="h-screen bg-slate-950 text-white flex flex-col justify-between p-6 text-center select-none overflow-hidden">
    <div>
        <span class="text-xs font-bold text-fuchsia-500 uppercase tracking-widest">Taldyk Summer • Crowd DJ</span>
        <h1 class="text-xl font-black mt-1 text-cyan-400">🔥 РЕЗЕРВКЕ ӘН ҚОСУ</h1>
        <p class="text-xs text-gray-400 mt-2">Папкадағы хиттер: Ворона, Шашлындос, Девочка, Истерика, Не получается, Пломбир, Твои глаза.</p>
    </div>

    <div class="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4 my-auto shadow-xl">
        <h3 class="text-xs font-bold text-fuchsia-400 uppercase text-left">🎼 Ән немесе Автор аты:</h3>
        <form onsubmit="sendVote(event)" class="flex flex-col gap-3">
            <input type="text" id="songInput" placeholder="Мысалы: Шашлындос, Пломбир, Ворона" required
                   class="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-cyan-400">
            <button type="submit" class="w-full bg-gradient-to-r from-fuchsia-500 to-cyan-500 text-black font-black py-3 rounded-xl text-sm">
                🎵 КЕЗЕККЕ (РЕЗЕРВКЕ) ҚОСУ
            </button>
        </form>
    </div>

    <div class="bg-black/30 p-2 rounded-xl border border-white/5">
        <div class="text-emerald-400 text-[10px] font-bold">БАЙЛАНЫС: СЕРВЕРГЕ ҚОСЫЛЫП ТҰР 🌐</div>
    </div>

    <script>
        async function sendVote(event) {
            event.preventDefault();
            const input = document.getElementById('songInput');
            const songName = input.value.trim();

            try {
                const formData = new FormData();
                formData.append('title', songName);

                const response = await fetch('/vote', { method: 'POST', body: formData });
                const result = await response.json();
                if(result.status === "success") {
                    alert(`"${songName}" ремиксі кезекке резервке қосылды! 🚀`);
                    input.value = '';
                }
            } catch (error) {
                alert("Қате! Сервер жауап бермеді.");
            }
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
            <span class="text-xs font-bold text-cyan-400 tracking-widest uppercase">Smart Playlist Manager v9</span>
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
            <div id="ticker" class="absolute top-0 w-full text-center text-xs font-bold text-yellow-300 tracking-wide animate-pulse" style="cursor: pointer;" onclick="forceInitAudio()">
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

        <div class="bg-slate-900/60 border border-slate-800 p-6 rounded-3xl space-y-4">
            <h2 class="text-sm font-black text-cyan-400 tracking-wider uppercase border-b border-slate-800 pb-2">👑 ЗАЛДЫҢ АКТИВТІЛІГІ:</h2>
            <div id="activityLog" class="space-y-3 text-xs text-gray-300">
                <div class="flex justify-between border-b border-slate-800/50 pb-1">
                    <span>Жалпы жіберілген дауыс:</span>
                    <span id="totalVotesCount" class="font-bold text-white">0</span>
                </div>
                <p class="text-[11px] text-gray-400 italic mt-2">• Телефоннан жазылған әндер бұзып кірмейді, резервке тұрады.</p>
                <p class="text-[11px] text-gray-400 italic">• Ноутбуктегі батырманы басып, кез келген уақытта әнді қолмен келесіге ауыстыра аласыз!</p>
            </div>
        </div>
    </div>

    <footer class="w-full border-t border-slate-800 pt-4 flex justify-between items-center bg-slate-950 p-4 rounded-2xl">
        <div class="text-[10px] text-gray-400">TALDYK SUMMER QUEUE SYSTEM v9</div>
        <div class="bg-white p-2 rounded-2xl flex items-center gap-4 text-black shadow-lg">
            <div id="qrcode" class="p-1 bg-white rounded-lg"></div>
            <div class="text-left pr-4">
                <h4 class="text-xs font-black uppercase tracking-wide text-slate-950">Өз әніңді жаз</h4>
                <p class="text-[9px] text-gray-600 mt-0.5 leading-tight">Камерамен сканерле де, резервке қос!</p>
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

        let beatInterval = null;
        let audioPermissionGranted = false;
        let isPlaying = false;
        let serverQueueList = [];

        function forceInitAudio() {
            audioPermissionGranted = true;
            ticker.innerText = "🎵 ДЫБЫСТЫҚ ЖҮЙЕ БЕЛСЕНДІ!";
            ticker.style.color = "#10b981";
        }

        // Серверден мәлімет алып тұру
        async function fetchVotes() {
            try {
                const response = await fetch('/get_votes');
                const data = await response.json();

                totalVotesCount.innerText = data.total_clicks;
                serverQueueList = data.queue;

                updateQueueUI(data.queue);

                // Егер қазір ештеңе ойнап тұрмаса және резервте ән болса — автоматты біріншісін қосамыз
                if (!isPlaying && data.queue.length > 0) {
                    startNextFromQueue();
                }
            } catch (e) {
                console.log("Дерек алу қатесі");
            }
        }
        setInterval(fetchVotes, 1000);

        // Кезектегі бірінші әнді алу және ойнату
        async function startNextFromQueue() {
            if (isPlaying) return;

            const response = await fetch('/pop_queue', { method: 'POST' });
            const result = await response.json();

            if (result.status === "popped") {
                playLocalTrack(result.song);
            }
        }

        // ⏭️ НОУТБУКТЕН ӘНДІ АУЫСТЫРУ БАТЫРМАСЫНЫҢ ФУНКЦИЯСЫ (SKIP)
        function skipTrack() {
            audioPlayer.pause();
            clearInterval(beatInterval);
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
            isPlaying = true;
            let fileTarget = encodeURIComponent("Шашлындос (Хлеб)"); 
            let displayName = "Хлеб - Шашлындос (Remix)";

            if (songKey === "истерика") { fileTarget = encodeURIComponent("Истерика (Джиос)"); displayName = "Джиос & Паша - Истерика (Remix)"; }
            else if (songKey === "девочка") { fileTarget = encodeURIComponent("Девочка (Remix)"); displayName = "Jah Khu & Ханза - Девочка (Remix)"; }
            else if (songKey === "ворона") { fileTarget = encodeURIComponent("Ворона (Кэнни)"); displayName = "Кэнни & МС Дым - Ворона (Remix)"; }
            else if (songKey === "глаза") { fileTarget = encodeURIComponent("Твои глаза (Лейти"); displayName = "Leytink & RSXD - Твои глаза (Remix)"; }
            else if (songKey === "любовь") { fileTarget = encodeURIComponent("Все слова о любви"); displayName = "Никита & Мария - Все слова о любви"; }
            else if (songKey === "ню") { fileTarget = encodeURIComponent("Не получается (Н"); displayName = "НЮ - Не получается (Remix)"; }
            else if (songKey === "пломбир") { fileTarget = encodeURIComponent("Пломбир (RASA)"); displayName = "RASA - Пломбир (Remix)"; }

            currentPlaying.innerText = displayName.toUpperCase();
            ballStatus.innerText = "LIVE PLAYING";
            bpmText.innerText = "🥁 КЕЗЕКПЕН ОЙНАУДА";
            djBall.style.backgroundColor = '#06b6d4';
            djBall.style.boxShadow = '0 0 50px #00f0ff';

            audioPlayer.src = window.location.origin + "/static/" + fileTarget + ".mp3";
            audioPlayer.load();

            if (audioPermissionGranted) {
                audioPlayer.play().catch(e => console.log("Дыбыс қатесі"));
            }

            if (beatInterval) clearInterval(beatInterval);
            beatInterval = setInterval(() => {
                djBall.style.transform = 'scale(1.2)';
                setTimeout(() => djBall.style.transform = 'scale(1)', 80);
            }, 450);

            // Ән толық өзі біткенде келесі әнге автоматты көшу логикасы
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

        // 📋 ЭКРАНДАҒЫ РЕЗЕРВ ТІЗІМІН СИНХРОНДЫ КӨРСЕТУ
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