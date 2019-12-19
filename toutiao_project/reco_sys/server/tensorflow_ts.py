# 没有GPU的支持，则添加如下环境变量，会去除程序运行时的警告
# 因为如果电脑有GPU，TensorFlow程序默认会交给GPU计算
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import tensorflow as tf


def tensorflow_demo():
    """
    通过简单案例来了解tensorflow的基础结构
    :return: None
    """
    # 一、原生python实现加法运算
    a = 10
    b = 20
    c = a + b
    print("原生Python实现加法运算方法1：\n", c)
    def add(a, b):
        return a + b
    sum = add(a, b)
    print("原生python实现加法运算方法2：\n", sum)

    # 二、tensorflow实现加法运算
    a_t = tf.constant(10)
    b_t = tf.constant(20)
    # 不提倡直接运用这种符号运算符进行计算
    # 更常用tensorflow提供的函数进行计算
    # c_t = a_t + b_t
    c_t = tf.add(a_t, b_t)
    print("tensorflow实现加法运算：\n", c_t)
    print(tf.get_default_graph())
    # 如何让计算结果出现？
    # 开启会话
    with tf.Session() as sess:
        sum_t = sess.run(c_t)
        print("在sess当中的sum_t:\n", sum_t)

    return None


def linear_regression():
    # 1）准备好数据集：y = 0.8x + 0.7 100个样本
    # 特征值X, 目标值y_true
    with tf.variable_scope("original_data"):
        X = tf.random_normal(shape=(100, 1), mean=2, stddev=2, name="original_data_x")
        # y_true [100, 1]
        # 矩阵运算 X（100， 1）* （1, 1）= y_true(100, 1)
        y_true = tf.matmul(X, [[0.8]], name="original_matmul") + 0.7
    # 2）建立线性模型：
    # y = W·X + b，目标：求出权重W和偏置b
    # 3）随机初始化W1和b1
    with tf.variable_scope("linear_model"):
        weights = tf.Variable(initial_value=tf.random_normal(shape=(1, 1)), name="weights")
        bias = tf.Variable(initial_value=tf.random_normal(shape=(1, 1)), name="bias")
        y_predict = tf.matmul(X, weights, name="model_matmul") + bias
    # 4）确定损失函数（预测值与真实值之间的误差）-均方误差
    with tf.variable_scope("loss"):
        error = tf.reduce_mean(tf.square(y_predict - y_true), name="error_op")
    # 5）梯度下降优化损失：需要指定学习率（超参数）
    # W2 = W1 - 学习率*(方向)
    # b2 = b1 - 学习率*(方向)
    with tf.variable_scope("gd_optimizer"):
        optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.01, name="optimizer").minimize(error)

    # 2）收集变量
    tf.summary.scalar("error", error)
    tf.summary.histogram("weights", weights)
    tf.summary.histogram("bias", bias)

    # 3）合并变量
    merge = tf.summary.merge_all()

    # 初始化变量
    init = tf.global_variables_initializer()
    # 创建模型保存对象
    saver = tf.train.Saver()
    # 开启会话进行训练
    with tf.Session() as sess:
        # 运行初始化变量Op
        sess.run(init)
        print("随机初始化的权重为%f， 偏置为%f" % (weights.eval(), bias.eval()))
        # 1）创建事件文件
        file_writer = tf.summary.FileWriter(logdir="./tmp/", graph=sess.graph)

        # 加载模型
        saver.restore(sess, './model/myregression.ckpt')
        print('加载模型之后的权重为{}，偏置为{}'.format(weights.eval(), bias.eval()))
        # 训练模型
        for i in range(301):
            sess.run(optimizer)
            print("第%d步的误差为%f，权重为%f， 偏置为%f" % (i, error.eval(), weights.eval(), bias.eval()))
            # 4）运行合并变量op
            summary = sess.run(merge)
            file_writer.add_summary(summary, i)
            # if i % 100 == 0:
            #     # 指定目录 + 模型名字
            #     saver.save(sess, './model/myregression.ckpt')

    return None

if __name__ == '__main__':
    # tensorflow_demo()
    linear_regression()
