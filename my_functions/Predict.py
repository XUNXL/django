
import torch
import torch.backends
from torch.nn import CrossEntropyLoss
from torchvision.models import vgg16
from torchvision.transforms import transforms
from baal.bayesian.dropout import patch_module
from baal import ModelWrapper

import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image
import json

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def normalize(img, mean, std):
    img_array = np.array(img).astype(np.float32)
    img1_mean, img1_std = img_array.mean(
        axis=(0, 1)), img_array.std(axis=(0, 1))
    # 标准化图像
    img_array = (img_array - img1_mean) / img1_std
    img_array = img_array * std + mean
    # 将数据类型转换回整型
    img_array = np.clip(img_array, 0, 255).astype(np.uint8)
    img_normalized = Image.fromarray(img_array)
    return img_normalized


def run_predict(img_path, save_path1, save_path2):
    mean = [187.74448, 95.00587, 23.374166]
    std = [27.05076, 28.098957, 14.033631]
    # use_cuda = torch.cuda.is_available()
    torch.backends.cudnn.benchmark = True
    data_transform = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(3 * [0.5], 3 * [0.5]),
        ]
    )
    # load image
    # img_path = "D:\青光眼辅助诊断系统\数据集\ACRIMA原始数据集\ACRIMA\\val\\Normal\Im231_ACRIMA.jpg"
    # img_path = "./Test/Images/drishtiGS_001.jpg"
    assert os.path.exists(
        img_path), "file: '{}' dose not exist.".format(img_path)
    img_init = Image.open(img_path)
    img_init = normalize(img_init, mean, std)  # 标准化
    print(type(img_init))
    img_init.save(save_path1)

    # [N, C, H, W]
    img = data_transform(img_init)
    img = torch.unsqueeze(img, dim=0)
    # 读取类别
    json_path = './my_functions/class_indices.json'
    assert os.path.exists(
        json_path), "file: '{}' dose not exist.".format(json_path)
    with open(json_path, "r") as f:
        class_indict = json.load(f)
    print("load json")
    # model = model.to(device)
    img = img.to(device)

    criterion = CrossEntropyLoss()
    model = vgg16(weights=None, num_classes=2)
    # load model weights
    weights_path = "./my_functions/best_['bald'].pth"
    assert os.path.exists(
        weights_path), "file: '{}' dose not exist.".format(weights_path)
    # 加载权重
    checkpoint = torch.load(weights_path, map_location='cpu')
    model.load_state_dict(checkpoint['model'])
    print("load pth")
    # dropout层 改成 MCDropout
    model = patch_module(model)
    # if use_cuda:
    #     model.cuda()
    model = model.to(device)

    # 包装模型
    model = ModelWrapper(model, criterion, replicate_in_memory=False)

    # Validation!
    with torch.no_grad():
        predictions = model.predict_on_batch(
            img.to(device), iterations=100).cpu()  # iterations是进行mcdropout的次数
        result = torch.softmax(predictions, dim=1)

        max_values, max_indices = torch.max(
            result, dim=1)  # 每个iteration的最大概率及其对应类别
        mean_pro = torch.mean(result, dim=2)  # 对iteration的值求均值

        max_mean_pro, max_mean_indices = torch.max(
            mean_pro, dim=1)  # 两个类分别的概率 0是Positive，1是Negative
        print(max_mean_pro, max_mean_indices)

    for i in range(max_indices.size(1)):
        prediction_values = max_values[0, i]  # 维度0只有0，维度1有i次预测即i个
        prediction_indices = max_indices[0, i]
        print("Prediction {}: Probabilistic = {:.4f}, Class = {}".format(i, prediction_values,
                                                                         class_indict[str(prediction_indices.numpy())]))
    # 暂时以平均概率值来判别分类类别
    print_res = "Probabilistic = {:.4f}, Class = {}".format(max_mean_pro[0],
                                                            class_indict[str(max_mean_indices[0].numpy())])
    probablistic = max_mean_pro[0]
    print(type(probablistic))
    class_result = class_indict[str(max_mean_indices[0].numpy())]
    # 预测熵
    mean_positive = torch.mean(result, dim=2)
    # print(mean_positive)
    predic_entropy = -torch.sum(mean_pro * torch.log2(mean_pro), dim=1)
    print('predic_entropy = ', predic_entropy)

    # 数据
    # 第二维=0，因为第二维表示类别，0在我的模型中表示正类。即取0位置的概率值就表示越接近1就越有可能是正类
    data = result[0, 0, :].numpy()
    bins = np.linspace(0, 1, num=50)
    # 绘制直方图
    fig, ax = plt.subplots()
    n, bins, patches = ax.hist(data, bins=bins)
    n = n.tolist()
    bins = bins.tolist()
    plt.xlabel("Probablistic")
    plt.ylabel("iterations")
    plt.savefig(save_path2)
    # plt.show()
    # 显示图形

    # plt.imshow(img_init)
    # plt.title(print_res)
    print(print_res)
    return probablistic.item(), class_result, predic_entropy, max_mean_pro, n, bins


    # plt.show()
if __name__ == "__main__":
    run_predict()
