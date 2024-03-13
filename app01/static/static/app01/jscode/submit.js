let float_window = document.getElementById('float_window');
document.getElementById('SubmitButton').addEventListener('mouseover', function () {
    float_window.style.display = 'block';
    this.style.backgroundColor = ' rgb(180, 243, 222)';
});  //显示浮窗

document.addEventListener('click', function (event) {
    if (event.target !== float_window && !float_window.contains(event.target)) {
        float_window.style.display = 'none';
        SubmitButton.style.backgroundColor = 'rgb(234, 248, 244)';
    }
});//点击空白处浮窗消失

