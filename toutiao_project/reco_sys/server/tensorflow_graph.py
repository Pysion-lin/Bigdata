import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import tensorflow as tf


def graph_demo():
    # 图的演示
    a_t = tf.constant(10)
    b_t = tf.constant(20)
    # 不提倡直接运用这种符号运算符进行计算
    # 更常用tensorflow提供的函数进行计算
    # c_t = a_t + b_t
    c_t = tf.add(a_t, b_t)
    print("tensorflow实现加法运算：\n", c_t)

    # 获取默认图
    default_g = tf.get_default_graph()
    print("获取默认图：\n", default_g)

    # 数据的图属性
    print("a_t的graph:\n", a_t.graph)
    print("b_t的graph:\n", b_t.graph)
    # 操作的图属性
    print("c_t的graph:\n", c_t.graph)

    # 开启会话
    with tf.Session() as sess:
        sum_t = sess.run(c_t)
        print("在sess当中的sum_t:\n", sum_t)
        # 会话的图属性
        print("会话的图属性：\n", sess.graph)

    return None


def graph_demo2():
    # 图的演示
    a_t = tf.constant(10)
    b_t = tf.constant(20)
    # 不提倡直接运用这种符号运算符进行计算
    # 更常用tensorflow提供的函数进行计算
    # c_t = a_t + b_t
    c_t = tf.add(a_t, b_t)
    print("tensorflow实现加法运算：\n", c_t)

    # 获取默认图
    default_g = tf.get_default_graph()
    print("获取默认图：\n", default_g)

    # 数据的图属性
    print("a_t的graph:\n", a_t.graph)
    print("b_t的graph:\n", b_t.graph)
    # 操作的图属性
    print("c_t的graph:\n", c_t.graph)

    # 自定义图
    new_g = tf.Graph()
    print("自定义图：\n", new_g)
    # 在自定义图中去定义数据和操作
    with new_g.as_default():
        new_a = tf.constant(30)
        new_b = tf.constant(40)
        new_c = tf.add(new_a, new_b)

    # 数据的图属性
    print("new_a的graph:\n", new_a.graph)
    print("new_b的graph:\n", new_b.graph)
    # 操作的图属性
    print("new_c的graph:\n", new_c.graph)

    # 开启会话
    with tf.Session() as sess:
        sum_t = sess.run(c_t)
        print("在sess当中的sum_t:\n", sum_t)
        # 会话的图属性
        print("会话的图属性：\n", sess.graph)
        # 不同的图之间不能互相访问
        # sum_new = sess.run(new_c)
        # print("在sess当中的sum_new:\n", sum_new)

    # config是否打印使用的设备信息
    with tf.Session(graph=new_g, config=tf.ConfigProto(allow_soft_placement=True,
                                        log_device_placement=True)) as sess2:
        sum_new = sess2.run(new_c)
        print("在sess2当中的sum_new:\n", sum_new)
        print("会话的图属性：\n", sess2.graph)

        # 返回filewriter,写入事件文件到指定目录(最好用绝对路径)，以提供给tensorboard使用
        tf_writer = tf.summary.FileWriter('./tmp/', graph=sess2.graph)

    # 很少会同时开启不同的图，一般用默认的图就够了
    return None


def sess_demo():
    # 自定义图
    new_g = tf.Graph()
    # 在自定义图中去定义数据和操作
    with new_g.as_default():
        new_a = tf.constant(30)
        new_b = tf.constant(40)
        new_c = tf.add(new_a, new_b)
        # 定义占位符
        a = tf.placeholder(tf.float32)
        b = tf.placeholder(tf.float32)
        sum_ab = tf.add(a, b)
        print("sum_ab:\n", sum_ab)

    with tf.Session(graph=new_g) as sess2:
        sum_new = sess2.run(new_c)
        # print(new_c.eval())
        print("在sess2当中的sum_new:\n", sum_new)
        print("占位符的结果：\n", sess2.run(sum_ab, feed_dict={a: 3.0, b: 4.0}))

    return None


def tensor_ts():
    # 创建张量
    # tensor1 = tf.constant(4.0)
    # tensor2 = tf.constant([1, 2, 3, 4])
    # linear_squares = tf.constant([[4], [9], [16], [25]], dtype=tf.int32)
    # print(tensor1, tensor2, linear_squares)

    # 定义占位符
    a_p = tf.placeholder(dtype=tf.float32, shape=[None, None])
    b_p = tf.placeholder(dtype=tf.float32, shape=[None, 10])
    c_p = tf.placeholder(dtype=tf.float32, shape=[3, 2])
    # 获取静态形状
    print("a_p的静态形状为：\n", a_p.get_shape())
    print("b_p的静态形状为：\n", b_p.get_shape())
    print("c_p的静态形状为：\n", c_p.get_shape())

    # 形状更新
    # a_p.set_shape([2, 3])
    # 静态形状已经固定部分就不能修改了
    # b_p.set_shape([10, 3])
    # c_p.set_shape([2, 3])

    # 获取静态形状
    print("a_p的静态形状为：\n", a_p.shape)
    print("b_p的静态形状为：\n", b_p.shape)
    print("c_p的静态形状为：\n", c_p.shape)

    # 动态形状
    # c_p_r = tf.reshape(c_p, [1, 2, 3])
    c_p_r = tf.reshape(c_p, [2, 3])
    # 动态形状，改变的时候，不能改变元素的总个数
    # c_p_r2 = tf.reshape(c_p, [3, 1])
    print("动态形状的结果：\n", c_p_r)
    # print("动态形状的结果2：\n", c_p_r2)

    return None


def variable_demo():
    """
    变量的演示
    :return:
    """
    # 定义变量
    a = tf.Variable(initial_value=30)
    b = tf.Variable(initial_value=40)
    sum = tf.add(a, b)

    # 初始化变量
    init = tf.global_variables_initializer()

    # 开启会话
    with tf.Session() as sess:
        # 变量初始化
        sess.run(init)
        print("sum:\n", sess.run(sum))

    return None

if __name__ == '__main__':
    # graph_demo()
    # graph_demo2()
    # sess_demo()
    # tensor_ts()
    variable_demo()
