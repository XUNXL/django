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
var username = textContent.substring(0); // 从索引为 5 的位置开始提取字符串
console.log(username); // 输出 "{{ username }}"

document.querySelector(".picture1").addEventListener("click", function () {
    document.querySelector(".modal-body").innerHTML = `<img src="../static/images/${username}.jpg" style = "width:100%; height:100%">`;
    console.log(document.querySelector(".modal-body").innerHTML);
});

document.querySelector(".picture2").addEventListener("click", function () {
    document.querySelector(".modal-body").innerHTML = `<img src="../static/images/${username}_result.jpg" style = "width:100%; height:100%">`;
});

document.querySelector(".picture3").addEventListener("click", function () {
    document.querySelector(".modal-body").innerHTML = `<img src="../static/images/${username}_normalize.jpg" style = "width:100%; height:100%">`;
});

let ifshow = false;
document.querySelector(".getResult").addEventListener("click", function () {
    document.querySelector(".getResult span").style.display = "inline";
    document.querySelector(".alert-danger").style.display = "none";
    var imgElement = document.getElementById("image");

    // 设置图片的 src 属性
    imgElement.src = `../static/images/${username}.jpg`;

    imgElement.onload = function () {
        // 图片存在，设置相应的 div 显示
        let loader = setTimeout(function () {
            document.querySelector(".dots-container").style.display = "flex";
        }, 0)
        document.querySelector(".result_picture").style.display = "flex";
        document.querySelector(".alert-success").style.display = "block";
        document.querySelector(".result_download").style.display = "block";

        // 设置 ifshow 为 true
        ifshow = true;
        // 根据 ifshow 的值执行后续逻辑
        if (ifshow) {
            clearTimeout(loader);
            document.querySelector(".getResult span").style.display = "none";
            document.querySelector(".getResult button").innerHTML = "检测完毕";
        }
    };
    // 监听图片加载失败事件
    imgElement.onerror = function () {
        let loader = setTimeout(function () {
            document.querySelector(".dots-container").style.display = "flex";
        }, 0)
        // 图片不存在，设置相应的 div 隐藏
        document.querySelector(".result_picture").style.display = "none";
        document.querySelector(".alert-success").style.display = "none";
        document.querySelector(".result_download").style.display = "none";
        // 设置 ifshow 为 false
        ifshow = false;
        // 根据 ifshow 的值执行后续逻辑
        if (!ifshow) {
            setTimeout(() => {
                document.querySelector(".dots-container").style.display = "none";
                clearTimeout(loader);
                document.querySelector(".getResult span").style.display = "none";
                document.querySelector(".getResult button").innerHTML = "重新检测";
                document.querySelector(".alert-danger").style.display = "block";
            }, 5000);
        }
    }
});

