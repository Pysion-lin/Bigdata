import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import argparse
import tensorflow as tf

from server.models import iris_data


def iris_estiamtor():
    # 1、 创建一个或多个输入函数。
    # 2、定义模型的特征列。
    # 3、实例化 Estimator，指定特征列和各种超参数。
    # 4、在 Estimator 对象上调用一个或多个方法，传递适当的输入函数作为数据的来源。

    # 获取数据
    (train_x, train_y), (test_x, test_y) = iris_data.load_data()

    # 特征处理
    my_feature_columns = []
    for key in train_x.keys():
        my_feature_columns.append(tf.feature_column.numeric_column(key=key))
    print("四列特征的处理方式指定：", my_feature_columns)

    # 建立两层，每层10个神经元的网络
    classifier = tf.estimator.DNNClassifier(
        feature_columns=my_feature_columns,
        hidden_units=[10, 10],
        n_classes=3)

    # 训练模型
    classifier.train(
        input_fn=lambda: iris_data.train_input_fn(train_x, train_y, 32),
        steps=1000)

    # 评估模型
    eval_result = classifier.evaluate(
        input_fn=lambda: iris_data.eval_input_fn(test_x, test_y, 32))

    print('result: {}'.format(eval_result))

    # 进行结果预测
    # 目标值
    expected = ['Setosa', 'Versicolor', 'Virginica']
    # 特征值
    predict_x = {
        'SepalLength': [5.1, 5.9, 6.9],
        'SepalWidth': [3.3, 3.0, 3.1],
        'PetalLength': [1.7, 4.2, 5.4],
        'PetalWidth': [0.5, 1.5, 2.1],
    }

    predictions = classifier.predict(
        input_fn=lambda: iris_data.eval_input_fn(predict_x,
                                                labels=None,
                                                batch_size=32))

    # for pred_dict, expec in zip(predictions, expected):
    #     class_id = pred_dict['class_ids'][0]
    #     probability = pred_dict['probabilities'][class_id]
    #
    #     print('\nPrediction is "{}" ({:.1f}%), expected "{}"'.format(iris_data.SPECIES[class_id],
    #                           100 * probability, expec))
    print(predictions)
    for i in predictions:
        print(i)

if __name__ == '__main__':
    iris_estiamtor()
