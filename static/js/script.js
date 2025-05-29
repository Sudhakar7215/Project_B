function quickReply(text) {
    document.getElementById("user-input").value = text;
    submitChat(new Event("submit"));
}

async function submitChat(event) {
    event.preventDefault();
    const userInput = document.getElementById("user-input").value;
    document.getElementById("user-input").value = "";

    // Display user input in chatbox
    const chatbox = document.getElementById("chatbox");
    const userMessage = document.createElement("div");
    userMessage.classList.add("message", "user");
    userMessage.innerHTML = `<div class="user-icon"></div><div class="user-text">${userInput}</div>`;
    chatbox.appendChild(userMessage);

    // Show typing indicator
    const typingIndicatorContainer = document.getElementById("typing-indicator-container");
    typingIndicatorContainer.classList.remove("hidden");
    
    chatbox.scrollTop = chatbox.scrollHeight;

    try {
        console.log("Sending user input to server:", userInput);
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: userInput })
        });

        const result = await response.json();
        console.log("Received response from server:", result);

        // Hide typing indicator
        typingIndicatorContainer.classList.add("hidden");

        const botMessage = document.createElement("div");
        botMessage.classList.add("message", "bot");
        //botMessage.innerHTML = `<div class="bot-icon"></div><div class="bot-text">Chitti: ${result.reply}</div>`;
        botMessage.innerHTML = `
            <div class="bot-icon"></div>
            <div class="bot-text">
                Chitti: ${result.reply}
                <div class="token-info">
                    <small>Prompt Tokens: ${result.prompt_tokens}, Completion Tokens: ${result.completion_tokens}, Total Tokens: ${result.total_tokens}, Estimated Cost: $${result.estimated_cost_usd.toFixed(6)}</small>
                </div>
            </div>
        `;

        chatbox.appendChild(botMessage);
        chatbox.scrollTop = chatbox.scrollHeight;

    } catch (error) {
        console.error("Error during fetch operation:", error);

        // Hide typing indicator
        typingIndicatorContainer.classList.add("hidden");

        const errorMessage = document.createElement("div");
        errorMessage.classList.add("message", "bot");
        errorMessage.innerHTML = `<div class="bot-icon"></div><div class="bot-text">Chitti: An error occurred. Please try again.</div>`;
        chatbox.appendChild(errorMessage);
    }
}
