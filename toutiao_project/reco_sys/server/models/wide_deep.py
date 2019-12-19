import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

import tensorflow as tf
from tensorflow.python import keras


class WDL(object):
    """wide&deep模型
    """
    def __init__(self):
        pass

    @staticmethod
    def read_ctr_records():
        # 定义转换函数,输入时序列化的
        def parse_tfrecords_function(example_proto):
            features = {
                "label": tf.FixedLenFeature([], tf.int64),
                "feature": tf.FixedLenFeature([], tf.string)
            }
            parsed_features = tf.parse_single_example(example_proto, features)

            feature = tf.decode_raw(parsed_features['feature'], tf.float64)
            feature = tf.reshape(tf.cast(feature, tf.float32), [1, 121])
            # 特征顺序 1 channel_id,  100 article_vector, 10 user_weights, 10 article_weights
            # 1 channel_id类别型特征， 100维文章向量求平均值当连续特征，10维用户权重求平均值当连续特征
            channel_id = tf.cast(tf.slice(feature, [0, 0], [1, 1]), tf.int32)
            vector = tf.reduce_sum(tf.slice(feature, [0, 1], [1, 100]), axis=1, keep_dims=True)
            user_weights = tf.reduce_sum(tf.slice(feature, [0, 101], [1, 10]), axis=1, keep_dims=True)
            article_weights = tf.reduce_sum(tf.slice(feature, [0, 111], [1, 10]), axis=1, keep_dims=True)

            label = tf.reshape(tf.cast(parsed_features['label'], tf.float32), [1, 1])

            # 构造字典数据 名称-tensor
            FEATURE_COLUMNS = ['channel_id', 'vector', 'user_weigths', 'article_weights']
            tensor_list = [channel_id, vector, user_weights, article_weights]

            feature_dict = dict(zip(FEATURE_COLUMNS, tensor_list))

            return feature_dict, label

        dataset = tf.data.TFRecordDataset(["./train_ctr_201905.tfrecords"])
        dataset = dataset.map(parse_tfrecords_function)
        dataset = dataset.shuffle(buffer_size=10000)
        dataset = dataset.repeat(10000)
        return dataset.make_one_shot_iterator().get_next()

    def build_estimator(self):
        """建立模型
        :param dataset:
        :return:
        """
        # 离散分类
        article_id = tf.feature_column.categorical_column_with_identity('channel_id', num_buckets=25)
        # 连续类型
        vector = tf.feature_column.numeric_column('vector')
        user_weigths = tf.feature_column.numeric_column('user_weigths')
        article_weights = tf.feature_column.numeric_column('article_weights')

        wide_columns = [article_id]

        # embedding_column用来表示类别型的变量
        deep_columns = [tf.feature_column.embedding_column(article_id, dimension=25),
                        vector, user_weigths, article_weights]

        estimator = tf.estimator.DNNLinearCombinedClassifier(model_dir="./ckpt/wide_and_deep",
                                                             linear_feature_columns=wide_columns,
                                                             dnn_feature_columns=deep_columns,
                                                             dnn_hidden_units=[1024, 512, 256])

        return estimator


if __name__ == '__main__':
    wdl = WDL()
    # dataset = wdl.read_ctr_records()
    # lwf.train(dataset)
    # lwf.train_v2(dataset)
    estimator = wdl.build_estimator()
    estimator.train(input_fn=wdl.read_ctr_records, steps=10000)
    # eval_result = estimator.evaluate(input_fn=wdl.read_ctr_records, steps=10000)
    # print(eval_result)

    # 导出serving_model
    wide_columns = [tf.feature_column.categorical_column_with_identity('channel_id', num_buckets=25)]
    deep_columns = [tf.feature_column.embedding_column(tf.feature_column.categorical_column_with_identity('channel_id', num_buckets=25), dimension=25),
                    tf.feature_column.numeric_column('vector'),
                    tf.feature_column.numeric_column('user_weigths'),
                    tf.feature_column.numeric_column('article_weights')
                    ]

    columns = wide_columns + deep_columns
    feature_spec = tf.feature_column.make_parse_example_spec(columns)
    serving_input_receiver_fn = tf.estimator.export.build_parsing_serving_input_receiver_fn(feature_spec)
    estimator.export_savedmodel("./serving_model/wdl/", serving_input_receiver_fn)
