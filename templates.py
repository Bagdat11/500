# templates.py

HTML_CONTROLLER = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Taldyk Summer - Әнді Іске Қосу</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>
<body class="h-screen bg-slate-950 text-white flex flex-col justify-between p-6 text-center select-none overflow-hidden">
    <div>
        <span class="text-xs font-bold text-fuchsia-500 uppercase tracking-widest">Taldyk Summer • Instant AI DJ</span>
        <h1 class="text-xl font-black mt-1 text-cyan-400">🔥 ӘНДІ БАСҚАРУ ЗОНАСЫ</h1>
        <p class="text-xs text-gray-400 mt-2">Папкадағы хиттер: Ворона, Шашлындос, Девочка, Истерика, Не получается, Пломбир, Твои глаза.</p>
    </div>

    <div class="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4 my-auto shadow-xl">
        <h3 class="text-xs font-bold text-fuchsia-400 uppercase text-left">🎼 Ән немесе Автор аты:</h3>
        <form onsubmit="sendVote(event)" class="flex flex-col gap-3">
            <input type="text" id="songInput" placeholder="Мысалы: Шашлындос, Пломбир, Ворона" required
                   class="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-cyan-400">
            <button type="submit" class="w-full bg-gradient-to-r from-fuchsia-500 to-cyan-500 text-black font-black py-3 rounded-xl text-sm">
                🚀 ӘНДІ БІРДЕН ОЙНАТУ (PLAY)
            </button>
        </form>
    </div>

    <div class="bg-black/30 p-2 rounded-xl border border-white/5">
        <div class="text-emerald-400 text-[10px] font-bold">БАЙЛАНЫС: 100% ҚАУІПСІЗ СЕРВЕР 🌐</div>
    </div>

    <script>
        async function sendVote(event) {
            event.preventDefault();
            const input = document.getElementById('songInput');
            const songName = input.value.trim();

            try {
                const formData = new FormData();
                formData.append('title', songName);

                const response = await fetch('/vote', {
                    method: 'POST',
                    body: formData
                });
                const result = await response.json();
                if(result.status === "success") {
                    alert(`"${songName}" ремиксі экранға жіберілді! 🚀`);
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
            <span class="text-xs font-bold text-cyan-400 tracking-widest uppercase">Instant Crowd DJ System v7</span>
            <h1 class="text-2xl font-black tracking-wider text-white">TALDYK SUMMER <span class="text-fuchsia-500">LIVE SCREEN</span></h1>
        </div>
        <div class="bg-slate-900 border border-cyan-500/30 px-4 py-2 rounded-xl text-center">
            <span class="text-[10px] text-gray-400 block uppercase">ҚАЗІР ОЙНАП ТҰРҒАН РЕМИКС:</span>
            <span id="currentPlaying" class="text-sm font-black text-green-400">ӘН КҮТУДЕ... 🎵</span>
        </div>
    </header>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 my-auto items-center">
        <div class="bg-slate-900/60 border border-slate-800 p-6 rounded-3xl space-y-4">
            <h2 class="text-sm font-black text-fuchsia-400 tracking-wider uppercase border-b border-slate-800 pb-2">📊 ЕҢ КӨП ЖАЗЫЛҒАН ӘНДЕР:</h2>
            <div id="ratingList" class="space-y-4">
                <p class="text-xs text-gray-500 text-center py-4">Соткадан ән жазыңыз... 🎼</p>
            </div>
        </div>

        <div class="flex flex-col items-center justify-center relative h-64" style="cursor: pointer;" onclick="forceInitAudio()">
            <div id="ticker" class="absolute top-0 w-full text-center text-xs font-bold text-yellow-300 tracking-wide animate-pulse">
                🚨 ДЫБЫСТЫ ҚОСУ ҮШІН ЭКРАНДЫ 1 РЕТ БАСЫҢЫЗ!
            </div>

            <audio id="localAudioPlayer" crossorigin="anonymous"></audio>

            <div id="djBall" class="w-36 h-36 rounded-full bg-slate-900 border-4 border-slate-700 flex flex-col items-center justify-center transition-all duration-75 text-center p-2">
                <span id="ballStatus" class="text-[10px] font-black text-gray-500 uppercase">КҮТУДЕ</span>
                <span id="bpmText" class="text-[9px] text-cyan-400 font-mono mt-1"></span>
            </div>
            <div id="timerText" class="text-xs text-fuchsia-400 mt-4 font-mono h-4 font-bold"></div>
        </div>

        <div class="bg-slate-900/60 border border-slate-800 p-6 rounded-3xl space-y-4">
            <h2 class="text-sm font-black text-cyan-400 tracking-wider uppercase border-b border-slate-800 pb-2">👑 ЗАЛДЫҢ АКТИВТІЛІГІ:</h2>
            <div id="activityLog" class="space-y-3 text-xs text-gray-300">
                <div class="flex justify-between border-b border-slate-800/50 pb-1">
                    <span>Жалпы жіберілген дауыс:</span>
                    <span id="totalVotesCount" class="font-bold text-white">0</span>
                </div>
                <div class="flex justify-between border-b border-slate-800/50 pb-1">
                    <span>Соңғы белсенділік:</span>
                    <span id="lastActiveSong" class="font-bold text-yellow-400">-</span>
                </div>
                <p class="text-[11px] text-gray-400 italic mt-2">• Жаңа ән жазылған сәтте ескі ән автоматты түрде тоқтап, жаңасы шорт үзіліссіз қосылады!</p>
            </div>
        </div>
    </div>

    <footer class="w-full border-t border-slate-800 pt-4 flex justify-between items-center bg-slate-950 p-4 rounded-2xl">
        <div class="text-[10px] text-gray-400">TALDYK SUMMER INSTANT INTERACTIVE REMIXER v7</div>
        <div class="bg-white p-2 rounded-2xl flex items-center gap-4 text-black shadow-lg">
            <div id="qrcode" class="p-1 bg-white rounded-lg"></div>
            <div class="text-left pr-4">
                <h4 class="text-xs font-black uppercase tracking-wide text-slate-950">Өз әніңді жаз</h4>
                <p class="text-[9px] text-gray-600 mt-0.5 leading-tight">Камерамен сканерле де, лезде ауыстыр!</p>
            </div>
        </div>
    </footer>

    <script>
        const phoneUrl = window.location.origin + '/phone';
        new QRCode(document.getElementById("qrcode"), { text: phoneUrl, width: 85, height: 85 });

        const djBall = document.getElementById('djBall');
        const ticker = document.getElementById('ticker');
        const currentPlaying = document.getElementById('currentPlaying');
        const ratingList = document.getElementById('ratingList');
        const timerText = document.getElementById('timerText');
        const ballStatus = document.getElementById('ballStatus');
        const bpmText = document.getElementById('bpmText');
        const audioPlayer = document.getElementById('localAudioPlayer');
        const totalVotesCount = document.getElementById('totalVotesCount');
        const lastActiveSong = document.getElementById('lastActiveSong');

        let beatInterval = null;
        let audioPermissionGranted = false;
        let currentPlayingKey = null;
        let localVoteTracker = {};

        function forceInitAudio() {
            audioPermissionGranted = true;
            ticker.innerText = "🎵 ДЫБЫСТЫҚ ЖҮЙЕ БЕЛСЕНДІ! Ән күтуде...";
            ticker.style.color = "#10b981";
        }

        // Серверден мәліметтерді тірілей алу
        async function fetchVotes() {
            try {
                const response = await fetch('/get_votes');
                const votes = await response.json();

                // Тексеру: Жалпы дауыс санын есептеу және соңғы жазылған әнді анықтау
                let total = 0;
                let activeSongName = "-";
                let maxVal = -1;

                Object.keys(votes).forEach(key => {
                    total += votes[key];
                    if (votes[key] > 0 && votes[key] >= maxVal) {
                        maxVal = votes[key];
                    }

                    // 🧠 ІРГЕЛІ ӨЗГЕРІС: Жаңа дауыс келгенін анықтау алгоритмі
                    if (!localVoteTracker[key]) localVoteTracker[key] = 0;
                    if (votes[key] > localVoteTracker[key]) {
                        localVoteTracker[key] = votes[key];
                        activeSongName = key.toUpperCase();
                        lastActiveSong.innerText = activeSongName;

                        // Ескі әнді лақтырып, жаңасын бірден қосу (INTERRUPT / SKIP LOGIC)
                        playLocalTrack(key);
                    }
                });

                totalVotesCount.innerText = total;
                updateRatingUI(votes);
            } catch (e) {
                console.log("Дерек алу қатесі");
            }
        }
        setInterval(fetchVotes, 1000); 

        function playLocalTrack(songKey) {
            currentPlayingKey = songKey;
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
            bpmText.innerText = "🥁 ТОЛЫҚ РЕЖИМ";
            djBall.style.backgroundColor = '#06b6d4';
            djBall.style.boxShadow = '0 0 50px #00f0ff';

            // Аудионы ойнату
            audioPlayer.src = window.location.origin + "/static/" + fileTarget + ".mp3";
            audioPlayer.load();

            if (audioPermissionGranted) {
                audioPlayer.play().catch(e => console.log("Дыбыс ойнату қатесі"));
            }

            // Шардың бит ырғағы
            if (beatInterval) clearInterval(beatInterval);
            beatInterval = setInterval(() => {
                djBall.style.transform = 'scale(1.2)';
                setTimeout(() => djBall.style.transform = 'scale(1)', 80);
            }, 450);

            // Таймерді тазалау (Енді ән үзілмейді, өзі табиғи біткенше толық ойнайды)
            timerText.innerText = "🔊 ӘН ТОЛЫҚ ОЙНАУДА...";

            // Ән өзі табиғи біткенде шарды бастапқы күйге келтіру
            audioPlayer.onended = function() {
                if (currentPlayingKey === songKey) {
                    clearInterval(beatInterval);
                    ballStatus.innerText = "АЯҚТАЛДЫ";
                    bpmText.innerText = "";
                    djBall.style.backgroundColor = '#0f172a';
                    djBall.style.boxShadow = 'none';
                    currentPlaying.innerText = "ӘН КҮТУДЕ... 🎵";
                    timerText.innerText = "";
                }
            };
        }

        function updateRatingUI(votes) {
            let sortedSongs = Object.keys(votes).map(key => ({ name: key, count: votes[key] })).filter(s => s.count > 0).sort((a, b) => b.count - a.count);

            if (sortedSongs.length === 0) {
                ratingList.innerHTML = `<p class="text-xs text-gray-500 text-center py-4">Соткадан ән жазыңыз... 🎼</p>`;
                return;
            }

            let maxVotes = sortedSongs[0].count || 1;
            ratingList.innerHTML = "";

            sortedSongs.slice(0, 3).forEach(song => {
                let percentage = (song.count / maxVotes) * 100;
                ratingList.innerHTML += `
                    <div>
                        <div class="flex justify-between text-[11px] mb-1 font-bold">
                            <span class="text-cyan-400 font-mono">🎵 ${song.name.toUpperCase()}</span>
                            <span class="text-fuchsia-400">${song.count} РЕТ</span>
                        </div>
                        <div class="w-full bg-slate-950 h-2 rounded-full">
                            <div class="bg-gradient-to-r from-cyan-400 to-fuchsia-500 h-2 rounded-full transition-all duration-300" style="width: ${percentage}%"></div>
                        </div>
                    </div>`;
            });
        }
    </script>
</body>
</html>
"""