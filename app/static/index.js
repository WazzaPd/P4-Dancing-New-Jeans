window.onload = function () {
    const clickMe = document.getElementById('click');

    clickMe.addEventListener('click', () => {
        const main = document.getElementById('main');

        for (let i = 0; i < 100; i++) {
            setTimeout(() => {
                main.style.fontSize = `${i}px`;
                main.style.color = `rgb(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)})`;
            }, i * 100);
        }
    });
};  