// static/js/popup.js

function openPopup(url) {
    // Open a small centered window
    const width = 500;
    const height = 600;
    const left = (window.screen.width / 2) - (width / 2);
    const top = (window.screen.height / 2) - (height / 2);

    window.open(
        url,
        "popupWindow",
        `width=${width},height=${height},top=${top},left=${left},scrollbars=yes,resizable=yes`
    );
}

function closePopupAndRefresh() {
    if (window.opener) {
        window.opener.location.reload(); // Refresh main page to show new log
    }
    window.close(); // Close popup
}