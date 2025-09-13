let currentIndex = 0;
let stories = [];
let progressTimer = null;
let isPaused = false;
let duration = 5000; // стандартное время для картинок/текста

// Открыть сторис
function openStory(index) {
    currentIndex = index;
    stories = document.querySelectorAll(".story");
    document.getElementById("storyModal").style.display = "flex";
    renderProgressBars();
    showStory(currentIndex);
}

// Закрыть сторис
function closeStory() {
    const modal = document.getElementById("storyModal");
    const modalContent = document.getElementById("modalContent");

    clearInterval(progressTimer);

    // Останавливаем все видео
    const videos = modalContent.querySelectorAll("video");
    videos.forEach(video => {
        video.pause();
        video.currentTime = 0;
    });

    modal.style.display = "none";
    modalContent.innerHTML = "";
    document.getElementById("progressContainer").innerHTML = "";
}

// Показать текущий сторис
function showStory(index) {
    const modalContent = document.getElementById("modalContent");

    modalContent.innerHTML = "";

    let story = stories[index];

    if (story.querySelector(".story-text-preview")) {
        // Текст
        let textDiv = document.createElement("div");
        textDiv.innerText = story.querySelector(".story-text-preview").innerText;
        modalContent.appendChild(textDiv);
        duration = 5000;

    } else if (story.querySelector("img") && story.querySelector("img").dataset.video) {
        // Видео
        let video = document.createElement("video");
        video.src = story.querySelector("img").dataset.video;
        video.controls = false;
        video.autoplay = true;

        modalContent.appendChild(video);

        video.onloadedmetadata = () => {
            duration = video.duration * 1000;
            startProgress(index);
        };

        video.onended = () => nextStory();

        // Отмечаем просмотренной
        story.classList.add("viewed");
        return;

    } else if (story.querySelector("img")) {
        // Картинка
        let image = document.createElement("img");
        image.src = story.querySelector("img").src;
        modalContent.appendChild(image);
        duration = 5000;
    }

    // Отмечаем просмотренной
    story.classList.add("viewed");

    startProgress(index);
}

// Прогресс-бары для всех сторис
function renderProgressBars() {
    const progressContainer = document.getElementById("progressContainer");
    progressContainer.innerHTML = "";

    for (let i = 0; i < stories.length; i++) {
        let bar = document.createElement("div");
        bar.classList.add("progress-bar");

        let fill = document.createElement("div");
        fill.classList.add("progress-fill");

        if (i < currentIndex) {
            fill.style.width = "100%"; // предыдущие полные
        } else if (i === currentIndex) {
            fill.style.width = "0"; // текущий заполняется
        } else {
            fill.style.width = "0"; // следующие пустые
        }

        bar.appendChild(fill);
        progressContainer.appendChild(bar);
    }
}

// Анимация прогресса
function startProgress(index) {
    clearInterval(progressTimer);

    const fills = document.querySelectorAll(".progress-fill");
    const currentFill = fills[index];

    let width = 0;
    progressTimer = setInterval(() => {
        if (!isPaused) {
            width += 100 / (duration / 100);
            currentFill.style.width = width + "%";
            if (width >= 100) {
                clearInterval(progressTimer);
                nextStory();
            }
        }
    }, 100);
}

// Навигация
function nextStory() {
    if (currentIndex < stories.length - 1) {
        currentIndex++;
        renderProgressBars();
        showStory(currentIndex);
    } else {
        closeStory();
    }
}

function prevStory() {
    if (currentIndex > 0) {
        currentIndex--;
        renderProgressBars();
        showStory(currentIndex);
    }
}

// Пауза при удержании
function pauseStory() { isPaused = true; }
function resumeStory() { isPaused = false; }

// Навешиваем слушатели
document.addEventListener("mousedown", pauseStory);
document.addEventListener("mouseup", resumeStory);
document.addEventListener("touchstart", pauseStory);
document.addEventListener("touchend", resumeStory);
