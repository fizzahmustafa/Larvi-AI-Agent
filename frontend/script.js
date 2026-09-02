const API_URL = "http://127.0.0.1:8000/chat";

const chatBox = document.getElementById("chatBox");
const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const typing = document.getElementById("typing");


function addMessage(text, sender) {

    const message = document.createElement("div");
    message.className = `message ${sender}`;

    const content = document.createElement("div");
    content.className = "message-content";

    content.textContent = text;

    message.appendChild(content);
    chatBox.appendChild(message);

    chatBox.scrollTop = chatBox.scrollHeight;
}


function removeWelcome() {

    const welcome = document.querySelector(".welcome");

    if (welcome) {
        welcome.remove();
    }
}


function showTyping() {
    typing.style.display = "flex";
}


function hideTyping() {
    typing.style.display = "none";
}


function formatResponse(data) {

    if (!data) {
        return "I didn't receive a response.";
    }

    if (typeof data === "string") {
        return data;
    }

    if (data.response) {
        data = data.response;
    }

    if (data.message) {

        let text = data.message;

        if (data.result) {
            text += "\n\n" + formatResult(data.result);
        }

        return text;
    }

    if (data.result) {
        return formatResult(data.result);
    }

    if (data.error) {
        return "Error: " + data.error;
    }

    return JSON.stringify(data, null, 2);
}


function formatResult(result) {

    if (!result) {
        return "";
    }

    if (typeof result === "string") {
        return result;
    }

    if (Array.isArray(result)) {

        if (result.length === 0) {
            return "No results found.";
        }

        return result.map((item, index) => {

            if (typeof item === "object") {

                const lines = Object.entries(item)
                    .filter(([key, value]) => value !== null && value !== "")
                    .map(([key, value]) => {

                        let displayValue = value;

                        if (typeof value === "object") {
                            displayValue = JSON.stringify(value);
                        }

                        return `${key}: ${displayValue}`;
                    });

                return `${index + 1}. ${lines.join("\n")}`;

            }

            return `${index + 1}. ${item}`;

        }).join("\n\n");
    }


    if (typeof result === "object") {

        if (result.event) {

            const event = result.event;

            return [
                `Event: ${event.summary || "Untitled"}`,
                `Start: ${event.start || ""}`,
                `End: ${event.end || ""}`,
                event.location ? `Location: ${event.location}` : ""
            ]
            .filter(Boolean)
            .join("\n");
        }

        if (result.summary) {
            return result.summary;
        }

        if (result.body) {
            return result.body;
        }

        if (result.message) {
            return result.message;
        }

        return Object.entries(result)
            .map(([key, value]) => {

                if (typeof value === "object") {
                    value = JSON.stringify(value, null, 2);
                }

                return `${key}: ${value}`;

            })
            .join("\n");
    }

    return String(result);
}


async function sendMessage() {

    const message = messageInput.value.trim();

    if (!message) {
        return;
    }

    removeWelcome();

    addMessage(message, "user");

    messageInput.value = "";

    messageInput.style.height = "auto";

    sendButton.disabled = true;

    showTyping();

    try {

        const response = await fetch(API_URL, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })
        });


        const data = await response.json();

        hideTyping();

        if (!response.ok) {

            addMessage(
                "Something went wrong: " +
                (data.error || "Server error"),
                "assistant"
            );

            return;
        }


        const reply = formatResponse(data);

        addMessage(reply, "assistant");

    }

    catch (error) {

        hideTyping();

        addMessage(
            "Unable to connect to Larvi. Make sure the FastAPI server is running.",
            "assistant"
        );

        console.error(error);
    }

    finally {

        sendButton.disabled = false;

        messageInput.focus();
    }
}


function sendSuggestion(message) {

    messageInput.value = message;

    sendMessage();
}


function newChat() {

    chatBox.innerHTML = `

        <div class="welcome">

            <div class="welcome-icon">
                L
            </div>

            <h2>How can I help you?</h2>

            <p>
                I can manage your emails, calendar,
                and help you organize your day.
            </p>

            <div class="suggestions">

                <button onclick="sendSuggestion('Show me my latest emails')">
                    <span>✉</span>
                    Show my latest emails
                </button>

                <button onclick="sendSuggestion('Show my calendar')">
                    <span>▣</span>
                    Show my calendar
                </button>

                <button onclick="sendSuggestion('Summarize my latest email')">
                    <span>✦</span>
                    Summarize an email
                </button>

                <button onclick="sendSuggestion('Search my calendar for Larvi')">
                    <span>⌕</span>
                    Search calendar
                </button>

            </div>

        </div>
    `;

    messageInput.focus();
}


function handleKey(event) {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();

        sendMessage();
    }
}


messageInput.addEventListener("input", function () {

    this.style.height = "auto";

    this.style.height =
        Math.min(this.scrollHeight, 120) + "px";
});


messageInput.focus();
