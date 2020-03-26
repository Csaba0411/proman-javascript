let passwordInputs = document.querySelectorAll('.password');
let checkBox = document.querySelector('#checkbox');

if (checkBox) {
    checkBox.addEventListener('click', function () {
        for (let item of passwordInputs) {
            if (item.type === 'password') {
                item.type = 'text';
            } else {
                item.type = 'password'
            }
        }
    });
}