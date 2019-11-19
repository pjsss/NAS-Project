import unittest
from info_str import NAS_CONFIG


class Test_static(unittest.TestCase):
    def _judge_int(self, _v):
        self.assertEqual(int, type(_v))

    def _judge_str(self, _v):
        self.assertEqual(str, type(_v))

    def _judge_float(self, _v):
        self.assertEqual(float, type(_v))

    def _judge_list(self, _v):
        self.assertEqual(list, type(_v))

    def test_int_nasmain(self):
        self._judge_int(NAS_CONFIG['nas_main']['num_gpu'])
        self._judge_int(NAS_CONFIG['nas_main']['block_num'])
        self._judge_int(NAS_CONFIG['nas_main']['num_opt_best'])
        self._judge_int(NAS_CONFIG['nas_main']['opt_best_k'])
        self._judge_int(NAS_CONFIG['nas_main']['finetune_threshold'])
        self._judge_int(NAS_CONFIG['nas_main']['subp_debug'])
        self._judge_int(NAS_CONFIG['nas_main']['eva_debug'])
        self._judge_int(NAS_CONFIG['nas_main']['ops_debug'])


    def test_int_enum(self):
        self._judge_int(NAS_CONFIG['enum']['debug'])
        self._judge_int(NAS_CONFIG['enum']['depth'])
        self._judge_int(NAS_CONFIG['enum']['width'])
        self._judge_int(NAS_CONFIG['enum']['max_depth'])
        self._judge_int(NAS_CONFIG['enum']['enum_debug'])

    def test_int_eva(self):
        self._judge_int(NAS_CONFIG['eva']['image_size'])
        self._judge_int(NAS_CONFIG['eva']['num_classes'])
        self._judge_int(NAS_CONFIG['eva']['num_examples_for_train'])
        self._judge_int(NAS_CONFIG['eva']['num_examples_per_epoch_for_eval'])
        self._judge_int(NAS_CONFIG['eva']['batch_size'])
        self._judge_int(NAS_CONFIG['eva']['epoch'])

    def test_float_eva(self):
        self._judge_float(NAS_CONFIG['eva']['initial_learning_rate'])
        self._judge_float(NAS_CONFIG['eva']['num_epochs_per_decay'])
        self._judge_float(NAS_CONFIG['eva']['learning_rate_decay_factor'])
        self._judge_float(NAS_CONFIG['eva']['moving_average_decay'])
        self._judge_float(NAS_CONFIG['eva']['weight_decay'])
        self._judge_float(NAS_CONFIG['eva']['momentum_rate'])

    def test_str_eva(self):
        self._judge_str(NAS_CONFIG['eva']['model_path'])
        self._judge_str(NAS_CONFIG['eva']['learning_rate_type'])

    def test_list_eva(self):
        self._judge_list(NAS_CONFIG['eva']['boundaries'])
        self._judge_list(NAS_CONFIG['eva']['learing_rate'])

    def test_int_spl(self):
        self._judge_int(NAS_CONFIG['spl']['skip_max_dist'])
        self._judge_int(NAS_CONFIG['spl']['skip_max_num'])
        self._judge_int(NAS_CONFIG['spl']['pool_switch'])

    def test_str_spl(self):
        self._judge_str(NAS_CONFIG['spl']['spl_log_path'])

    def test_space_ops_conv(self):
        self._judge_list(NAS_CONFIG['spl']['conv_space']['filter_size'])
        for li in NAS_CONFIG['spl']['conv_space']['filter_size']:
            for i in li:
                self._judge_int(i)

        self._judge_list(NAS_CONFIG['spl']['conv_space']['kernel_size'])
        for i in NAS_CONFIG['spl']['conv_space']['kernel_size']:
            self._judge_int(i)

        self._judge_list(NAS_CONFIG['spl']['conv_space']['activation'])
        for i in NAS_CONFIG['spl']['conv_space']['activation']:
            self._judge_str(i)

    def test_space_ops_pooling(self):
        self._judge_list(NAS_CONFIG['spl']['pool_space']['pooling_type'])
        for i in NAS_CONFIG['spl']['pool_space']['pooling_type']:
            self._judge_str(i)

        self._judge_list(NAS_CONFIG['spl']['pool_space']['kernel_size'])
        for i in NAS_CONFIG['spl']['pool_space']['kernel_size']:
            self._judge_int(i)


if __name__ == "__main__":
    unittest.main()
