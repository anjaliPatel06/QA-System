async function askQuestion() {
    const context = document.getElementById("context").value;
    const question = document.getElementById("question").value;

    if (!context || !question) {
        alert("Please enter both context and question");
        return;
    }

    document.getElementById("answer").innerText = "Loading...";
    document.getElementById("confidence").innerText = "...";

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                context: context,
                question: question
            })
        });

        const data = await response.json();

        document.getElementById("answer").innerText = data.answer;
        document.getElementById("confidence").innerText = data.confidence;

    } catch (error) {
        document.getElementById("answer").innerText = "Error occurred";
        document.getElementById("confidence").innerText = "-";
        console.error(error);
    }
}
