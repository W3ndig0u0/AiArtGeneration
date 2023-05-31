function chat() {
  const user_input = document.getElementById('user-input').value;
  if (user_input.trim() !== "") {
    fetch('/process_input', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ user_input: user_input })
    })
    .then(response => response.json())
    .then(data => {
      const response = data?.response;
      const chatHistory = document.getElementById('chat-history');
  const userMessage = `<div class="user-message">
                          <div class="message-bubble">
                            <img src="https://i.etsystatic.com/38867718/r/il/6996f5/4392363952/il_570xN.4392363952_d009.jpg" alt="User Avatar" class="avatar">
                            <div class="message-content">
                              <span class="message-text">${user_input}</span>
                            </div>
                          </div>
                        </div>`;
  const aiMessage = `<div class="ai-message">
                       <div class="message-bubble">
                         <img src="https://www.uu.se/digitalAssets/895/c_895428-l_3-k_image.jpg" alt="Ai Avatar" class="avatar">
                         <div class="message-content">
                           <span class="message-text">${response}</span>
                         </div>
                       </div>
                     </div>`;

      if (user_input.trim() !== "") {
        chatHistory.innerHTML += userMessage;
      }

      if (response) {
        chatHistory.innerHTML += aiMessage;
      }

      document.getElementById('user-input').value = "";
      document.getElementById('user-input').focus();

      // Scroll to the bottom of the chat history
      chatHistory.scrollTop = chatHistory.scrollHeight;
    })
    .catch(error => {
      console.log(error);
    });
  }
}


function handleKeyDown(event) {
  if (event.keyCode === 13) {
    chat();
  }
}
