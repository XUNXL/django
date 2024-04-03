var paragraph = document.querySelector(".job");

// 遍历 <p> 标签的子节点
var childNodes = paragraph.childNodes;
var textContent = "";

for (var i = 0; i < childNodes.length; i++) {
    var node = childNodes[i];

    // 判断节点类型为文本节点
    if (node.nodeType === Node.TEXT_NODE) {
        // 获取文本节点的内容，并去除首尾空白字符
        var content = node.textContent.trim();
        textContent += content;
    }
}
var username = textContent.substring(0);
console.log(username); // 输出 "{{ username }}"

document.querySelector(".picture1").addEventListener("click", function () {
    document.querySelector(".modal-body").innerHTML = `<img src="../static/images/${username}.jpg" style = "width:100%; height:100%">`;
    console.log(document.querySelector(".modal-body").innerHTML);
});

document.querySelector(".picture2").addEventListener("click", function () {
    document.querySelector(".modal-body").innerHTML = `<img src="../static/images/${username}_normalize.jpg" style = "width:100%; height:100%">`;
});

document.querySelector(".picture3").addEventListener("click", function () {
    document.querySelector(".modal-body").innerHTML = `<img src="../static/images/${username}_result.jpg" style = "width:100%; height:100%">`;
});

document.querySelector(".getResult").addEventListener("click", function () {
    document.querySelector(".dots-container").style.display = "flex";
    document.querySelector(".getResult span").style.display = "inline";
    document.querySelector(".result_picture").style.display = "none";
});


