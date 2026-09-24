# Requirements
Using Python, create a server web application which implements an API that receives, stores, and returns simple messages, according to the following specifications:

Two RESTful routes:

POST /messages: receives a message within the body of the request and records the message in the message log, by writing (appending) the message to a file on the local filesystem. The server should respond appropriately with the status code 201 Created. No response body content is necessary.

GET /messages: returns all messages contained within the message log, by reading the messages from the file on the local filesystem. The data should be returned as a JSON array within the response body, and the server should respond appropriately with the status code 200 OK and the Content-Type response header set correctly.

Both routes should be implemented according to REST standards. Test both of your routes using a tool such as Postman or curl.

CORS  should be implemented server-wide in order to support Ajax requests from client applications.

If a GET or POST request is received that does not conform to the paths defined above (or any others that you choose to implement), then the server should return an appropriate Not Found response, with the correct status code, and content that properly explains the reason for this response. The content type may be plain text or HTML; set the response header correctly.

Using JavaScript, create a client web application that communicates with your server application, using its API, on behalf of the user, with the following:

A simple form that allows the user to enter a message and click a button to record their message. Upon submission, the message should be sent to the server API using the Fetch API, using the appriorate API route above. The form should be styled to allow the user to easily enter a message of any length.

A list of messages that contains all messages returned by the server API, displayed in the order they are given. The messages should be requested from the server API using the Fetch API, using the appropriate API route above. The list should be styled to cleanly display a large list of messages, containing messages of any length.

After the user submits a new message to the server API, the list should be refreshed to reflect the new message. After the server responds from the initial request which sent the message, a subsequent request should be made to refresh the list.

All data sent and received to and from the server API should be implemented using Ajax requests.

You may take liberties to modify your application’s features and purpose from that described above, but the overall specifications and structure listed above should still be met.

Make your application look professional and presentable. Use valid HTML and CSS to structure and style your application.

No third-party JavaScript or CSS libraries or frameworks may be used without prior instructor permission.

# Practice
## HTML

    <main>
        <form class="message-form">
            <label for="message-input">Add a message</label>
            <textarea id="message-input" name="message" rows="4" required></textarea>
            <button type="submit">Post message</button>
            <p class="form-status" aria-live="polite"></p>
        </form>
        <section class="messages">

        </section>
    </main>

## JavaScript

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

## Python

    @app.route("/messages", methods=["GET"])
    def get_messages():
        messages = []

        with MESSAGE_FILE.open("r", encoding="utf-8") as file:
            for line in file:
                if line.strip():
                    messages.append(json.loads(line))

        return jsonify(messages), 200

    @app.route("/messages", methods=["POST"])
    def add_message():
        if not request.is_json:
            return jsonify({
                "error": "Content-Type must be application/json"
            }), 400

        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return jsonify({
                "error": "Request body must contain a JSON object"
            }), 400

        message = data.get("message")

        if not isinstance(message, str) or not message.strip():
            return jsonify({
                "error": "The message field must contain text"
            }), 400

        new_message = {
            "message": message.strip()
        }

        with MESSAGE_FILE.open("a+", encoding="utf-8") as file:
            file.seek(0, 2)

            if file.tell() > 0:
                file.seek(file.tell() - 1)
                last_character = file.read(1)

                if last_character != "\n":
                    file.write("\n")

            file.write(json.dumps(new_message) + "\n")

        return "", 201

# Zelda Question Info

Each question obtained from Open Trivia DB is an object with the following data members:

- question (str): the actual text of the question
- correct_answer (str): the correct answer to the question
- incorrect_answers: (Array[str]): a list of incorrect answers to the question

# Other Notes

Three tiered databases: Front end, back end, and databases.
Create interfaces that connect these three things in a way so changing any one of them won't break how the others work (or something like that).

DON'T PUT API KEYS IN THE FRONTEND OR ON GITHUB!!! Store it on the machine that runs your backend.

API stands for Application Programming Interface. It is a set of rules and protocols that allows different software applications to communicate and share data with each other.

## In this project

- Front end: all the html, css, javascript files, and media (anything in static or templates)
- Back end: server.py
- Database: messages.jsonl

The API is pretty much the GET and POST methods defined in server.py