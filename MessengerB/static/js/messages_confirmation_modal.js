const confirmationModal = () => {
    const confirmation = document.querySelector('.confirmation');

    document.querySelector('.chat__clear-messages').addEventListener("click", function () {
        confirmation.style.display = 'block';
    });

    document.querySelector('.close-btn').addEventListener("click", function () {
        confirmation.style.display = 'none';
    });

    document.querySelector('.close-confirm').addEventListener("click", function () {
        confirmation.style.display = 'none';
    });
}

confirmationModal();