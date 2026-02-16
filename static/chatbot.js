document.getElementById('dark-toggle').addEventListener('click', () = {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
});

window.addEventListener('load', () = {
    if (localStorage.getItem('darkMode') === 'true') {
        document.body.classList.add('dark-mode');
    }
});

function previewImage(event) {
    const reader = new FileReader();
    reader.onload = function(){
        const output = document.getElementById('imagePreview');
        output.src = reader.result;
        output.style.display = 'block';
    };
    reader.readAsDataURL(event.target.files[0]);
}

document.getElementById('ask-button').addEventListener('click', () = {
    const userInput = document.getElementById('user-input').value.toLowerCase().trim();
    const responseBox = document.getElementById('chat-response');

    let response = 🤔 I’m not sure — try asking something grape-related!;
    if (userInput.includes(black rot)) {
        response = 🍄 Black Rot is a fungal disease. Remove infected leaves and apply fungicide early.;
    } else if (userInput.includes(esca)) {
        response = 🍂 ESCA requires pruning infected vines. No chemical cure available.;
    } else if (userInput.includes(healthy)) {
        response = 🍇 Grapes are rich in Vitamin C, Vitamin K, and antioxidants.;
    } else if (userInput.includes(grape varieties)) {
        response = 🍷 Common grape varieties include Concord, Thompson Seedless, and Red Globe.;
    }

    responseBox.textContent = response;
});
