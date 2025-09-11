let currentIndex = 0;
let stories = [];

// Открыть сторис
function openStory(index) {
    currentIndex = index;
    stories = document.querySelectorAll(".story");
    document.getElementById("storyModal").style.display = "flex";
    showStory(currentIndex);
}

// Закрыть сторис
function closeStory() {
    const modal = document.getElementById("storyModal");
    const modalContent = document.getElementById("modalContent");

    // Останавливаем все видео внутри модалки
    const videos = modalContent.querySelectorAll("video");
    videos.forEach(video => {
        video.pause();
        video.currentTime = 0; // сброс на начало
    });

    modal.style.display = "none";
    modalContent.innerHTML = ""; // чистим DOM, чтобы точно не играло
}

// Показать текущий сторис
function showStory(index) {
    const modalContent = document.getElementById("modalContent");
    modalContent.innerHTML = "";

    let story = stories[index];

    // Текстовая история
    if (story.querySelector(".story-text-preview")) {
        let textDiv = document.createElement("div");
        textDiv.innerText = story.querySelector(".story-text-preview").innerText;
        modalContent.appendChild(textDiv);

    // История с видео
    } else if (story.querySelector("img") && story.querySelector("img").dataset.video) {
        let video = document.createElement("video");
        video.src = story.querySelector("img").dataset.video;
        video.controls = true;
        video.autoplay = true;
        video.style.maxWidth = "100%";
        video.style.maxHeight = "100%";
        modalContent.appendChild(video);

    // История с картинкой
    } else if (story.querySelector("img")) {
        let image = document.createElement("img");
        image.src = story.querySelector("img").src;
        image.style.maxWidth = "100%";
        image.style.maxHeight = "100%";
        modalContent.appendChild(image);
    }
}

// Навигация
function nextStory() {
    if (currentIndex < stories.length - 1) {
        showStory(++currentIndex);
    } else {
        closeStory();
    }
}

function prevStory() {
    if (currentIndex > 0) {
        showStory(--currentIndex);
    }
}
