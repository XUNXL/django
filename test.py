# 熏小漏 2023/7/4 20:55
# 熏小漏 2023/7/3 9:42
"""
训练器模块
"""
import os
import cv2
from torch_model import unet
#import unet
#import dataset
import torch
from torch_model import dataset
import torch.nn as nn

from tqdm import tqdm
from torch.utils.data import DataLoader
from torchvision.utils import save_image
import torchvision
from torchvision import transforms

# 训练器
class Trainer:

    def __init__(self, path, model, model_copy, img_save_path):
        self.path = path
        self.model = model
        self.model_copy = model_copy
        self.img_save_path = img_save_path
        self.trans=torchvision.transforms.Compose([torchvision.transforms.ToTensor()])
        # 使用的设备
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # 网络
        self.net = unet.UNet().to(self.device)
        # 优化器，这里用的Adam，跑得快点
        self.opt = torch.optim.Adam(self.net.parameters())
        # 这里直接使用二分类交叉熵来训练，效果可能不那么好
        # 可以使用其他损失，比如DiceLoss、FocalLoss之类的
        self.loss_func = nn.BCELoss()
        # 设备好，batch_size和num_workers可以给大点
        #self.loader = DataLoader(dataset.Datasets(path), batch_size=4, shuffle=True, num_workers=4)

        # 判断是否存在模型
        if os.path.exists(self.model):
            self.net.load_state_dict(torch.load(model))
            print(f"Loaded{model}!")
        else:
            print("No Param!")
        os.makedirs(img_save_path, exist_ok=True)

    # 训练
    def train(self, stop_value):
        epoch = 1
        while True:
            for inputs, labels in tqdm(self.loader, desc=f"Epoch {epoch}/{stop_value}",
                                       ascii=True, total=len(self.loader)):
                # 图片和分割标签
                inputs, labels = inputs.to(self.device), labels.to(self.device)
                # 输出生成的图像
                out = self.net(inputs)
                loss = self.loss_func(out, labels)
                # 后向
                self.opt.zero_grad()
                loss.backward()
                self.opt.step()

                # 输入的图像，取第一张
                x = inputs[0]
                # 生成的图像，取第一张
                x_ = out[0]
                # 标签的图像，取第一张
                y = labels[0]
                # 三张图，从第0轴拼接起来，再保存
                img = torch.stack([x, x_, y], 0)
                save_image(img.cpu(), os.path.join(self.img_save_path, f"{epoch}.png"))
                # print("image save successfully !")
            print(f"\nEpoch: {epoch}/{stop_value}, Loss: {loss}")
            torch.save(self.net.state_dict(), self.model)
            # print("model is saved !")

            # 备份
            if epoch % 50 == 0:
                torch.save(self.net.state_dict(), self.model_copy.format(epoch, loss))
                print("model_copy is saved !")
            if epoch > stop_value:
                break
            epoch += 1

    def imgtrans(self,img, size):
        # 图片的宽高
        h, w = img.shape[0:2]
        # 需要的尺寸
        _w = _h = size
        # 不改变图像的宽高比例
        scale = min(_h / h, _w / w)
        h = int(h * scale)
        w = int(w * scale)
        # 缩放图像
        img = cv2.resize(img, (w, h), interpolation=cv2.INTER_CUBIC)
        # 上下左右分别要扩展的像素数
        top = (_h - h) // 2
        left = (_w - w) // 2
        bottom = _h - h - top
        right = _w - w - left
        # 生成一个新的填充过的图像，这里用纯黑色进行填充(0,0,0)
        new_img = cv2.copyMakeBorder(img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0, 0, 0))
        return new_img

    def segment(self, imgpath,imgname):
        #if os.path.exists(self.model):
        #    self.net.load_state_dict(torch.load(model))
        # 图片和分割标签
        #inputs = cv2.imread(os.path.join(self.path,imgpath))
        inputs = cv2.imread(r"C:\Users\yxy\PycharmProjects\pythonProject\venv\Scripts\myproject\userimg\熏小漏.tif")
        inputs = cv2.cvtColor(inputs, cv2.COLOR_BGR2RGB)
        inputs = self.imgtrans(inputs,256)
        inputs = self.trans(inputs)
        inputs = inputs.to(self.device)
        inputs = torch.unsqueeze(inputs, 0)
        #inputs = transforms.ToTensor()(inputs)
        # 输出生成的图像
        out = self.net(inputs)
        #loss = self.loss_func(out, labels)
        # 后向
        #self.opt.zero_grad()
        #loss.backward()
        #self.opt.step()

        # 输入的图像，取第一张
        x = inputs[0]
        # 生成的图像，取第一张
        x_ = out[0]
        # 标签的图像，取第一张
        #y = labels[0]
        # 三张图，从第0轴拼接起来，再保存
        img = torch.stack([x, x_], 0)
        save_image(img.cpu(), os.path.join(self.img_save_path, f"{imgname}.png"))
        # print("image save successfully !")

        #print(f"\nEpoch: {epoch}/{stop_value}, Loss: {loss}")
        #torch.save(self.net.state_dict(), self.model)
        # print("model is saved !")


if __name__ == '__main__':
	# 路径改一下
    #t = Trainer(r"./data/DRIVE/training", r'./model.pt', r'./model_{}_{}.pt', img_save_path=r'./train_img')
    #t.train(300)
    #t = Trainer("./data/DRIVE/test/images", r'./model.pt', r'./model_{}_{}.pt', img_save_path=r'./resultimg')
    t = Trainer("./userimg", './torch_model/model.pt', './torch_model/model_{}_{}.pt', img_save_path=r'./resultimg')
    username = '熏小漏'
    t.segment('熏小漏.tif',username + '_result')