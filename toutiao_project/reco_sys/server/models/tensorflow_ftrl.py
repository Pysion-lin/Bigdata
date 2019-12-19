import tensorflow as tf
from tensorflow.python import keras


class LrWithFtrl(object):
    """LR以FTRL方式优化
    """
    def __init__(self):
        self.model = keras.Sequential([
            keras.layers.Dense(1, activation='sigmoid', input_shape=(121,))
        ])

    @staticmethod
    def read_ctr_records_to_dataset():
        """
        读取TFRecords训练文件到dattaset类型
        :return:
        """
        def parse_single_function(example):
            features = {
                "label": tf.FixedLenFeature([], tf.int64),
                "features": tf.FixedLenFeature([], tf.string)
            }
            # 解析example
            p_feature = tf.parse_single_example(example, features)
            # feature字典
            feature = tf.decode_raw(p_feature['features'], tf.float64)
            feature = tf.reshape(tf.cast(feature, tf.float32), [1, 121])
            label = tf.reshape(tf.cast(p_feature['label'], tf.float32), [1, 1])
            return feature, label

        dataset = tf.data.TFRecordDataset(["./train_ctr_20190523.tfrecords"])
        # 解析dataset中de example
        dataset = dataset.map(parse_single_function)
        dataset = dataset.shuffle(buffer_size=10000)
        dataset = dataset.repeat(10000)
        return dataset

    def train(self, dataset):
        """
        训练模型
        :return:
        """
        self.model.compile(optimizer=tf.train.FtrlOptimizer(0.03, l1_regularization_strength=0.01,
                                                            l2_regularization_strength=0.01),
                           loss='binary_crossentropy',
                           metrics=['binary_accuracy'])
        self.model.fit(dataset, steps_per_epoch=10000, epochs=1)
        self.model.summary()
        self.model.save_weights("./ckpt/ftrl/ftrl_lr.h5")

    def predict(self, inputs):
        """预测
        :return:
        """
        # 首先加载模型
        self.model.load_weights('/root/workspace/toutiao_project/reco_sys/server/models/ckpt/ftrl/ctr_lr_ftrl.h5')
        init = tf.global_variables_initializer()

        with tf.Session() as sess:
            sess.run(init)
            predictions = self.model.predict(sess.run(inputs))
        return predictions


if __name__ == '__main__':
    lwf = LrWithFtrl()
    dataset = lwf.read_ctr_records_to_dataset()
    lwf.train(dataset)
