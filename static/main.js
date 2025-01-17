function copyToClipboard(button) {
    const text = 'curl -fsSL https://jprq.io/install.sh | sudo bash';
    navigator.clipboard.writeText(text).then(() => {
        button.classList.add('copied');
        setTimeout(() => button.classList.remove('copied'), 2000);
    }).catch(err => {
        alert('Failed to copy: ' + err);
    });
}


