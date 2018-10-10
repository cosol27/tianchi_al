开源数据集：ImageNet；下载链接：http://image-net.org/download

开源模型1：InceptionV3模型；
	  下载链接：https://github.com/fchollet/deep-learning-models/releases/download/v0.5/inception_v3_weights_tf_dim_ordering_tf_kernels_notop.h5；
	  论文引用：Rethinking the Inception Architecture for Computer Vision.

开源模型2：Inception-ResNet模型；
	  下载链接：https://github.com/fchollet/deep-learning-models/releases/download/；v0.7/inception_resnet_v2_weights_tf_dim_ordering_tf_kernels_notop.h5；
	  论文引用：Inception-v4, Inception-ResNet and the Impact of Residual Connections on Learning.

开源模型3：Inception-v4模型；
	  下载链接：https://data.lip6.fr/cadene/pretrainedmodels/inceptionv4-8e4777a0.pth；
	  论文引用：Inception-v4, Inception-ResNet and the Impact of Residual Connections on Learning.

开源模型在算法中的位置和作用：
1、在训练中采用InceptionV3模型和Inception-ResNet模型进行模型融合和训练；
2、在训练中采用已经训练好的Inception-v4模型数据进行模型参数初始化。

开源模型均采用开源数据集ImageNet训练，下载链接为：http://image-net.org/download，论文引用：Inception-v4, Inception-ResNet and the Impact of Residual Connections on Learning.

pakeage：
pytorch-0.4.1
tensorflow-gpu==1.5.0
keras==2.2.2
openCV==3.4.2
numpy==1.14.3
matplotlib==2.2.2
PIL==5.1.0

注明：
导入的Sample_Process模块以及pro_main()函数是进行数据预处理的函数，是在所有程序步骤前进行的，在原有的train样本和test样本基础上额外生成train2文件夹和test_b文件夹，包含经过处理的样本图片。数据处理模块基于Python2.7编写，main.py基于python3.6版本，在整合代码的时候已经进行过代码的修改。若数据预处理过程出错，请单独先对Sample_Process.py进行运行（在运行main.py之前），并注释掉main.py中main函数的“Sample_Process.pro_main()”这行代码，再运行main.py即可以，谢谢。
