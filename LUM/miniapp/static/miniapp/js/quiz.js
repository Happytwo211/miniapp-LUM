document.addEventListener("DOMContentLoaded", () => {
    const questionBlocks = document.querySelectorAll(".quiz-question-block");
    const quizContainer = document.querySelector(".quiz-container");
    let currentIndex = 0;
    let score = 0;

    const quizId = quizContainer.dataset.quizId;
    const totalQuestions = questionBlocks.length;

    function showNextQuestion() {
        if (currentIndex < questionBlocks.length - 1) {
            questionBlocks[currentIndex].classList.add("hidden");
            currentIndex++;
            questionBlocks[currentIndex].classList.remove("hidden");
        } else {
            // показать результат
            quizContainer.classList.add("hidden");
            const result = document.querySelector(".quiz-result");
            result.classList.remove("hidden");
            document.getElementById("quiz-score").innerText =
                `Вы ответили правильно на ${score} из ${totalQuestions}`;

            // сохранить результат в БД
            fetch("/quiz/save-result/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: JSON.stringify({
                    quiz_id: quizId,
                    score: score,
                    total_questions: totalQuestions,
                }),
            })
                .then((res) => res.json())
                .then((data) => console.log("✅ Результат сохранён:", data))
                .catch((err) => console.error("❌ Ошибка сохранения:", err));
        }
    }

    questionBlocks.forEach((block) => {
        const options = block.querySelectorAll(".quiz-option");
        options.forEach((btn) => {
            btn.addEventListener("click", () => {
                const isCorrect = btn.dataset.correct === "true";

                if (isCorrect) {
                    btn.classList.add("correct");
                    score++;
                } else {
                    btn.classList.add("wrong");
                    options.forEach(opt => {
                        if (opt.dataset.correct === "true") {
                            opt.classList.add("correct");
                        }
                    });
                }

                options.forEach(opt => (opt.disabled = true));
                setTimeout(showNextQuestion, 1000);
            });
        });
    });

    // 🔑 Функция для получения CSRF-токена
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
