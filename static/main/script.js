const messageSection = document.querySelector(".messages");
const messageForm = document.querySelector(".message-form");
const messageInput = document.querySelector("#message-input");
const formStatus = document.querySelector(".form-status");

async function getMessages() {
    messageSection.textContent = "Loading messages...";

    try {
        const response = await fetch("/messages");

        if (!response.ok) {
            throw new Error(`The server returned ${response.status}.`);
        }

        const messages = await response.json();
        messageSection.replaceChildren();

        if (messages.length === 0) {
            messageSection.textContent = "No messages have been posted yet.";
            return;
        }

        messages.forEach((messageData) => {
            const message = document.createElement("p");
            message.textContent = messageData.message;
            messageSection.append(message);
        });
    } catch (error) {
        messageSection.textContent = "Unable to load messages.";
        console.error(error);
    }
}

async function addMessage(event) {
    event.preventDefault();

    const message = messageInput.value.trim();

    if (!message) {
        formStatus.textContent = "Please enter a message.";
        return;
    }

    const submitButton = messageForm.querySelector("button");
    submitButton.disabled = true;
    formStatus.textContent = "Posting message...";

    try {
        const response = await fetch("/messages", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ message })
        });

        if (!response.ok) {
            throw new Error(`The server returned ${response.status}.`);
        }

        messageForm.reset();
        formStatus.textContent = "Message posted.";
        await getMessages();
    } catch (error) {
        formStatus.textContent = "Unable to post message.";
        console.error(error);
    } finally {
        submitButton.disabled = false;
    }
}

messageForm.addEventListener("submit", addMessage);
getMessages();