# templates.py

HTML_CONTROLLER = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Taldyk Summer - Әнге Дауыс Беру</title>
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>
<body class="h-screen bg-slate-950 text-white flex flex-col justify-between p-6 text-center select-none overflow-hidden">
    <div>
        <span class="text-xs font-bold text-fuchsia-500 uppercase tracking-widest">Taldyk Summer • Crowd AI DJ</span>
        <h1 class="text-xl font-black mt-1 text-cyan-400">🔥 ӘНГЕ ДАУЫС БЕРУ</h1>
        <p class="text-xs text-gray-400 mt-2">Папкадағы хиттер: Ворона, Шашлындос, Девочка, Истерика, Не получается, Пломбир, Твои глаза.</p>
    </div>

    <div class="bg-slate-900/80 border border-slate-800 p-6 rounded-2xl space-y-4 my-auto shadow-xl">
        <h3 class="text-xs font-bold text-fuchsia-400 uppercase text-left">🎼 Ән немесе Автор аты:</h3>
        <form onsubmit="sendVote(event)" class="flex flex-col gap-3">
            <input type="text" id="songInput" placeholder="Мысалы: Шашлындос, Пломбир, Ворона" required
                   class="w-full bg-slate-950 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white focus:outline-none focus:border-cyan-400">
            <button type="submit" class="w-full bg-gradient-to-r from-fuchsia-500 to-cyan-500 text-black font-black py-3 rounded-xl text-sm">
                👍 ДАУЫС БЕРУ (VOTE)
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
                    alert(`"${songName}" әніне дауыс қабылданды! 🚀`);
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
            <span class="text-xs font-bold text-cyan-400 tracking-widest uppercase">Crowdsourced AI DJ System v6</span>
            <h1 class="text-2xl font-black tracking-wider text-white">TALDYK SUMMER <span class="text-fuchsia-500">LIVE SCREEN</span></h1>
        </div>
        <div class="bg-slate-900 border border-cyan-500/30 px-4 py-2 rounded-xl text-center">
            <span class="text-[10px] text-gray-400 block uppercase">ҚАЗІР ЗАЛДЫ ЖАРЫП ТҰРҒАН ӘН:</span>
            <span id="currentPlaying" class="text-sm font-black text-green-400">ДАУЫС БЕРУДІ КҮТУДЕ... 🎵</span>
        </div>
    </header>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 my-auto items-center">
        <div class="bg-slate-900/60 border border-slate-800 p-6 rounded-3xl space-y-4">
            <h2 class="text-sm font-black text-fuchsia-400 tracking-wider uppercase border-b border-slate-800 pb-2">📊 ҚОНАҚТАР ТАНДАУЫ (ТОП):</h2>
            <div id="ratingList" class="space-y-4">
                <p class="text-xs text-gray-500 text-center py-4">Телефоннан ән жазып, дауыс беріңіз... 🎼</p>
            </div>
        </div>

        <div class="flex flex-col items-center justify-center relative h-64" style="cursor: pointer;" onclick="forceInitAudio()">
            <div id="ticker" class="absolute top-0 w-full text-center text-xs font-bold text-yellow-300 tracking-wide">
                🚨 ДЫБЫСТЫ ҚОСУ ҮШІН ЭКРАНДЫ 1 РЕТ БАСЫҢЫЗ!
            </div>

            <audio id="localAudioPlayer" crossorigin="anonymous"></audio>

            <div id="djBall" class="w-36 h-36 rounded-full bg-slate-900 border-4 border-slate-700 flex flex-col items-center justify-center transition-all duration-75 text-center p-2">
                <span id="ballStatus" class="text-[10px] font-black text-gray-500 uppercase">КҮТУДЕ</span>
                <span id="bpmText" class="text-[9px] text-cyan-400 font-mono mt-1"></span>
            </div>
            <div id="timerText" class="text-xs text-fuchsia-400 mt-4 font-mono h-4 font-bold"></div>
        </div>

        <div class="bg-slate-900/60 border border-slate-800 p-6 rounded-3xl text-xs space-y-2 text-gray-300">
            <p class="text-cyan-400 font-bold text-sm">👑 SMART HTTP POLLING SYSTEM:</p>
            <p>• <strong>Safe Connection:</strong> Вебсокетсіз, таза HTTP арқылы істейді. Ешқашан бұғатталмайды.</p>
            <p>• <strong>Автоматты Кезек:</strong> Таймер аяқталғанда, жүйе ең көп дауыс алған әнді папкадан өзі қосады.</p>
        </div>
    </div>

    <footer class="w-full border-t border-slate-800 pt-4 flex justify-between items-center bg-slate-950 p-4 rounded-2xl">
        <div class="text-[10px] text-gray-400">TALDYK SUMMER REAL INTERACTIVE REMIXER v6</div>
        <div class="bg-white p-2 rounded-2xl flex items-center gap-4 text-black shadow-lg">
            <div id="qrcode" class="p-1 bg-white rounded-lg"></div>
            <div class="text-left pr-4">
                <h4 class="text-xs font-black uppercase tracking-wide text-slate-950">Өз әніңді жаз</h4>
                <p class="text-[9px] text-gray-600 mt-0.5 leading-tight">Камерамен сканерле де, дауыс бер!</p>
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

        let isPlaying = false;
        let beatInterval = null;
        let audioPermissionGranted = false;
        let currentVotesGlobal = {};

        function forceInitAudio() {
            audioPermissionGranted = true;
            ticker.innerText = "🎵 ДЫБЫС ЖҮЙЕСІ БЕЛСЕНДІ! Дауыс күтуде...";
            ticker.style.color = "#10b981";
        }

        // 🔄 СЕРВЕРДЕН ДАУЫСТАРДЫ ӘР 1 СЕКУНД САЙЫН АВТОМАТТЫ СУЫРЫП АЛЫП ТҰРУ (POLLING)
        async function fetchVotes() {
            try {
                const response = await fetch('/get_votes');
                const votes = await response.json();
                currentVotesGlobal = votes;
                updateRatingUI(votes);

                if (!isPlaying) {
                    checkAndPlayWinner(votes);
                }
            } catch (e) {
                console.log("Дерек алу қатесі");
            }
        }
        setInterval(fetchVotes, 1000); // 1 секунд сайын тірілей жаңарту

        function checkAndPlayWinner(votes) {
            if (isPlaying) return;
            let sorted = Object.keys(votes).map(key => ({ name: key, count: votes[key] })).sort((a, b) => b.count - a.count);
            if (sorted.length === 0 || sorted[0].count === 0) return;

            let winner = sorted[0];

            // Сервердегі дауысын нөлдеу сұранысы
            const formData = new FormData();
            formData.append('song_key', winner.name);
            fetch('/reset_vote', { method: 'POST', body: formData });

            playLocalTrack(winner.name);
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

            currentPlaying.innerText = displayName.toUpperCase() + " (ЗАЛ ТАНДАУЫ 👑)";
            ballStatus.innerText = "LIVE PLAYING";
            bpmText.innerText = "🥁 АКТИВТІ БИТ";
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

            let timeLeft = 20; 
            timerText.innerText = `⏳ Ремикс уақыты: ${timeLeft} сек`;
            let countdown = setInterval(() => {
                timeLeft--;
                if (timeLeft > 0 && isPlaying) { timerText.innerText = `⏳ Ремикс уақыты: ${timeLeft} сек`; } 
                else { clearInterval(countdown); }
            }, 1000);

            setTimeout(() => {
                clearInterval(beatInterval);
                audioPlayer.pause();
                isPlaying = false;
            }, 20000);
        }

        function updateRatingUI(votes) {
            let sortedSongs = Object.keys(votes).map(key => ({ name: key, count: votes[key] })).filter(s => s.count > 0).sort((a, b) => b.count - a.count);

            if (sortedSongs.length === 0) {
                ratingList.innerHTML = `<p class="text-xs text-gray-500 text-center py-4">Кезек бос... 🎼</p>`;
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
                            <span class="text-fuchsia-400">${song.count} ДАУЫС</span>
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