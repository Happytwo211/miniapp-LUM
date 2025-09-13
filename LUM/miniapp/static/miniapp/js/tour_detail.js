// Переключение выпадающих блоков экскурсии
function toggleElement(header) {
    const content = header.nextElementSibling;
    const isActive = header.classList.contains("active");

    // Закрыть все элементы перед открытием нового
    document.querySelectorAll(".tour-element-header").forEach(h => h.classList.remove("active"));
    document.querySelectorAll(".tour-element-content").forEach(c => c.style.display = "none");

    if (!isActive) {
        header.classList.add("active");
        content.style.display = "block";
    }
}

// 🔙 Функция возврата
function handleBack() {
    if (document.referrer) {
        history.back();
    } else {
        window.location.href = "/tours/"; // замени на свой url
    }
}
